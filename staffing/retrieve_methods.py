from flask import current_app
from datetime import datetime, date


def get_client_info():
    query = """SELECT client_id, client_name, contact_name, contact_email, contact_phone, billing_address, billing_terms, industry, status FROM client;"""
    cursor = current_app.db.execute(query)
    clients = cursor.fetchall()
    cursor.close()
    return clients


def get_employee_info():
    query = """SELECT employee_id, full_name, email, phone, rate_type, default_pay_rate, default_bill_rate, role_title, status FROM employee;"""
    cursor = current_app.db.execute(query)
    employees = cursor.fetchall()
    cursor.close()
    return employees


def get_job_info():
    query = """SELECT job_id, client_id, position_title, staff_type, location, bill_rate, pay_rate, currency, start_date, end_date, status, notes FROM job;"""
    cursor = current_app.db.execute(query)
    jobs_tup = cursor.fetchall()
    cursor.close()

    jobs = []
    for job in jobs_tup:
        jobs.append(clean_job(job))
    
    return jobs


def clean_job(raw_job):
    job = []
    job.append(raw_job[0])    # job_id

    # Client
    client_id = raw_job[1]
    query = """SELECT client_name FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    client_name = cursor.fetchone()[0]
    job.append(client_name)

    job += raw_job[2:5]    # position_title, staff_type, location

    # Bill/Pay Rate
    job.append(str(raw_job[5]) + " " + raw_job[7])
    job.append(str(raw_job[6]) + " " + raw_job[7])

    # Start/End Dates
    start_date_raw = date.fromisoformat(raw_job[8])
    end_date_raw = date.fromisoformat(raw_job[9])
    start_date = start_date_raw.strftime("%B %#d, %Y")
    end_date = end_date_raw.strftime("%B %#d, %Y")
    job += [start_date, end_date]

    job += raw_job[10:]    # status, notes
    
    return job


def get_placement_info():
    query = """SELECT placement_id, job_id, employee_id, start_date, end_date, bill_rate, pay_rate, status FROM placement;"""
    cursor = current_app.db.execute(query)
    placements_tup = cursor.fetchall()
    cursor.close()

    placements = []
    for placement in placements_tup:
        placements.append(clean_placement(placement))
    
    return placements


def clean_placement(raw_placement):
    placement = []
    placement.append(raw_placement[0])
    
    # Client/Position
    query = """SELECT client_id, position_title, currency FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": raw_placement[1]})
    client_info = cursor.fetchone()
    
    query = """SELECT client_name FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_info[0]})
    client_name = cursor.fetchone()[0]
    placement += [client_name, client_info[1]]

    # Employee
    query = """SELECT full_name FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": raw_placement[2]})
    employee_name = cursor.fetchone()
    placement.append(employee_name[0])

    # Start/End Dates
    start_date_raw = date.fromisoformat(raw_placement[3])
    end_date_raw = date.fromisoformat(raw_placement[4])
    start_date = start_date_raw.strftime("%B %#d, %Y")
    end_date = end_date_raw.strftime("%B %#d, %Y")
    placement += [start_date, end_date]

    # Bill/Pay Rate
    placement.append(str(raw_placement[5]) + " " + client_info[2])
    placement.append(str(raw_placement[6]) + " " + client_info[2])
    
    placement.append(raw_placement[7])    # Status

    cursor.close()
    return placement