from models.model1 import db, Services, Shop, Employee, ProvidedServices, Customer, Order, Invoice, WorkingTime
from datetime import datetime, time

def create_tables():
    db.create_tables([Services, Shop, Employee, ProvidedServices])
    print('done')

def show_table_status():
    imported_tables= [Services, Shop, Employee, ProvidedServices]
    for _class in imported_tables:
        print(_class.id)



class ServiceUsage:

    @staticmethod
    def all_services_name():
        q= Services.select()
    
        return [i.service_name for i in q ]

    @staticmethod
    def add_service(name, price, group, description):
        Services.create(service_name= name, price= price,
                         group_name= group,
                           description= description)

    @staticmethod
    def remove_service(name):
        Services.delete().where(Services.service_name== name).execute()

    @staticmethod
    def update_service_base_on_name(old_name, new_name):
        (Services.update(service_name= new_name)
        .where(Services.service_name== old_name)
        .execute())

    

class EmployeeUsage:

    @staticmethod
    def get_all_employee_brif_info():
        q= Employee.select()
        names= [i.name for i in q]
        natioanal_code= [i.nationalcode for i in q]
        return names, natioanal_code
    
    @staticmethod
    def get_employee_by_name(name):
        q= Employee.select().where(Employee.name== name)
        return [i for i in q]

    @staticmethod
    def add_employee(name, nationalcode, mobile,  status, salary, username, password, join_date= datetime.now, ):
        emp= Employee()
        password_hashed= emp.set_password(password)
        emp.create(name= name, nationalcode= nationalcode, mobile= mobile,
                    status= status,salary= salary,
                     username= username)
        emp.set_password(password)
        emp.save()
        return emp

    @staticmethod
    def edit_employee_information(nationalcode, **fields):
        if not fields:
            return None
        return (Employee.update(**fields)
                .where(Employee.nationalcode == nationalcode)
                .execute())

    @staticmethod
    def remove_employee(nationalcode):
        return Employee.delete().where(Employee.nationalcode == nationalcode).execute()

    @staticmethod
    def shift_hour(natinalcode, login, logout):
        emp= Employee.get(Employee.nationalcode == natinalcode)

        try:
            rec= WorkingTime(
                employee_nationalcode=emp,
                login=login,
                logout=logout,
                )
            rec.save()
        except Exception as e:
            return e
class CustomerUsage:
    @staticmethod
    def get_all_customers():
        names= Customer.select(Customer.name)
        natioalcodes= Customer.select(Customer.nationalcode)
        mobile= Customer.select(Customer.mobile)
        return names, natioalcodes, mobile

    @staticmethod
    def get_customer_by_nationalcode(nationalcode):
        q= Customer.select().where(Customer.nationalcode== nationalcode).first()
        return q

    @staticmethod
    def add_customer(nationalcode, name, mobile):
        Customer.create(name= name, nationalcode= nationalcode, mobile= mobile)

    @staticmethod
    def edit_info_customer(nationlcode, **fields):
        if not fields:
                    return 0
        return (Customer.update(**fields)
                .where(Customer.nationalcode == nationlcode)
                .execute())

    @staticmethod
    def remove_customer(nationalcode):
        return Customer.delete().where(Customer.nationalcode == nationalcode).execute()

class ShopUsage:
    @staticmethod
    def get_all_shops():
        return [s for s in Shop.select()]
 
    @staticmethod
    def add_shop(name, address, postcode):
        return Shop.create(name=name, address=address, postcode=postcode)
 
    @staticmethod
    def edit_shop(shop_id, **fields):
        return Shop.update(**fields).where(Shop.id == shop_id).execute()
 
    @staticmethod
    def remove_shop(shop_id):
        return Shop.delete().where(Shop.id == shop_id).execute()

class Counter:

    @staticmethod
    def get_all_factors():
        return [f for f in Invoice.select()]
 
    @staticmethod
    def get_selected_factor(factor_id):
        return Invoice.get_or_none(Invoice.id == factor_id)

    @staticmethod
    def add_factor():
        pass

    @staticmethod
    def edit_factor():
        pass

class OrderUsage:

    @staticmethod
    def get_all_orders():
        return [o for o in Order.select()]

    @staticmethod
    def delete_an_order(id):
        Order.delete().where(Order.id== id).execute()

    @staticmethod
    def get_order_base_on_id(order_id):
        q= Order.select().where(Order.ordrer_id== order_id).first()
        return [i for i in q]