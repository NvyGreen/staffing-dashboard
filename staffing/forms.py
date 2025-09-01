from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email


class ClientForm(FlaskForm):
    client_name = StringField("Client Name", validators=[InputRequired()])
    contact_name = StringField("Person to Contact")
    email = StringField("Contact Email", validators=[Email()])
    phone = StringField("Contact Number", render_kw={"placeholder": "+1 (234) 567-8910"})
    address = StringField("Billing Address")
    terms = StringField("Billing Terms", validators=[InputRequired()], default="Net 30")
    industry = StringField("Industry")

    submit = SubmitField("Save Client")


class EmployeeForm(FlaskForm):
    full_name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[Email()])
    phone = StringField("Phone Number", render_kw={"placeholder": "+1 (234) 567-8910"})
    rate_type = SelectField("Rate Type", choices=[
        ("hourly", "Hourly"),
        ("salary", "Salary")
    ])
    pay_rate = DecimalField("Default Pay Rate", default=0.0)
    bill_rate = DecimalField("Default Bill Rate", default=0.0)
    title = StringField("Role Title")

    submit = SubmitField("Save Employee")


class JobForm(FlaskForm):
    client = SelectField("Client")
    title = StringField("Job Position", validators=[InputRequired()])
    staff_type = SelectField("Staff Type", choices=[
        ("Contractor", "Contractor"),
        ("Temp", "Temp"),
        ("FTE", "FTE"),
        ("Temp-to-Hire", "Temp-to-Hire")
    ])
    location = StringField("Location")
    bill_rate = DecimalField("Bill Rate", default=0.0)
    pay_rate = DecimalField("Pay Rate", default=0.0)
    currency = StringField("Currency", default="USD")
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    staff_needed = IntegerField("# of Positions", default=1)
    notes = StringField("Notes")

    submit = SubmitField("Save Job")


class PlacementForm(FlaskForm):
    client_role = SelectField("Client - Position")
    employee = SelectField("Employee")

    submit = SubmitField("Save Placement")


class InvoiceSelect(FlaskForm):
    client = SelectField("Client", choices=[
        (0, " ")
    ])
    
    submit = SubmitField("See Invoice")