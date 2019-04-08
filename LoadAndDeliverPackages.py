# Jason Burke

from QuadraticProbingHashTable import EmptyBucket
from interface import interface
from truck import Truck
from datetime import datetime, time, timedelta

# This greedy algorithm will find the closest vertex from our starting hub vertex(WGU)
# and add the package(s) to the first truck that are to be delivered there.
# We add the package(s) for that vertex, and continue this process
# until the truck has at most 16 packages on it to deliver. Then fill the next 
# truck to at most 16 and so on until all packages have been loaded/delivered.

# This method takes graph and truck objects a starting vertex, the current_time,
# any packages that must be delivered first in a list, and an empty list to hold
# all packages when they are loaded to a truck.  It loads packages onto a truck 
# object and returns the miles that will need to be traveled to deliver the packages
# on time and with consideration to the special notes for the packages.      

## Big O: This function has a O(n*p*pkg) time
def load_truck(hash_table, graph, truck, start_vertex, current_time, deliver_first, packages_loaded):
    
    # This assumes that all packages to a specific destination are loaded on the same
    # truck and at the same time.  When this is not the case, the flag is changed to
    # True further below.
    visit_vertex_again = False

    # Base case for recursion
    if not start_vertex:
        return 0

    # THIS GETS ME A DICT OF ALL THE EDGES AND THEIR WEIGHTS FOR THE CURRENT VERTEX
    # CAN USE THIS TO DETERMINE THE NEXT PACKAGE STOP.  THEN ADD THE PACKAGES FOR THAT
    # STOP TO THE TRUCK TILL IT HAS AT MOST 16 PACKAGES ON IT.
    edge_dict = {}
    for key, value in graph.edge_weights.items():
        
        if start_vertex is key[0]:
            edge_dict[key[1]] = value

    ## O(n*p*pkg) time
    for vertex, edge_distance in sorted(edge_dict.items(), key=lambda kv: kv[1]):
        
        # Check if deliver_first has any packages in it, if it does, check if the
        # current vertex.address matches any packages in the deliver_first list.
        #  If the address doesnt match, continue to the next vertex and check again.
        if deliver_first:

            # first_pkg = deliver_first[0] #### this would be used if I want to take the earliest 
            # package delivery and deliver it first ##### should not have to do this...it balloons 
            # my milage by 20%-30%!!!!!
            if vertex.address[0] not in [i.address for i in deliver_first]:#!= first_pkg.address: #  
                continue
            else:
                # the addresses match so remove the address-matched item from deliver_first for the next loop 
                for p in deliver_first:
                    if vertex.address[0] == p.address:
                        deliver_first.remove(p)
                        # print('\nDeliver_first after removing package:', deliver_first)
            

        # Find all packages to be delivered to the current vertex address
        same_address_packages = hash_table.search_by(lambda pkg: pkg.address == vertex.address[0] and pkg.delivery_status == 'At HUB')

                                                   
        # Here we are checking to see if the package needs to be on a specific truck, and checking
        # if the current truck is that specified truck.  We remove it from the list if it does not 
        # belong on the current truck.
        deliver_with_pkgs = []
        if same_address_packages:
            for p in same_address_packages:
                # if there are special notes and the note is for a sepecified truck and the current
                # truck is NOT the truck the package must be on, remove that package from
                # from same_address_packages and check the next one
                if p.notes and p.notes[0] == 'specified_truck' and int(p.notes[1]) != truck.get_truck_id():
                    # print(f'Package {p.id_num} must be on truck {p.notes[1]} and not on {truck.get_truck_id()} (current truck).')
                    # Specified truck does not match current truck so dont add this package to truck
                    same_address_packages.remove(p)
                    # We will need to visit this vertex again
                    visit_vertex_again = True
                # Create a list holding any packages that need to be on the same truck as the current package
                # These will be added to the truck further below
                if p.notes and p.notes[0] == 'deliver_with':
                    deliver_with_pkgs.append(hash_table.search_by_id(p.notes[1][0]))
                    deliver_with_pkgs.append(hash_table.search_by_id(p.notes[1][1]))

                if p.notes and p.notes[0] == 'flight_delay' and current_time < p.notes[1]:
                    same_address_packages.remove(p)
                    # We will need to visit this vertex again
                    visit_vertex_again = True

                if p.notes and p.notes[0] == 'wrong_address' and current_time < p.notes[1]:
                    same_address_packages.remove(p)

        
        # Skip any vertex that has been visited already
        if vertex.visited:
            continue

        # CHECK VALID PACKAGES FOR THE TRUCK HERE (ALL SPECIAL NOTES)
        if not same_address_packages:
            continue
            
        # If the current number of pkgs on truck + the number of pkgs in same_address_packages
        # totals no more than 16, then add the packages from same_address_packages to the truck.
        if len(truck.package_list) + len(same_address_packages) + len(deliver_with_pkgs) <= 14:
               
            print(f'\nDistance from {start_vertex} to {vertex} is:', edge_distance)   
            print(f'\nTrying to add package(s) {same_address_packages, deliver_with_pkgs} to truck {truck.truck_id} for current location: {vertex} \n')


            # Add the packages to be delivered to the current address to the truck
            ## O(p) time
            for p in same_address_packages:
                # if p.id_num in packages_loaded: print(f'Rejecting Package {p.id_num} b/c in packages_loaded already(2).')
                if p.id_num not in packages_loaded:
                    p.change_package_status('In route')
                    truck.add_package(p)
                    truck.add_miles(edge_distance / len(same_address_packages)) #len(same_address_packages))
                    print('Current miles:', truck.get_miles())
                    packages_loaded.append(p.id_num)
            pkg_and_edge_distance = [len(same_address_packages), edge_distance]
            truck.add_edge_info(pkg_and_edge_distance)

            # Mark current vertex as visited
            if not visit_vertex_again:
                vertex.vertex_visited(True)

            # If there is a package to this address that must be on the truck with other pkgs, add them
            if deliver_with_pkgs:
                ## O(pkg) time
                for pkg in deliver_with_pkgs:
                    
                    if pkg.id_num not in packages_loaded:
                        # Get the vertex that the current pkg is to be delivered to
                        next_vertex = graph.get_vertex_by_address(pkg.address)
                        # Get the edge_distance between vertex and next_vertex
                        edge_distance = graph.get_edge_weight(vertex, next_vertex)
                        # Add the package to the truck
                        truck.add_package(pkg)
                        pkg_and_edge_distance = [1, edge_distance]
                        truck.add_edge_info(pkg_and_edge_distance)
                        # Change pkg status
                        pkg.change_package_status('In route')
                        # Add the milage to the truck
                        truck.add_miles(edge_distance)
                        # Add pkg to packages_loaded
                        packages_loaded.append(pkg.id_num)
                        # Remove the current pkg from the deliver_with_pkgs list
                        deliver_with_pkgs.remove(pkg)
                        # Mark current vertex as visited
                        if not visit_vertex_again:
                            vertex.vertex_visited(True)
                        # Set vetex to next_vertex to calculate info for the next pkg
                        vertex = next_vertex

            print('\nPackages on truck:', truck.show_packages())        

            # Recursively find the next package and load it
            # also add the edge distances together to get the total distance.
            print('-----------------------------------------------------------------------------')
            return edge_distance + load_truck(hash_table, graph, truck, vertex, current_time, deliver_first, packages_loaded)

    return 0



