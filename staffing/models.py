from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class Client:
    client_name: str
    contact_name: str
    email: str
    phone: str
    address: str
    terms: str
    industry: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Employee:
    full_name: str
    email: str
    phone: str
    rate_type: str
    pay_rate: float
    bill_rate: float
    title: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Job:
    client_id: int
    title: str
    staff_type: str
    location: str
    bill_rate: float
    pay_rate: float
    currency: str
    start_date: date
    end_date: date
    staff_needed: int
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Placement:
    job_id: int
    employee_id: int
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Invoice:
    invoice_no: str
    contact_name: str
    contact_email: str
    contact_phone: str
    billing_address: str
    issue_date: str
    due_date: str
    terms: str
    status: str
    currency: str
    subtotal: float
    tax_amount: float
    total: float
    amt_paid: float
    balance: float
    invoice_items: list