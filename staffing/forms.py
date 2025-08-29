from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, SubmitField
from wtforms.validators import InputRequired, Email


class AddClient(FlaskForm):
    client_name = StringField("Client Name", validators=[InputRequired()])
    contact_name = StringField("Person to Contact")
    email = StringField("Contact Email", validators=[Email()])
    phone = StringField("Contact Number", render_kw={"placeholder": "+1 (234) 567-8910"})
    address = StringField("Billing Address")
    terms = StringField("Billing Terms", validators=[InputRequired()], default="Net 30")
    industry = StringField("Industry")

    submit = SubmitField("Add Client")


class AddEmployee(FlaskForm):
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

    submit = SubmitField("Add Employee")


class AddJob(FlaskForm):
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
    notes = StringField("Notes")

    submit = SubmitField("Add Job")


class PlaceEmployee(FlaskForm):
    client_role = SelectField("Client - Position")
    employee = SelectField("Employee")

    submit = SubmitField("Place Employee")



class EditClient(FlaskForm):
    client_name = StringField("Client", validators=[InputRequired()])
    contact_name = StringField("Person to Contact")
    email = StringField("Contact Email", validators=[Email()])
    phone = StringField("Contact Number", render_kw={"placeholder": "+1 (234) 567-8910"})
    address = StringField("Billing Address")
    terms = StringField("Billing Terms", validators=[InputRequired()])
    industry = StringField("Industry")
    status = SelectField("Status", choices=[
        ("Active", "Active"),
        ("Inactive", "Inactive")
    ])

    submit = SubmitField("Save Changes")


class EditEmployee(FlaskForm):
    full_name = StringField("Name", validators=[InputRequired()])
    email = StringField("Email", validators=[Email()])
    phone = StringField("Phone Number", render_kw={"placeholder": "+1 (234) 567-8910"})
    rate_type = SelectField("Rate Type", choices=[
        ("hourly", "Hourly"),
        ("salary", "Salary")
    ])
    pay_rate = DecimalField("Default Pay Rate")
    bill_rate = DecimalField("Default Bill Rate")
    title = StringField("Role Title")
    status = SelectField("Status", choices=[
        ("Active", "Active"),
        ("Standby", "Standby")
    ])

    submit = SubmitField("Save Changes")


class EditJob(FlaskForm):
    client = SelectField("Client")
    title = StringField("Job Position", validators=[InputRequired()])
    staff_type = SelectField("Staff Type", choices=[
        ("Contractor", "Contractor"),
        ("Temp", "Temp"),
        ("FTE", "FTE"),
        ("Temp-to-Hire", "Temp-to-Hire")
    ])
    location = StringField("Location")
    bill_rate = DecimalField("Bill Rate")
    pay_rate = DecimalField("Pay Rate")
    currency = StringField("Currency")
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    status = SelectField("Status", choices=[
        ("open", "Open"),
        ("filled", "Filled"),
        ("closed", "Closed")
    ])
    notes = StringField("Notes")

    submit = SubmitField("Save Changes")


class EditPlacement(FlaskForm):
    client_role = SelectField("Client - Position")
    employee = SelectField("Employee")
    status = SelectField("Status", choices=[
        ("Active", "Active"),
        ("Ended", "Ended")
    ])

    submit = SubmitField("Save Changes")