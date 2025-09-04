from flask import current_app
from datetime import date, datetime, timedelta


def generate_invoice_items(client_id):
    # Get client jobs
    query = """SELECT job_id FROM job WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    jobs = cursor.fetchall()
    if len(jobs) == 0:
        return

    # Get client placements
    query = """SELECT placement_id FROM placement WHERE job_id = :job_id;"""
    placements = []
    for job in jobs:
        cursor = current_app.db.execute(query, {"job_id": job[0]})
        placements += cursor.fetchall()
    if len(placements) == 0:
        return
    
    # Get client timesheets
    query = """SELECT timesheet_id FROM timesheet WHERE placement_id = :placement_id AND status = :status;"""
    timesheets = []
    for placement in placements:
        cursor = current_app.db.execute(query, {"placement_id": placement[0], "status": "approved"})
        timesheets += cursor.fetchall()
    if len(timesheets) == 0:
        return
    
    # See if client has invoice
    query = """SELECT invoice_id FROM invoice WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    invoice = cursor.fetchone()

    # Generate invoice if there isn't one
    if invoice is None:
        create_new_invoice(client_id)

        # Get the invoice id after creation
        query = """SELECT invoice_id FROM invoice WHERE client_id = :client_id;"""
        cursor = current_app.db.execute(query, {"client_id": client_id})
        invoice = cursor.fetchone()
    
    # Clean timesheet ids
    for i in range(len(timesheets)):
        timesheets[i] = timesheets[i][0]

    # Find out what timesheets are already invoiced
    invoice = invoice[0]
    query = """SELECT timesheet_id FROM invoice_item WHERE invoice_id = :invoice_id;"""
    cursor = current_app.db.execute(query, {"invoice_id": invoice})

    invoice_sheets = cursor.fetchall()
    for i in range(len(invoice_sheets)):
        invoice_sheets[i] = invoice_sheets[i][0]
    
    # Make sure duplicates are not added
    i = 0
    while i < len(timesheets):
        if timesheets[i] in invoice_sheets:
            timesheets.remove(timesheets[i])
            i -= 1
        i += 1
    
    # Create invoice items for each timesheet
    for timesheet in timesheets:
        create_invoice_item(invoice, timesheet)
    
    # Fill subtotal, total, and balance entries
    fill_total(invoice)
    cursor.close()


