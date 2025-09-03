from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request
)
from staffing.forms import (
    ClientForm,
    EmployeeForm,
    JobForm,
    PlacementForm,
    InvoiceSelect
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
import staffing.invoice_methods as invoice_methods
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
    form = ClientForm()

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
    form = EmployeeForm()

    if form.validate_on_submit():
        new_employee = Employee(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            rate_type=form.rate_type.data,
            pay_rate=form.pay_rate.data,
            bill_rate=form.bill_rate.data,
            title=form.title.data,
            status="Standby",
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
    form = JobForm()
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
            staff_needed=form.staff_needed.data,
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
    form = PlacementForm()
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
    form = ClientForm()
    client = edit_methods.get_client(_id)

    if request.method == "GET":
        form.client_name.data = client[0]
        form.contact_name.data = client[1]
        form.email.data = client[2]
        form.phone.data = client[3]
        form.address.data = client[4]
        form.terms.data = client[5]
        form.industry.data = client[6]

    if form.validate_on_submit():
        edited_client = Client(
            client_name=form.client_name.data,
            contact_name=form.contact_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            terms=form.terms.data,
            industry=form.industry.data,
            status="Active",              # Not used
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
    form = EmployeeForm()
    employee = edit_methods.get_employee(_id)

    if request.method == "GET":
        form.full_name.data = employee[0]
        form.email.data = employee[1]
        form.phone.data = employee[2]
        form.rate_type.data = employee[3]
        form.pay_rate.data = employee[4]
        form.bill_rate.data = employee[5]
        form.title.data = employee[6]
    

    if form.validate_on_submit():
        edited_employee = Employee(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            rate_type=form.rate_type.data,
            pay_rate=form.pay_rate.data,
            bill_rate=form.bill_rate.data,
            title=form.title.data,
            status="Standby",             # Not used
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
    form = JobForm()
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
        form.staff_needed.data = job[9]
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
            staff_needed=form.staff_needed.data,
            status="open",                # Not used
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
    form = PlacementForm()
    form.client_role.choices = add_methods.get_job_dropdown()
    form.employee.choices = add_methods.get_employee_dropdown()
    placement = edit_methods.get_placement(_id)

    curr_job = edit_methods.get_current_job_option(placement[0])
    if curr_job not in form.client_role.choices:
        form.client_role.choices.append(curr_job)
    form.employee.choices.append(edit_methods.get_current_employee_option(placement[1]))

    if request.method == "GET":
        form.client_role.data=str(placement[0])
        form.employee.data=str(placement[1])
    

    if form.validate_on_submit():
        updated_placement = Placement(
            job_id=int(form.client_role.data),
            employee_id=int(form.employee.data),
            status="Active",              # Not used
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


@pages.route("/invoice")
def invoices():
    invoice_methods.generate_invoice_items(2)

    form = InvoiceSelect()
    form.client.choices += add_methods.get_client_dropdown()

    return render_template(
        "invoices.html",
        title="Dashboard | Invoices",
        form=form
    )