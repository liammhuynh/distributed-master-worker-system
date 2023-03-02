from xmlrpc.server import SimpleXMLRPCServer
import sys
import json

# Storage of data
data_table = {}

def ping():
    return {
        'error': False,
        'result': True
    }

def load_data(group):
    # load data based which portion it handles (am or nz)
    global data_table
    if group == 'am':
        with open('data-am.json') as f1, open('data-nz.json') as f2:
            #open the two JSON files, and the | operator is used to merge the dictionaries loaded from each file.             
            data_table = json.load(f1) | json.load(f2) 
    elif group == "nz":
        with open('data-nz.json') as f1, open('data-am.json') as f2:
            data_table = json.load(f1) | json.load(f2)
    
def getbyname(name):
    # Look up person by name
    try:
        result = data_table[name]
        return {
            'error': False,
            'result': [result]
        }
    except KeyError:
        return {
            'error': False,
            'result': []
        }
            
def getbylocation(location):
    # Filter data to include only records with specified location
    if not data_table:
        return {
            'error': True,
            'result': 'No data loaded'
        }
    
    results = []
    for record in data_table.values():
        if record['location'] == location:
            results.append(record)
    
    return {
        'error': False,
        'result': results
    }

def getbyyear(location, year):
    # filter data to include only records with specified location & year
    if not data_table:
        return {
            'error': True,
            'result': 'No data loaded'
        }
    results = []
    for record in data_table.values():
        if record['location'] == location and record['year'] == year:
            results.append(record)

    return {
        'error': False,
        'result': results
    }

def main():
    if len(sys.argv) < 3:
        print('Usage: worker.py <port> <group: am or nz>')
        sys.exit(0)

    port = int(sys.argv[1])
    group = sys.argv[2]
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    load_data(group) # load the data based on the group parameter

    # register RPC functions
    server.register_function(getbyname)
    server.register_function(getbylocation)
    server.register_function(getbyyear)
    server.register_function(ping)

    server.serve_forever()

if __name__ == '__main__':
    main()
