from datetime import time

class Truck:

    def __init__(self, truck_id, delivery_miles = 0, driver = None):

        self.truck_id = truck_id
        self.delivery_miles = delivery_miles
        self.driver = driver
        self.package_list = []
        self.return_to_hub = False
        self.at_hub = True
        self.start_time = None
        self.pkg_and_edge_distance = []
        self.miles_traveled = 0
        self.hub_to_next_stop_miles = 0
        self.time_back_to_hub = None

    def __str__(self):
        return str(self.truck_id)
        

    def add_package(self, package):
        self.package_list.append(package)

    def remove_package(self, package):
        self.package_list.remove(package)

    def show_packages(self):
        return [p.id_num for p in self.package_list]

    def set_driver(self, driver):
        self.driver = driver

    def add_miles(self, miles_to_add):
        self.delivery_miles += miles_to_add

    def get_miles(self):
        return round(self.delivery_miles, 1)

    def get_truck_id(self):
        return self.truck_id

    def set_return_to_hub(self, val):
        self.return_to_hub = val

    def set_start_time(self, val):
        self.start_time = val

    def add_edge_info(self, val):
        self.pkg_and_edge_distance.append(val)

    def get_edge_info(self):
        return self.pkg_and_edge_distance

    def add_miles_traveled(self, val):
        self.miles_traveled += val

    def get_miles_traveled(self):
        return self.miles_traveled

    def add_hub_to_next_stop_miles(self, val):
        self.hub_to_next_stop_miles += val

    def get_hub_to_next_stop_miles(self):
        return self.hub_to_next_stop_miles

    def set_at_hub(self, val):
        self.at_hub = val

    def set_clock_time_at_hub_return(self, time):
        self.time_back_to_hub = time.time()