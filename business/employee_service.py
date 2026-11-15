from datetime import datetime

from peewee import IntegrityError, fn

from models.model2 import Employee, Salary, ShiftTime, SalaryIncome
from jalali_date import jnow, jtoday

def _get_employee(nationalcode):
    ''' return employee model
     to get an employee with nationalcode'''
    emp= Employee.get_or_none(Employee.nationalcode == nationalcode)
    if emp is None:
        raise ValueError('No employee with nationalcode {}'.format(nationalcode))
    return emp

def create_employee(first_name, last_name, email, phone_number):
    ''' add employee in feature only admin or manager level user can add an employee'''
    employee = Employee()
    employee.first_name = first_name
    employee.last_name = last_name
    employee.email = email
    employee.phone_number = phone_number
    try:
        employee.create()
    except IntegrityError as e:
        return e
    return employee

def update_employee(nationalcode, first_name, last_name, email, phone_number):
    '''edit employee with nationalcode because nationalcode is uniq for evry employee'''
    emp= Employee.select().where(Employee.nationalcode == nationalcode)
    assert isinstance(phone_number, object)
    emp.update(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)

def delete_employee(nationalcode):
    ''' employee with expected nationalcode will be deleted
    must be admin level user for employee to delete'''
    Employee.delete().where(Employee.nationalcode == nationalcode)

def get_employee(nationalcode):
    ''' general information of an expected employee '''
    emp= Employee.select().where(Employee.nationalcode == nationalcode)
    info= [i for i in emp]
    return info

def shift_time_checkin(nationalcode, checkin = jnow()):
    emp= _get_employee(nationalcode)
    now= jnow()
    checkin= checkin or now

    open_shift= (ShiftTime.select()
                 .where(ShiftTime.emp== emp, ShiftTime.checkin == now, ShiftTime.checkout.is_null())
                 .first()
                 )
    if open_shift:
        raise ValueError(f'current shift for <<{nationalcode}>> already exists')
    return ShiftTime.create(emp=emp, checkin=checkin, date= jtoday())

def shift_time_checkout(nationalcode, checkout):
    emp = _get_employee(nationalcode)
    now= jnow()
    checkout= checkout or now

    shift = (ShiftTime.select()
             .where(ShiftTime.emp == emp,
                    ShiftTime.checkout.is_null())
             .order_by(ShiftTime.date.desc(), ShiftTime.checkout.desc())
             .first())
    if shift is None:
        raise ValueError(f'current shift for <<{nationalcode}>> already exists')
    return ShiftTime.create(emp=emp, checkin=checkout, date= jtoday())

def shift_calculate(nationalcode):
    emp= _get_employee(nationalcode)
    query= (ShiftTime.select(ShiftTime.emp, fn.MIN(ShiftTime.checkin), fn.MAX(ShiftTime.checkout))
            .where(ShiftTime.emp == emp).group_by(ShiftTime.date).get()
            )

    total_seconds= 0
    for shift_date, first_check, last_check in query:
        if first_check is None or last_check is None:
            continue
        start= datetime.combine(shift_date, first_check)
        end= datetime.combine(shift_date, last_check)
        total_seconds += (end - start).total_seconds()

    total= round(total_seconds/3600, 2)
    shift= ShiftTime()
    shift.total= total
    shift.save()

def shift_calculation_range(nationalcode, start_data, end_data):
    emp= _get_employee(nationalcode)
    query= (ShiftTime.select(fn.COALESCE(fn.SUM(ShiftTime.total_work_hour)))
            .where(ShiftTime.emp == emp, ShiftTime.date.between(start_data, end_data))
            )
    return query.scalar()

def add_incomes(nationalcode, incomes: dict[str, int]):
    emp= _get_employee(nationalcode)
    SalaryIncome.insert_many(incomes).where('' == emp)