def create_new_invoice(client_id):
    # Generate invoice if there isn't one
    today = date.today()
    query = """SELECT invoice_no FROM invoice ORDER BY invoice_id DESC LIMIT 1;"""
    cursor = current_app.db.execute(query)
    last_invoice = cursor.fetchone()
    invoice_no = ""

    # Generate invoice number
    if last_invoice is not None:
        last_invoice = last_invoice[0]
        invoice_date = last_invoice[4:10]
        invoice_date = datetime.strptime(invoice_date, "%y%m%d")

        if invoice_date == today.strftime("%y%m%d"):    # if invoice is being created on same day as last invoice
            last_no = int(last_invoice[11:])
            new_no = last_no + 1

            if len(str(new_no)) == 1:
                new_no = "00" + str(new_no)
            elif len(str(new_no)) == 2:
                new_no = "0" + str(new_no)
            else:
                new_no = str(new_no)
            
            invoice_no = "INV-" + today.strftime("%y%m%d") + "-" + new_no
        else:
            invoice_no = "INV-" + today.strftime("%y%m%d") + "-001"
    else:
        invoice_no = "INV-" + today.strftime("%y%m%d") + "-001"
    
    # Generate due date
    due_date = today + timedelta(days=15)

    # Insert invoice
    query = """INSERT INTO invoice (client_id, invoice_no, issue_date, due_date, tax_amount, created_at, updated_at) VALUES (:client_id, :invoice_no, :issue_date, :due_date, :tax_amount, :created_at, :updated_at);"""
    values = {
        "client_id": client_id,
        "invoice_no": invoice_no,
        "issue_date": today,
        "due_date": due_date,
        "tax_amount": 0.075,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def create_invoice_item(invoice_id, timesheet_id):
    # Get total hours worked
    query = """SELECT hours, overtime_hours FROM timesheet_entry WHERE timesheet_id = :timesheet_id;"""
    cursor = current_app.db.execute(query, {"timesheet_id": timesheet_id})
    entries = cursor.fetchall()

    hours = 0
    ot_hours = 0
    for entry in entries:
        hours += entry[0]
        ot_hours += entry[1]
    
    # Get bill rate
    query = """SELECT placement_id FROM timesheet WHERE timesheet_id = :timesheet_id;"""
    cursor = current_app.db.execute(query, {"timesheet_id": timesheet_id})
    placement = cursor.fetchone()[0]

    query = """SELECT job_id, employee_id FROM placement WHERE placement_id = :placement_id;"""
    cursor = current_app.db.execute(query, {"placement_id": placement})
    job, employee = cursor.fetchone()

    query = """SELECT position_title, bill_rate FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": job})
    title, job_bill_rate = cursor.fetchone()

    query = """SELECT full_name, default_bill_rate FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": employee})
    employee_name, employee_bill_rate = cursor.fetchone()

    bill_rate = max(job_bill_rate, employee_bill_rate)

    # Generate description
    description = employee_name + " - " + title

    # Create entry
    query = """INSERT INTO invoice_item (invoice_id, description, hours, ot_hours, bill_rate, timesheet_id, created_at) VALUES (:invoice_id, :description, :hours, :ot_hours, :bill_rate, :timesheet_id, :created_at);"""
    values = {
        "invoice_id": invoice_id,
        "description": description,
        "hours": hours,
        "ot_hours": ot_hours,
        "bill_rate": bill_rate,
        "timesheet_id": timesheet_id,
        "created_at": datetime.now()
    }
    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def fill_total(invoice_id):
    query = """SELECT amount FROM invoice_item WHERE invoice_id = :invoice_id;"""
    cursor = current_app.db.execute(query, {"invoice_id": invoice_id})
    amounts = cursor.fetchall()
    subtotal = 0

    for amount in amounts:
        subtotal += amount[0]
    
    query = """SELECT tax_amount FROM invoice WHERE invoice_id = :invoice_id;"""
    cursor = current_app.db.execute(query, {"invoice_id": invoice_id})
    tax = cursor.fetchone()[0]

    total = subtotal * (1 + tax)

    query = """UPDATE invoice SET subtotal = :subtotal, total = :total, balance = :balance;"""
    values = {
        "subtotal": subtotal,
        "total": total,
        "balance": total
    }

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_client_invoice(client_id):
    generate_invoice_items(client_id)

    query = """SELECT invoice_id, invoice_no, issue_date, due_date, subtotal, tax_amount, total, balance FROM invoice WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    invoice = cursor.fetchone()

    query = """SELECT hours, ot_hours, bill_rate, amount, timesheet_id FROM invoice_item WHERE invoice_id = :invoice_id;"""
    cursor = current_app.db.execute(query, {"invoice_id": invoice[0]})
    invoice_data = cursor.fetchall()
    if len(invoice_data) == 0:
        return []
    
    invoice_items = []
    for item in invoice_data:
        query = """SELECT placement_id, start_date, end_date FROM timesheet WHERE timesheet_id = :timesheet_id;"""
        cursor = current_app.db.execute(query, {"timesheet_id": item[4]})
        timesheet = cursor.fetchone()

        query = """SELECT job_id, employee_id FROM placement WHERE placement_id = :placement_id;"""
        cursor = current_app.db.execute(query, {"placement_id": timesheet[0]})
        placement = cursor.fetchone()

        query = """SELECT position_title FROM job WHERE job_id = :job_id;"""
        cursor = current_app.db.execute(query, {"job_id": placement[0]})
        title = cursor.fetchone()[0]

        query = """SELECT full_name FROM employee WHERE employee_id = :employee_id;"""
        cursor = current_app.db.execute(query, {"employee_id": placement[1]})
        employee = cursor.fetchone()[0]

        start_date, end_date = timesheet[1:3]
        reg_hours, reg_rate = item[0], item[2]
        reg_amt = reg_hours * reg_rate
        ot_hours, ot_rate = item[1], item[2] * 1.5
        ot_amt = ot_hours * ot_rate
        total = item[3]

        line_item = [employee, title, start_date, end_date, reg_hours, reg_rate, reg_amt, ot_hours, ot_rate, ot_amt, total]
        invoice_items.append(line_item)
    
    invoice_no, issue_date, due_date = invoice[1:4]

    query = """SELECT contact_name, contact_email, contact_phone, billing_address, billing_terms FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    contact_name, email, phone, address, terms = cursor.fetchone()

    return [invoice_no, contact_name, email, phone, address, issue_date, due_date, terms, invoice_items]