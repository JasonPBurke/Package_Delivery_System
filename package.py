from datetime import time

# Create a Package object class to store package data recieved by the hash table.
class Package:
    
    def __init__(self, id_num, address, delivery_deadline, 
                 city, zip_code, weight, notes, delivery_status):

        self.id_num = id_num
        self.address = address
        self.delivery_deadline = delivery_deadline
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.delivery_status = delivery_status
        self.notes = notes # if no special notes, will be None
        self.delivery_time = None

    def __str__(self):

        return (f'\n\n---Package info---\n\nPackage ID: {self.id_num}\nAddress: {self.address}'
                + f'\nCity:{self.city}\nZip Code: {self.zip_code}\nWeight: {self.weight}\nSpecial Notes: {self.notes}'                                                                       
                + f'\nDelivery Deadline: {str(self.delivery_deadline)}\nDelivery Time: {self.delivery_time}'
                + f'\nDelivery Status: {self.delivery_status}')

    def __repr__(self):
        return str(self.id_num)
                                                                                
    # This is used to change the delivery status of a package
    # from 'At HUB' to 'In route' and/or 'Delivered'.
    # Could change this to take an int in (1,2) and auto assign
    # to the two options.  This would eliminate the need to control
    # for spelling/ what is actually entered by the user. Or just send
    # the correct string yourself after user chooses their option.<-----
    def change_package_status(self, delivery_status):
        self.delivery_status = delivery_status

    def change_address(self, new_address, new_city, new_zip):
        self.address = new_address
        self.city = new_city
        self.zip_code = new_zip

    def set_delivery_time(self, time):
        self.delivery_time = time.time()

    def get_delivery_time(self):
        return self.delivery_time