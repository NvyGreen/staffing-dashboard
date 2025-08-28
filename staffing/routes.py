from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)
from staffing.forms import (
    AddClient,
    AddEmployee,
    AddJob,
    PlaceEmployee,
    EditClient,
    EditEmployee,
    EditJob,
    EditPlacement
)
from staffing.models import (
    Client,
    Employee,
    Job,
    Placement
)
import staffing.retrieve_methods as retrieve_methods
import staffing.add_methods as add_methods
import staffing.edit_methods as edit_methods
import staffing.delete_methods as delete_methods
from datetime import datetime, date


pages = Blueprint(
    "pages",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@pages.route("/")
def index():
    return render_template(
        "index.html",
        title="Dashboard"
    )

@pages.route("/clients")
def clients():
    clients = retrieve_methods.get_client_info()
    return render_template(
        "clients.html",
        title="Dashboard | Clients",
        clients=clients
    )

@pages.route("/employees")
def employees():
    employees = retrieve_methods.get_employee_info()
    return render_template(
        "employees.html",
        title="Dashboard | Employees",
        employees=employees
    )


@pages.route("/jobs")
def jobs():
    jobs = retrieve_methods.get_job_info()
    return render_template(
        "jobs.html",
        title="Dashboard | Jobs",
        jobs=jobs
    )


@pages.route("/placements")
def placements():
    placements = retrieve_methods.get_placement_info()
    return render_template(
        "placements.html",
        title="Dashboard | Placements",
        placements=placements
    )


@pages.route("/add-client", methods=["GET", "POST"])
def add_client():
    form = AddClient()

    if form.validate_on_submit():
        new_client = Client(
            client_name=form.client_name.data,
            contact_name=form.contact_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            terms=form.terms.data,
            industry=form.industry.data,
            status="Active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        add_methods.register_client(new_client)
        return redirect(url_for(".clients"))

    return render_template(
        "add-client.html",
        title="Dashboard | Add Client",
        form=form
    )


@pages.route("/add-employee", methods=["GET", "POST"])
def add_employee():
    form = AddEmployee()

    if form.validate_on_submit():
        new_employee = Employee(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            rate_type=form.rate_type.data,
            pay_rate=form.pay_rate.data,
            bill_rate=form.bill_rate.data,
            title=form.title.data,
            status="Active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        add_methods.register_employee(new_employee)
        return redirect(url_for(".employees"))

    return render_template(
        "add-employee.html",
        title="DashBoard | Add Employee",
        form=form
    )


@pages.route("/add-job", methods=["GET", "POST"])
def add_job():
    form = AddJob()
    form.client.choices = add_methods.get_client_dropdown()

    if form.validate_on_submit():
        new_job = Job(
            client_id=int(form.client.data),
            title=form.title.data,
            staff_type=form.staff_type.data,
            location=form.location.data,
            bill_rate=form.bill_rate.data,
            pay_rate=form.pay_rate.data,
            currency=form.currency.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status="open",
            notes=form.notes.data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        add_methods.add_job(new_job)
        return redirect(url_for(".jobs"))

    return render_template(
        "add-job.html",
        title="Dashboard | Add Job",
        form=form
    )


@pages.route("/add-placement", methods=["GET", "POST"])
def add_placement():
    form = PlaceEmployee()
    form.client_role.choices = add_methods.get_job_dropdown()
    form.employee.choices = add_methods.get_employee_dropdown()

    if form.validate_on_submit():
        new_placement = Placement(
            job_id=int(form.client_role.data),
            employee_id=int(form.employee.data),
            status="Active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        add_methods.place_employee(new_placement)
        return redirect(url_for(".placements"))

    return render_template(
        "add-placement.html",
        title="Dashboard | Place Employee",
        form=form
    )


@pages.route("/client/<int:_id>", methods=["GET", "POST"])
def edit_client(_id: int):
    form = EditClient()
    client = edit_methods.get_client(_id)

    if request.method == "GET":
        form.client_name.data = client[0]
        form.contact_name.data = client[1]
        form.email.data = client[2]
        form.phone.data = client[3]
        form.address.data = client[4]
        form.terms.data = client[5]
        form.industry.data = client[6]
        form.status.data = client[7]

    if form.validate_on_submit():
        edited_client = Client(
            client_name=form.client_name.data,
            contact_name=form.contact_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            terms=form.terms.data,
            industry=form.industry.data,
            status=form.status.data,
            created_at=datetime.now(),    # Not used
            updated_at=datetime.now()
        )

        edit_methods.update_client(_id, edited_client)
        return redirect(url_for(".clients"))

    return render_template(
        "edit-client.html",
        title="Dashboard | Edit Client",
        client_id=_id,
        form=form
    )


@pages.get("/delete-client/<int:_id>")
def delete_client(_id: int):
    delete_methods.delete_client(_id)
    return redirect(url_for(".clients"))


@pages.route("/employee/<int:_id>", methods=["GET", "POST"])
def edit_employee(_id: int):
    form = EditEmployee()
    employee = edit_methods.get_employee(_id)

    if request.method == "GET":
        form.full_name.data = employee[0]
        form.email.data = employee[1]
        form.phone.data = employee[2]
        form.rate_type.data = employee[3]
        form.pay_rate.data = employee[4]
        form.bill_rate.data = employee[5]
        form.title.data = employee[6]
        form.status.data = employee[7]
    

    if form.validate_on_submit():
        edited_employee = Employee(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            rate_type=form.rate_type.data,
            pay_rate=form.pay_rate.data,
            bill_rate=form.bill_rate.data,
            title=form.title.data,
            status=form.status.data,
            created_at=datetime.now(),    # Not used
            updated_at=datetime.now()
        )

        edit_methods.update_employee(_id, edited_employee)
        return redirect(url_for(".employees"))
    
    return render_template(
        "edit-employee.html",
        title="Dashboard | Edit Employee",
        employee_id=_id,
        form=form
    )


@pages.get("/delete-employee/<int:_id>")
def delete_employee(_id: int):
    delete_methods.delete_employee(_id)
    return redirect(url_for(".employees"))


@pages.route("/job/<int:_id>", methods=["GET", "POST"])
def edit_job(_id: int):
    form = EditJob()
    form.client.choices = add_methods.get_client_dropdown()
    job = edit_methods.get_job(_id)

    if request.method == "GET":
        form.client.data = str(job[0])
        form.title.data = job[1]
        form.staff_type.data = job[2]
        form.location.data = job[3]
        form.bill_rate.data = job[4]
        form.pay_rate.data = job[5]
        form.currency.data = job[6]
        form.start_date.data = date.fromisoformat(job[7])
        form.end_date.data = date.fromisoformat(job[8])
        form.status.data = job[9]
        form.notes.data = job[10]
    
    if form.validate_on_submit():
        updated_job = Job(
            client_id=int(form.client.data),
            title=form.title.data,
            staff_type=form.staff_type.data,
            location=form.location.data,
            bill_rate=form.bill_rate.data,
            pay_rate=form.pay_rate.data,
            currency=form.currency.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            notes=form.notes.data,
            created_at=datetime.now(),    # Not used
            updated_at=datetime.now()
        )

        edit_methods.update_job(_id, updated_job)
        return redirect(url_for(".jobs"))
    
    return render_template(
        "edit-job.html",
        title="Dashboard | Edit Job",
        job_id=_id,
        form=form
    )


@pages.get("/delete-job/<int:_id>")
def delete_job(_id: int):
    delete_methods.delete_job(_id)
    return redirect(url_for(".jobs"))


@pages.route("/placement/<int:_id>", methods=["GET", "POST"])
def edit_placement(_id: int):
    form = EditPlacement()
    form.client_role.choices = add_methods.get_job_dropdown()
    form.employee.choices = add_methods.get_employee_dropdown()
    placement = edit_methods.get_placement(_id)

    if request.method == "GET":
        form.client_role.data=str(placement[0])
        form.employee.data=str(placement[1])
        form.status.data=placement[2]
    

    if form.validate_on_submit():
        updated_placement = Placement(
            job_id=int(form.client_role.data),
            employee_id=int(form.employee.data),
            status=form.status.data,
            created_at=datetime.now(),    # Not used
            updated_at=datetime.now()
        )

        edit_methods.update_placement(_id, updated_placement)
        return redirect(url_for(".placements"))

    return render_template(
        "edit-placement.html",
        title="Dashboard | Edit Placement",
        placement_id=_id,
        form=form
    )


@pages.get("/delete-placement/<int:_id>")
def delete_placement(_id: int):
    delete_methods.delete_placement(_id)
    return redirect(url_for(".placements"))


# Test Commitments