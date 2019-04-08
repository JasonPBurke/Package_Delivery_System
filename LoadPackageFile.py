import xlrd # To import data from excel files
from datetime import datetime, time
from QuadraticProbingHashTable import QuadraticProbingHashTable

## O(n) time
def load_package_data():

    wb = xlrd.open_workbook('WGUPS Package File.xlsx')
    sh = wb.sheet_by_index(0)
    # A list to hold dictionary objects of package data
    package_list = []
    # This dict holds the correction info for package 9 including the time the correction can be made
    # key = package_num (9), value = 4-tuple (address_correction_time, address, city, zip)
    wrong_address_corrections = {}
    wrong_address_corrections[9] = [datetime.strptime('10:20AM', '%I:%M%p').time(), '410 S State St', 'Salt Lake City', '84111']

    # Iterate through each row in the worksheet and put info into a dictionary
    for rownum in range(8, sh.nrows):
        package = dict()
        row_values = sh.row_values(rownum)
        package['package-id'] = int(row_values[0])
        package['address'] = row_values[1]
        package['city'] = row_values[2]
        package['state'] = row_values[3]
        package['zip'] = str(round(row_values[4]))
        try:
            # Convert the Excel time fraction to a readable time value.
            # If time is '10:30 AM', this will show it as 10.5, if time
            # is '10:30 PM', this will show it as 20.5.
            del_time = float(row_values[5]) * 24
            hour, minute = divmod(del_time, 1)
            minute *= 60
            if del_time < 12.0:
                del_time = '{}:{}AM'.format(int(hour), int(minute))
            else:
                del_time = '{}:{}PM'.format(int(hour), int(minute))
            # Create a datetime object representing the delivery time
            # and insert that into the package dict object.
            dt_obj = datetime.strptime(del_time, '%I:%M%p')

            # This adds the delivery deadline to the dictionary obj as
            # a datetime.time() object.  we should be able to use this
            # to compare with the 'current time' to help insure that 
            # packages are delivered on time.
            package['delivery-deadline'] = dt_obj.time()
        except:
            # If the above try block fails, we will check if it was due
            # to the string value of 'EOD' being present.  If so, add 
            # 'EOD' as the value for delivery-deadline.
            if row_values[5] == 'EOD':
                # Consider EOD as 5PM.  Store as a datetime object.
                package['delivery-deadline'] = datetime.strptime('5:00PM', '%I:%M%p').time()#row_values[5]
        package['package-weight'] = row_values[6]
        # parse special notes info into a usable format depending on 
        # what the special note is referring to.
        if row_values[7] == '':
            package['special-notes'] = None 
        else:
            new_special_note = []
            specified_truck = 'Can only be on truck '
            flight_delay = 'Delayed on flight---will not arrive to depot until '
            wrong_address = 'Wrong address listed'
            deliver_with = 'Must be delivered with '

            if specified_truck in row_values[7]:
                new_special_note.extend(('specified_truck', int(row_values[7].strip(specified_truck))))
            elif flight_delay in row_values[7]:
                new_special_note.extend(('flight_delay', datetime.strptime(row_values[7].strip(flight_delay), '%I:%M%p').time()))
            # Get the corrected address and the time the correction comes in.
            # add that info to the notes.
            elif wrong_address in row_values[7]:
                correction_info = wrong_address_corrections[package['package-id']]
                new_special_note.append('wrong_address')
                for i in correction_info:
                    new_special_note.append(i)
            elif deliver_with in row_values[7]:
                # companion_pkgs is a list of the packages the current must be delivered with
                companion_pkgs = row_values[7].strip(deliver_with)
                companion_pkgs = companion_pkgs.split(', ')
                companion_pkgs  = [int(i) for i in companion_pkgs]
                new_special_note.extend(('deliver_with', companion_pkgs))

            package['special-notes'] = new_special_note

        # Add the package dict object to the list
        package_list.append(package)

    # Create a hash tabe object to hold package_data info.
    # Pass in the length of package_data * 2 to create a table of 
    # the correct length with room to add new packages.
    hash_table = QuadraticProbingHashTable(len(package_list))
    for package in package_list:

        inserted = hash_table.insert(package['package-id'],
                                    package['address'],
                                    package['delivery-deadline'],
                                    package['city'],
                                    package['zip'],
                                    package['package-weight'],
                                    package['special-notes'],
                                    )
        if not inserted:
            print('Package id {} not inserted into table.  Table full.'.format(package['package-id']))
    return hash_table