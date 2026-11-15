from datetime import datetime

import bcrypt
from peewee import (SqliteDatabase, CharField, DateTimeField, Model, IntegerField
, TextField, ForeignKeyField, SmallIntegerField, TimeField, DateField, BigIntegerField)

from business.jalali_date import jtoday

db= SqliteDatabase('db.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Service(BaseModel):
    service_name = CharField(max_length=256, null=False)
    price = IntegerField(null=False)
    group_name = CharField(max_length=256, null=False)
    description = TextField()

    def save(self, *args, **kwargs):
        if self.price <= 0:
            raise ValueError('Price must be greater than 0')
        super(Service, self).save(*args, **kwargs)

class Shop(BaseModel):
    pass

class Employee(BaseModel):
    EMPLOYEE_STATUS= [(0, 'inactive'), (1, 'active'), (2, 'on_leave'), (3, 'terminated')]

    first_name = CharField(max_length=256, null=False)
    status= SmallIntegerField(choices=EMPLOYEE_STATUS)
    last_name = CharField(max_length=256, null=False)
    nationalcode= CharField(max_length=256, null=False)
    phone = CharField(max_length=256, null=False)
    email = CharField(max_length=256, null=False)
    joined_date = DateTimeField(null=False, default=datetime.now)
    username = CharField(max_length=256, null=False)
    _password_hash = CharField(max_length=60, null=False)


    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'


    def hashed_password(self):
        """Hash the password (bcrypt, 60 chars) and store it on the instance."""
        hashed= bcrypt.hashpw(self._password_hash.encode('utf-8'), bcrypt.gensalt())
        self._password_hash = hashed.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(self._password_hash.encode('utf-8'), password.encode('utf-8'))

    @classmethod
    def authorization(cls, username, password):
        emp= cls.select().where(cls.username== username).first()
        if emp and emp.check_password(password):
            return emp
        return None

class ShiftTime(BaseModel):
    emp= ForeignKeyField(Employee, null=False, on_delete= 'CASCADE', backref='shift_times')
    date = DateField(null=False)
    checkin= TimeField()
    checkout= TimeField()
    total_work_hour= TimeField()

class Salary(BaseModel):
    employee = ForeignKeyField(Employee, on_delete= 'CASCADE', backref='salaryes')
    base_income = BigIntegerField()
    year = IntegerField()
    month = IntegerField()

    class Meta:
        indexes = (('employee', 'year', 'month'), True)

class SalaryIncome(BaseModel):
    salary = ForeignKeyField(Salary, on_delete= 'CASCADE', backref='increment_salary')
    shift_hour= ForeignKeyField(ShiftTime, on_delete= 'CASCADE', backref='shift_hours')
    increment= BigIntegerField()
    reason = TextField()

class SalaryDecrement(BaseModel):
    salary = ForeignKeyField(Salary, on_delete= 'CASCADE', backref='salary_decrement')
    decrement= BigIntegerField()
    reason = TextField()

    
class Customer(BaseModel):
    name = CharField(max_length=250)
    nationalcode = CharField(max_length=10, unique=True)
    mobile = CharField(max_length=11)

class CustomInvoice(BaseModel):
    employee= ForeignKeyField(Employee, on_delete= 'CASCADE', backref='invoice')
    customer = ForeignKeyField(Customer, on_delete= 'CASCADE', backref='invoice')
    inserted_date = DateTimeField(null=False, default=datetime.now)
    items= ForeignKeyField(Service, on_delete= 'CASCADE', backref='invoices')


class GeneralInvoice(BaseModel):
    employee= ForeignKeyField(Employee, on_delete= 'CASCADE', backref='invoice')
    inserted_date = DateTimeField(null=False, default=datetime.now)
    items = ForeignKeyField(Service, on_delete='CASCADE', backref='invoices')