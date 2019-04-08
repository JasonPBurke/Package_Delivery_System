# Jason Burke #000940322

from QuadraticProbingHashTable import EmptyBucket
from LoadAndDeliverPackages import deliver_packages
import LoadPackageFile as lp
import LoadDistanceTable as ld
from datetime import datetime, time


# load the package data from the WGUPS excel package file.
# This data is a list of dictionary objects, each one representing
# a single package with all package delivery info included.
hash_table = lp.load_package_data()

# Load the distance info from the excel spreadsheet into a graph object.
# Returned data is the graph object and the hub vertex(starting vertex).
distance_graph, hub_vertex = ld.load_distance_table()

# This list of all packages will be used to control the delivery loop 
# in the deliver_packages function
todays_packages = hash_table.search_by(lambda pkg: type(pkg) is not EmptyBucket and pkg.delivery_status == 'At HUB')

# Get a list of the package objects that have the earliest delivery times.
deliver_first = hash_table.search_by(lambda pkg: pkg.delivery_deadline < datetime.strptime('12:00PM', '%I:%M%p').time())

# Call deliver_packages to load and deliver packages.  
deliver_packages(todays_packages, hash_table, distance_graph, hub_vertex, deliver_first)
