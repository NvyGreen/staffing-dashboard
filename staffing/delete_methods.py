from flask import current_app


def delete_client(client_id):
    query = """SELECT job_id FROM job WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    jobs = cursor.fetchall()

    if len(jobs) > 0:
        for job in jobs:
            delete_job(job[0])
    
    query = """DELETE FROM client WHERE client_id = :client_id;"""
    cursor = current_app.db.execute(query, {"client_id": client_id})
    current_app.db.commit()
    cursor.close()


def delete_employee(employee_id):
    query = """SELECT placement_id FROM placement WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": employee_id})
    placements = cursor.fetchall()

    if len(placements) > 0:
        for placement in placements:
            delete_placement(placement[0])
    
    query = """DELETE FROM employee WHERE employee_id = :employee_id;"""
    cursor = current_app.db.execute(query, {"employee_id": employee_id})
    current_app.db.commit()
    cursor.close()


def delete_job(job_id):
    query = """SELECT placement_id FROM placement WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": job_id})
    placements = cursor.fetchall()

    if len(placements) > 0:
        for placement in placements:
            delete_placement(placement[0])
    
    query = """DELETE FROM job WHERE job_id = :job_id;"""
    cursor = current_app.db.execute(query, {"job_id": job_id})
    current_app.db.commit()
    cursor.close()


def delete_placement(placement_id):
    query = """DELETE FROM placement WHERE placement_id = :placement_id;"""
    cursor = current_app.db.execute(query, {"placement_id": placement_id})
    current_app.db.commit()
    cursor.close()