# This method will call load_truck when a truck is available at the hub.   It will also 
# step through time to make the package deliveries as the trucks reach the package delivery
# locations.  It will mark the packages as delivered and remove the package from the trucks
# package list.  When the trucks package list is empty, the truck will return to the hub if
# its return_to_hub flag is set to True, and be reloaded for another delivery.


## O(n^3) time
def deliver_packages(todays_packages, hash_table, distance_graph, hub_vertex, deliver_first):

    packages_loaded = []
    # The first item in each nested list is the truck number, the second is if the
    # truck must return to the hub for another set of packages.
    order_of_trucks_delivering_today = [[1, True],[2, True],[2, False],[1, False]]

    # current_time begins at 08:00AM
    current_time = datetime(10,1,1,8,00,00)

    truck_1 = None
    truck_2 = None
    # to calculate the time new packages can be loaded on the truck
    time_back_to_the_hub = None
    # total_miles is used to calculate/display the total distance the trucks drive
    total_miles = 0
    # used to automate pkg delivery...
    fast = False
    # Loop until all needed trucks have been loaded for the day
    # The lambda function insures the pkg is not EmptyBucket and that it has not been dilivered.
    # will exit the loop when all packages have been delivered.

    ## O(n) time
    while(hash_table.search_by(lambda pkg: type(pkg) is not EmptyBucket and pkg.delivery_status != 'Delivered')):

        # This block corrects the wrong address data when the clock time is >= 10:20AM

        ## O(n) time
        for p in todays_packages:
            if p.notes and p.notes[0] == 'wrong_address' and current_time.time() >= p.notes[1]:
                p.change_address(p.notes[2], p.notes[3], p.notes[4]) 
                # This corrected address vertex may have been visited.  Set
                # vertex_visited to False so we can visit it again.
                v = distance_graph.get_vertex_by_address(p.address)
                v.vertex_visited(False)

        print('\ntodays packages left to deliver:', todays_packages)

        # Trucks one and two will be arriving back at the hub at different times for 
        # their second loads, so I need to sepparate the loading of the trucks to be
        # independant of eachother.

        # if trucks still need to be loaded, then try to load them
        if order_of_trucks_delivering_today:
            
            if truck_1 is None or truck_1.at_hub == True:
                # Create truck objects using the truck numbers/return info found in order_of_trucks_delivering_today
                truck_info = order_of_trucks_delivering_today.pop(0)        
                truck_1 = Truck(truck_info[0])
                # Determine if the truck must return to the hub after empty
                truck_1.set_return_to_hub(truck_info[1])
                truck_1.set_start_time(current_time)

            if truck_2 is None or truck_2.at_hub == True:
                truck_info = order_of_trucks_delivering_today.pop(0)
                truck_2 = Truck(truck_info[0])
                truck_2.set_return_to_hub(truck_info[1])
                truck_2.set_start_time(current_time)
            truck_list = [truck_1, truck_2]
        
        # This block is where the trucks are actually loaded if they are qualified to be loaded
        if time_back_to_the_hub is None or time_back_to_the_hub.time() < current_time.time():
            # Load the trucks

            ## O(t) time
            for t in truck_list:
                # if no packages on truck and it is at the hub
                if not t.package_list and t.at_hub:
                    miles = load_truck(hash_table, distance_graph, t, hub_vertex, current_time.time(), deliver_first, packages_loaded) 
                    # if we are unsuccessful loading the truck (pkgs not ready to load due to delays/wrong address) 
                    # then return the popped info to the list so we can try again.
                    total_miles += t.get_miles()
                    if not t.package_list:
                        order_of_trucks_delivering_today.append(truck_info)
                        break

                # If the truck needs to return for another load, and is currently at the hub,
                # this calculates the edge info between the last vertex and the hub.                
                if t.return_to_hub and t.at_hub:
                    last_vertex = distance_graph.get_vertex_by_address(t.package_list[-1].address)
                    # t.add_miles(distance_graph.get_edge_weight(last_vertex, hub_vertex))
                    total_miles += distance_graph.get_edge_weight(last_vertex, hub_vertex)
                    t.add_edge_info(['HUB', distance_graph.get_edge_weight(last_vertex, hub_vertex)])
                t.set_at_hub(False)
        # A truck was not loaded, so put the truck load info back in the list.    
        else:
            order_of_trucks_delivering_today.append(truck_info)
        
        

        # Move the clock forward one step and then assign packages as delivered with their
        # correct delivery times for those that would have reached their delivery location
        # prior to the current clock time.  Then allow user to check package info or move 
        # the clock time forward again, and repeat until all packages on the two trucks are
        # delivered.

        
        while(True):   
            print('\n\n-----------------------------\nTo continue delivery, enter 1')
            print('To look up or add packages, enter 2')
            if not fast:
                user_choice = input('\nEnter choice now: ')
            else:
                user_choice = '1'

            if user_choice == 'f':
                fast = True
                user_choice = '1'
            if user_choice == str(1):
                # move clock ahead by desired time in seconds (5 minutes = 300 seconds)
                current_time += timedelta(seconds = 300)
                # In five minute clock jumps, the trucks will travel 1.5 miles 
                distance_traveled_in_5_mins = 1.5
                # add 1.5 miles to total distance traveled each loop to both trucks...traveling 1.5 miles / 5 minutes
                for t in truck_list:
                    if t.package_list:
                        t.add_miles_traveled(distance_traveled_in_5_mins)

                print(f'\nCurrent time is: {current_time.time()}')

                # Make the deliveries and mark the time of delivery. Change the package_status to 'delivered'

                ## O(n*t*t.package_list) time
                for t in truck_list:
                    while(t.package_list):
                        if t.pkg_and_edge_distance[0][0] == 'HUB':
                            break
                        t.add_hub_to_next_stop_miles(t.pkg_and_edge_distance[0][1])
                        if t.hub_to_next_stop_miles < t.miles_traveled: # Traveled at least as far as the stop and can deliver
                            # remove all pkgs that go to this stop.  use len(t.pkg_and_edge_distance[0][0]) 
                            ## O(n) time
                            for p in range(t.pkg_and_edge_distance[0][0]):
                                package = t.package_list.pop(0)
                                # todays_packages.remove(package)
                                # Change pkg status to Delivered
                                package.change_package_status('Delivered')

                                # Calculate the actual delivery time of the package
                                miles = t.hub_to_next_stop_miles/18# use hub_next_stop and calculate the actual time it was delivered ############
                                hrs, decimal = divmod(miles, 1)
                                decimal = decimal * 60 # to get whole minutes to the left of the decimal
                                mins, secs = divmod(decimal, 1)
                                total_seconds = int(hrs) * 3600 + int(mins) * 60 + round(secs * 60)
                                delivery_time = t.start_time + timedelta(seconds = total_seconds)
                                package.set_delivery_time(delivery_time)
                                print(f'\n\nDelivered package {package.id_num} at {delivery_time.time()} from truck {t.truck_id}.')
                                print(f'Miles traveled so far for truck {t.truck_id}: {t.miles_traveled}')
                                print(package)

                            print(f'\n\nTruck {t.truck_id} Package List: {t.package_list}')
                            # We have reached this delivery location so remove it from the list
                            t.pkg_and_edge_distance.pop(0)
                            
                        # Havent reached this stop, so check the other truck
                        else:
                            # remove the milage as we cant move on to the next stop yet..will need this compare again
                            t.hub_to_next_stop_miles -= t.pkg_and_edge_distance[0][1]
                            break
                    if not t.package_list and t.return_to_hub:
                        t.set_at_hub(True)
                        #### THE  BELOW CODE TO CALCULATE A RETURN TRIP TO THE HUB COULD/SHOULD GO HERE!!!!!
                        
                
            elif user_choice == str(2):
                # CALL INTERFACE HERE TO ALLOW USER TO LOOK UP PACKAGE INFO
                interface(hash_table, current_time)
                continue
            else:
                print(f'Entry {user_choice} was not recognized.  Try again.')

            
            # If either truck has delivered all packages, break to the outer loop and 
            # load the truck
            if not truck_list[0].package_list or not truck_list[1].package_list:

                ## O(t) time 
                for t in truck_list:
                    # If the truck is still at the hub because it is waiting to load pkgs, it
                    # wont have a pkg_and_edge_distance populated, so pass and break
                    try:
                        if t.pkg_and_edge_distance[0][0] == 'HUB':
                            
                            distance_to_hub = t.pkg_and_edge_distance[0][1]
                            # I need to calculate the time that the truck will arrive back at the 
                            # hub so I know what time its next load starts delivering.
                            # convert distance_to_hub to total seconds to drive back to hub
                            secs = (distance_to_hub/18) * 3600
                            time_back_to_the_hub = current_time + timedelta(seconds = secs)
                            break
                    except:
                        pass
                break
        # search and populate todays_packages again to account for any packages that were added by user.
        todays_packages = hash_table.search_by(lambda pkg: type(pkg) is not EmptyBucket and pkg.delivery_status == 'At HUB')

    # Calculate total miles traveled
    # total_miles += hub_return_distances
    print(f'\n\n----------------------\nAll Packages Delivered: Total miles driven: {total_miles}\n----------------------')
    # print(f'Total miles driven: {total_miles}')

    while(True):
        print('\n\nTo look up or add packages, enter 2')
        print("To exit program, enter 'exit'")
        user_choice = input('\nEnter choice now: ')

        if user_choice == str(2):
                # CALL INTERFACE HERE TO ALLOW USER TO LOOK UP PACKAGE INFO
                interface(hash_table, current_time)
        elif user_choice.lower() == 'exit':
            break
        else:
            print(f'Entry {user_choice} not recognized.  Try again.')