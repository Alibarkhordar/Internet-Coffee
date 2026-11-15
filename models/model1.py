from peewee import (SqliteDatabase, Model, ForeignKeyField, TextField, CharField, 
                    FloatField, DateField, IntegerField, SmallIntegerField, DateTimeField, TimeField)
import bcrypt
from datetime import datetime, date, timedelta

db= SqliteDatabase('price_and_job.db')

class BaseModel(Model):

    class Meta:
        database= db

    def __str__(self):
        return str(self.id)

class Services(BaseModel):
    service_name= CharField(max_length=256, null= False)
    price= IntegerField(null= False)
    group_name= CharField(max_length=256, null= False)
    description= TextField()

    def save(self, *args, **kwargs):
        if self.price < 0:
            raise ValueError("price cant be negetive")
        return super().save(*args, **kwargs)

class Shop(BaseModel):
    name= CharField(max_length=256, null= False)
    address= TextField(null= False)
    postcode= IntegerField(null= False)

class Employee(BaseModel):
    name= CharField(max_length=256, null= False)
    nationalcode= CharField(max_length=10, unique= True, null= False)
    mobile= CharField(max_length=11)
    join_date= DateField()
    status = SmallIntegerField(null=False, choices=[
        (0, 'inactive'),
        (1, 'active'),
        (2, 'on_leave'),
        (3, 'terminated'),
    ])
    salary= IntegerField(null= False,)
    username= CharField(default= 'a123456', null= False, unique= True)
    _password_hash= CharField(max_length= 60, null= False) # TODO: lengh of the password will be set at enterence
    working_place= ForeignKeyField(Shop, backref= 'employees')

    def save(self, *args, **kwargs):
            if self.salary < 0:
                raise ValueError("salary cant be negetive", "حقوق نمی‌تواند منفی باشد.")
            return super().save(*args, **kwargs)

    def check_password(self, raw_password: str)-> bool:
        return bcrypt.checkpw(raw_password.encode('utf-8'), self._password_hash.encode('utf-8'))

    def set_password(self, raw_password: str):
        """Hash the password (bcrypt, 60 chars) and store it on the instance.
            hash password and save it"""
        hashed= bcrypt.hashpw(raw_password.encode('UTF-8', bcrypt.gensalt()))
        self._password_hash= hashed.decode('UTF-8')

    @classmethod
    def authorization(cls, username, password):
        emp= cls.select().where(cls.username== username).first()
        if emp and emp.check_password(password):
            return emp
        return None

class Customer(BaseModel):
    name= CharField(max_length= 250)
    nationalcode= CharField(max_length= 10, unique= True)
    mobile= CharField(max_length= 11)

class ProvidedServices(BaseModel):
    service= ForeignKeyField(Services, backref='provides')
    employee= ForeignKeyField(Employee, backref='provides')
    customer= ForeignKeyField(Customer, backref='provides')
    create_at= DateTimeField(default= datetime.now, null= False)


class Payment(BaseModel):
    time= DateTimeField(default= datetime.now)
    price= IntegerField(null= False)
    payment_method= CharField(choices=[('cash','cash'), ('card','card')])
    providingservice= ForeignKeyField(ProvidedServices, backref='payments')

class Order(BaseModel):
    ordrer_id= IntegerField(null= False, primary_key= True)
    providedservice= ForeignKeyField(ProvidedServices, backref= 'orders')
    created_time= DateTimeField(default= datetime.now)

class WorkingTime(BaseModel):
    employee_nationalcode= ForeignKeyField(Employee, null=False, backref= 'times')
    login= TimeField(null=False)
    logout= TimeField(null=False)
    work_hour= FloatField(null= True)

    
    def save(self, *arg, **kwargs):
        if self.login and self.logout:
            today= date.today()
            start= datetime.combine(today, self.login)
            end= datetime.combine(today, self.logout)
            if end < start: #for night shifts
                end += timedelta(days=1)
            
            self.work_hour= (self.logout- self.login)/ 3600
        return super().save(*arg, **kwargs)

class Invoice(BaseModel):
    number= IntegerField(unique= True, null= False)
    customer= ForeignKeyField(Customer, backref='invoices')
    shop= ForeignKeyField(Shop, backref='invoices')
    created_at= DateTimeField(default= datetime.now)
    discount= IntegerField(default=0)
    note= TextField(default= '')
    voided_at= DateTimeField(null= True)

class InvoiceLine(BaseModel):
    invoice= ForeignKeyField(Invoice, backref='lines', on_delete='CASCADE')
    service= ForeignKeyField(Services, null=True, backref='invoice_line', on_delete='SET NULL')
    title= CharField(max_length=256)
    until_pricce= IntegerField()
    quantity= IntegerField(default=1)
    employee= ForeignKeyField(Employee, null=True, backref='invoice_line', on_delete='SET NULL')
    
    def save(self, *args, **kwargs):
        if self.quantity < 1:
            raise ValueError("تعداد باید حداقل ۱ باشد.", "list number of quantity is 1")
        if self.until_pricce < 0:
            raise ValueError("قیمت نمی‌تواند منفی باشد.", 'price can not be negetive')
        return super().save(*args, **kwargs)
class Payment(BaseModel):
    invoice = ForeignKeyField(Invoice, backref='payments')
    amount = IntegerField(null=False)
    method = CharField(max_length=16, choices=[('cash', 'cash'), ('card', 'card'), ('transfer', 'transfer')])
    paid_at = DateTimeField(default=datetime.now)
    reference = CharField(max_length=64, default='')         # card/transfer tracking number

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError("مبلغ پرداخت باید بیشتر از صفر باشد.", "the payment must be more than zero")
        return super().save(*args, **kwargs)

