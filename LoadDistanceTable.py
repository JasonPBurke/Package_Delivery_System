import xlrd # To import data from excel files
import pprint # for testing to print dicts in readable format
from Graph import Vertex, Graph


## O(n^2) time
def load_distance_table():

    wb = xlrd.open_workbook('WGUPS Distance Table.xlsx') # the excel workbook
    sh = wb.sheet_by_index(0) # The workbook sheet
    # A list to hold dictionary objects of distance info
    distance_table_list = []
    location_address_list = sh.row_values(7)
    # Clearing out the first two cells from the table that has unwanted info
    location_address_list.pop(0)
    location_address_list.pop(0)
    
    
    # Put the location names in their own list for reference...may not be needed
    # Currently using this to assign the names as keys to their distances from each city
    location_names = []
    for loc in location_address_list:
        location_names.append(loc.split('\n')[0])

    # FOR TESTING PURPOSES
    # for loc in location_names:
    #     print(loc)  

    g = Graph()
    # The vertex list is needed to add edges between nodes
    vertex_list = []
    get_start_vertex = False
    for rownum in range(8, sh.nrows):
        distance_table = dict()
        
        row_values = sh.row_values(rownum)

        distance_table['name'] = row_values[0].split('\n')[0]#.replace('\n', ' ')
        distance_table['address'] = row_values[1].split('\n')#.replace('\n', ' ')
        # Strip the leading whitespace off the address
        distance_table['address'][0] = distance_table['address'][0].strip()
        # TRYING TO STRIP THE () FROM THE ZIP CODE.  THIS IS SHOWING OUT OF INDEX.
        # COULD STRIP BEFORE READING IT OR WHEN READING IT, ACCOUNT FOR THE ()....
        if len(distance_table['address']) > 1:
            distance_table['address'][1] = distance_table['address'][1].strip( '() ' )
        distance_table['adjacent-stops'] = {}
        iterator = 2
        location_index = 0
        while iterator < len(row_values):
            
            # This skips the row that shows the distance from a location to itself.  
            # I dont want this in my adjacent-stops dictionary.
            if row_values[iterator] == 0.0: 
                iterator += 1
                location_index += 1
                continue

            distance_table['adjacent-stops'][location_names[location_index]] = row_values[iterator]
            iterator += 1
            location_index += 1  
        # Below we will create a vertex object and add it to the graph
        name = distance_table['name']
        address = distance_table['address']
        vertex = Vertex(name, address)
        # This small block saves the hub vertex and will be returned with the graph object
        while not get_start_vertex:
            # This sets the 'start vertex' as visited in the vertex object.
            # Used when getting a new shortest path when at a new vertex.
            # vertex.visited = True
            hub_vertex = vertex
            get_start_vertex = True

        g.add_vertex(vertex)
        # Add the vertex object to the vertex_list so we can add edges after the loop.
        vertex_list.append(vertex)
        
        distance_table_list.append(distance_table) # MAY NOT NEED THIS IF ADDING VERTEX TO GRAPH WORKS

    # FOR TESTING PURPOSES
    # for d in distance_table_list:
    #     pprint.pprint(d)

    # Add the undirected edges to all vertex objects
    # Vertex_list holds all the vertex objects
    for vertex_a in vertex_list:
        # Distance_table_list holds all the distance_table dict objects
        for distance_object in distance_table_list:

            if vertex_a.label == distance_object['name']:
                for adjacent_node_key in distance_object['adjacent-stops']:
                    for vertex_b in vertex_list:
                        weight = distance_object['adjacent-stops'].get(adjacent_node_key, 'N/A')
                        if vertex_b.label == adjacent_node_key:
                            g.add_undirected_edge(vertex_a, vertex_b, weight)

    return g, hub_vertex

    # ONLY RETURN LIST IF YOU MOVE THE ABOVE BLOCK TO A SEPERATE LOCATION/FILE
    # return distance_table_list 