from datetime import datetime, time
from QuadraticProbingHashTable import EmptyBucket


# Create an interface so the user can add new packages and look up the state
# of existing packages.
def interface(hash_table, current_time):


    while True:
                 
        print('\n--------------------------\n1 to insert a new package,')
        print('2 to look up package info,\nExit to exit.')

        user_choice = input('\nEnter choice now: ')

        if user_choice == str(1):

            print('To add a new package please enter the following info:')
            id_num = int(input('Package ID number: '))
            address = input('Package address: ')
            delivery_deadline = input('Delivery deadline (enter EOD if no deadline): ')
            city = input('Package City: ')
            zip_code = input('Package zip code: ')
            weight = input('Package weight: ')
            notes = input('Package special notes (enter None if none): ')

            inserted = hash_table.insert(id_num, 
                            address, 
                            delivery_deadline, 
                            city, 
                            zip_code, 
                            weight, 
                            notes)

            print('Package inserted:', inserted)
            inserted_package = hash_table.search_by_id(id_num)
            print(inserted_package)

        # look up packages based on user choice
        elif user_choice == str(2):
            print('---------------------------------\n')       
            print('Enter:\n1 to search by pacakage id,')
            print('2 to search by address,')
            print('3 to search by delivery deadline,')
            print('4 to search by ctiy,')
            print('5 to search by zip code,')
            print('6 to search by package weight,')
            print('7 to search by delivery status, or')
            print('8 to print all packages')

            choice = int(input('\nEnter choice now: '))

            # This list is used to output all packages that were found in the querry
            p_info = []
            if choice == 1:
                p_id = int(input('Enter package id: '))
                p_info = hash_table.search_by(lambda pkg: pkg.id_num == p_id)
                
            elif choice == 2:
                p_address = input('Enter package address: ')
                p_info = hash_table.search_by(lambda pkg: pkg.address == p_address)
            elif choice == 3:
                p_deadline = input("Enter delivery deadline in the format of xx:xxAM or xx:xxPM(enter 'EOD' for end of day): ")
                if p_deadline == 'EOD':
                    p_deadline = '5:00PM'
                p_deadline = datetime.strptime(p_deadline, '%I:%M%p').time()
                p_info = hash_table.search_by(lambda pkg: pkg.delivery_deadline == p_deadline)
                if not p_deadline:
                    print(f'no package with a delivery deadline of {p_deadline} was found.')
            elif choice == 4:
                p_city = input('Enter city: ')
                p_info = hash_table.search_by(lambda pkg: pkg.city == p_city)
            elif choice == 5:
                p_zip = input('Enter zip code: ')
                p_info = hash_table.search_by(lambda pkg: pkg.zip_code == p_zip)
            elif choice == 6:
                p_weight = int(input('Enter weight: '))  # this may need to be an int....
                p_info = hash_table.search_by(lambda pkg: pkg.weight == p_weight)
            elif choice == 7:
                p_status = input("Enter delivery status('At HUB', 'In route', or 'Delivered'): ")
                p_info = hash_table.search_by(lambda pkg: pkg.delivery_status.lower() == p_status.lower())
            elif choice == 8:
                info = ([i for i in hash_table.table])
                p_info = []
                for i in info:
                    if type(i) is not EmptyBucket:
                        p_info.append(i)
                    

            print(f'\n{len(p_info)} packages found for that paramater.')
            # Go throug all packages found and print each packages info in id_num order
            p_info = sorted(p_info, key = lambda pkg: pkg.id_num)
            
            while p_info:
                print('\nCurrent Time:', current_time.time())
                print(p_info.pop(0).__str__())

        elif user_choice.lower() == 'exit':
            return