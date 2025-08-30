from flask import current_app
import sqlite3


def get_client(client_id):
    query = """SELECT client_name, contact_name, contact_email, contact_phone, billing_address, billing_terms, industry, status FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    client = cursor.fetchone()
    cursor.close()
    return client


def update_client(client_id, update_info):
    query = """UPDATE client SET client_name = :client_name, contact_name = :contact_name, contact_email = :email, contact_phone = :phone, billing_address = :address, billing_terms = :terms, industry = :industry, updated_at = :updated_at WHERE client_id = :client_id;"""
    values = {
        "client_id": client_id,
        "client_name": update_info.client_name,
        "contact_name": update_info.contact_name,
        "email": update_info.email,
        "phone": update_info.phone,
        "address": update_info.address,
        "terms": update_info.terms,
        "industry": update_info.industry,
        "updated_at": update_info.updated_at.isoformat()
    }

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_employee(employee_id):
    query = """SELECT full_name, email, phone, rate_type, default_bill_rate, default_pay_rate, role_title, status FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": employee_id})
    employee = cursor.fetchone()
    cursor.close()
    return employee


def update_employee(employee_id, update_info):
    query = """UPDATE employee SET full_name = :full_name, email = :email, phone = :phone, rate_type = :rate_type, default_bill_rate = :bill_rate, default_pay_rate = :pay_rate, role_title = :title, updated_at = :updated_at WHERE employee_id = :employee_id;"""
    values = {
        "employee_id": employee_id,
        "full_name": update_info.full_name,
        "email": update_info.email,
        "phone": update_info.phone,
        "rate_type": update_info.rate_type,
        "bill_rate": float(update_info.bill_rate),
        "pay_rate": float(update_info.pay_rate),
        "title": update_info.title,
        "updated_at": update_info.updated_at.isoformat()
    }

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_job(job_id):
    query = """SELECT client_id, position_title, staff_type, location, bill_rate, pay_rate, currency, start_date, end_date, notes FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": job_id})
    job = cursor.fetchone()
    cursor.close()
    return job


def update_job(job_id, update_info):
    query = """UPDATE job SET client_id = :client_id, position_title = :title, staff_type = :staff_type, location = :location, bill_rate = :bill_rate, pay_rate = :pay_rate, currency = :currency, start_date = :start_date, end_date = :end_date, notes = :notes, updated_at = :updated_at WHERE job_id = :job_id;"""
    values = {
        "job_id": job_id,
        "client_id": update_info.client_id,
        "title": update_info.title,
        "staff_type": update_info.staff_type,
        "location": update_info.location,
        "bill_rate": float(update_info.bill_rate),
        "pay_rate": float(update_info.pay_rate),
        "currency": update_info.currency,
        "start_date": update_info.start_date.isoformat(),
        "end_date": update_info.end_date.isoformat(),
        "updated_at": update_info.updated_at.isoformat()
    }
    if len(update_info.notes) == 0:
        values["notes"] = None
    else:
        values["notes"] = update_info.notes

    cursor = current_app.db.execute(query, values)
    current_app.db.commit()
    cursor.close()


def get_placement(placement_id):
    query = """SELECT job_id, employee_id FROM placement WHERE placement_id = :placement_id;"""
    cursor = current_app.db.execute(query, {"placement_id": placement_id})
    placement = cursor.fetchone()
    cursor.close()
    return placement


def update_placement(placement_id, update_info):
    query = """SELECT status FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": update_info.employee_id})
    employee_status = cursor.fetchone()[0]
    if employee_status == "Active" or employee_status == "Inactive":
        cursor.close()
        return
    
    query = """SELECT status FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": update_info.job_id})
    job_status = cursor.fetchone()[0]
    if job_status == "filled" or job_status == "closed":
        cursor.close()
        return

    query = """UPDATE placement SET job_id = :job_id, employee_id = :employee_id, updated_at = :updated_at WHERE placement_id = :placement_id;"""
    values = {
        "placement_id": placement_id,
        "job_id": update_info.job_id,
        "employee_id": update_info.employee_id,
        "updated_at": update_info.updated_at.isoformat()
    }

    try:
        cursor = current_app.db.execute(query, values)
    except sqlite3.ProgrammingError:
        cursor.close()
        return

    query = """SELECT start_date, end_date, bill_rate, pay_rate FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": update_info.job_id})
    new_job = cursor.fetchone()

    query = """UPDATE placement SET start_date = :start_date, end_date = :end_date, bill_rate = :bill_rate, pay_rate = :pay_rate WHERE placement_id = :placement_id;"""
    values = {
        "placement_id": placement_id,
        "start_date": new_job[0],
        "end_date": new_job[1],
        "bill_rate": new_job[2],
        "pay_rate": new_job[3]
    }
    cursor = current_app.db.execute(query, values)

    current_app.db.commit()
    cursor.close()