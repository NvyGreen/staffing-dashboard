from flask import current_app
import sqlite3


def register_client(new_client):
    query = """INSERT INTO client (client_name, contact_name, contact_email, contact_phone, billing_address, billing_terms, industry, status, created_at, updated_at) VALUES (:client_name, :contact_name, :contact_email, :contact_phone, :billing_address, :billing_terms, :industry, :status, :created_at, :updated_at);"""
    values = {
        "client_name": new_client.client_name,
        "contact_name": new_client.contact_name,
        "contact_email": new_client.email,
        "contact_phone": new_client.phone,
        "billing_address": new_client.address,
        "billing_terms": new_client.terms,
        "industry": new_client.industry,
        "status": new_client.status
    }
    
    created_at = new_client.created_at.isoformat()
    updated_at = new_client.updated_at.isoformat()

    values["created_at"] = created_at
    values["updated_at"] = updated_at

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def register_employee(new_employee):
    query = """INSERT INTO employee (full_name, email, phone, rate_type, default_pay_rate, default_bill_rate, role_title, status, created_at, updated_at) VALUES (:full_name, :email, :phone, :rate_type, :pay_rate, :bill_rate, :role_title, :status, :created_at, :updated_at);"""
    values = {
        "full_name": new_employee.full_name,
        "email": new_employee.email,
        "phone": new_employee.phone,
        "rate_type": new_employee.rate_type,
        "role_title": new_employee.title,
        "status": new_employee.status
    }
    
    created_at = new_employee.created_at.isoformat()
    updated_at = new_employee.updated_at.isoformat()

    values["pay_rate"] = float(new_employee.pay_rate)
    values["bill_rate"] = float(new_employee.bill_rate)
    values["created_at"] = created_at
    values["updated_at"] = updated_at

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_client_dropdown():
    cursor = current_app.db.execute("""SELECT client_id, client_name FROM client WHERE status = :status;""", {"status": "Active"})
    clients = cursor.fetchall()
    cursor.close()    
    return clients


def add_job(new_job):
    query = """INSERT INTO job (client_id, position_title, staff_type, location, bill_rate, pay_rate, currency, start_date, end_date, staff_needed, status, notes, created_at, updated_at) VALUES (:client_id, :position_title, :staff_type, :location, :bill_rate, :pay_rate, :currency, :start_date, :end_date, :staff_needed, :status, :notes, :created_at, :updated_at);"""
    values = {
        "client_id": new_job.client_id,
        "position_title": new_job.title,
        "staff_type": new_job.staff_type,
        "location": new_job.location,
        "bill_rate": float(new_job.bill_rate),
        "pay_rate": float(new_job.pay_rate),
        "currency": new_job.currency,
        "start_date": new_job.start_date.isoformat(),
        "end_date": new_job.end_date.isoformat(),
        "staff_needed": new_job.staff_needed,
        "status": new_job.status,
        "created_at": new_job.created_at.isoformat(),
        "updated_at": new_job.updated_at.isoformat()
    }

    if len(new_job.notes) == 0:
        values["notes"] = None
    else:
        values["notes"] = new_job.notes

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_job_dropdown():
    query = """SELECT job_id, client_id, position_title FROM job WHERE status = :status;"""
    cursor = current_app.db.execute(query, {"status": "open"})
    raw_options = cursor.fetchall()
    options = []

    for option in raw_options:
        options.append(clean_job_option(option))
    
    cursor.close()
    return options


def clean_job_option(raw_option):
    job_id, client_id, title = raw_option

    query = """SELECT client_name FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    client_name = cursor.fetchone()[0]
    cursor.close()

    option = (job_id, client_name + " - " + title)
    return option


def get_employee_dropdown():
    query = """SELECT employee_id, full_name FROM employee WHERE status = :status;"""
    cursor = current_app.db.execute(query, {"status": "Standby"})
    employee_options = cursor.fetchall()
    cursor.close()
    return employee_options


def place_employee(new_placement):
    query = """SELECT status FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": new_placement.employee_id})
    employee_status = cursor.fetchone()[0]
    if employee_status == "Active" or employee_status == "Inactive":
        cursor.close()
        return

    query = """SELECT status FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": new_placement.job_id})
    job_status = cursor.fetchone()[0]
    if job_status == "filled" or job_status == "closed":
        cursor.close()
        return

    query = """SELECT start_date, end_date, bill_rate, pay_rate FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": new_placement.job_id})
    job_placement = cursor.fetchone()

    query = """INSERT INTO placement (job_id, employee_id, start_date, end_date, bill_rate, pay_rate, status, created_at, updated_at) VALUES (:job_id, :employee_id, :start_date, :end_date, :bill_rate, :pay_rate, :status, :created_at, :updated_at);"""
    values = {
        "job_id": new_placement.job_id,
        "employee_id": new_placement.employee_id,
        "start_date": job_placement[0],
        "end_date": job_placement[1],
        "bill_rate": job_placement[2],
        "pay_rate": job_placement[3],
        "status": new_placement.status,
        "created_at": new_placement.created_at.isoformat(),
        "updated_at": new_placement.updated_at.isoformat()
    }

    try:
        cursor = current_app.db.execute(query, values)
    except sqlite3.ProgrammingError:
        cursor.close()
        return

    query = """UPDATE job set staff_needed = staff_needed - 1 WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": new_placement.job_id})

    query = """SELECT staff_needed FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": new_placement.job_id})
    positions_left = cursor.fetchone()[0]

    if positions_left == 0:
        query = """UPDATE job SET status = :status WHERE job_id = :job_id;"""
        cursor = current_app.db.execute(query, {"status": "filled", "job_id": new_placement.job_id})

    query = """UPDATE employee SET status = :status WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"status": "Active", "employee_id": new_placement.employee_id})

    current_app.db.commit()
    cursor.close()