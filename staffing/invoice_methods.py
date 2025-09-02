from flask import current_app
from datetime import date, datetime, timedelta


def generate_invoice(client_id):
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
        cursor = current_app.db.execute(query, {"job_id", job[0]})
        placements += cursor.fetchall()
    if len(placements) == 0:
        return
    
    # Get client timesheets
    query = """SELECT timesheet_id FROM timesheet WHERE placement_id = :placement_id;"""
    timesheets = []
    for placement in placements:
        cursor = current_app.db.execute(query, {"timesheet_id", placement[0]})
        timesheets += cursor.fetchall()
    if len(timesheets) == 0:
        return
    
    # See if client has invoice
    query = """SELECT invoice_id FROM invoice WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    invoice = cursor.fetchone()

    # Generate invoice if there isn't one
    if invoice is None:
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
        query = """INSERT INTO invoice (client_id, invoice_no, issue_date, due_date, created_at, updated_at) VALUES (:client_id, :invoice_no, :issue_date, :due_date, :created_at, :updated_at);"""
        values = {
            "client_id": client_id,
            "invoice_no": invoice_no,
            "issue_date": today,
            "due_date": due_date,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        cursor = current_app.db.execute(query, values)
        current_app.db.commit()

        # Get the invoice id after creation
        query = """SELECT invoice_id FROM invoice WHERE client_id = :client_id;"""
        cursor = current_app.db.execute(query, {"client_id": client_id})
        invoice = cursor.fetchone()
    
    pass