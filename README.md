# Distributed Master-Worker System

This is a distributed system that handles queries on a dataset by forwarding them to two worker nodes that run instances of the same program. 
The queries can be for data on a specific location, name or year. 
The program implemented in Python and uses XML-RPC for communication between the server and workers.

The server has the following functions that are registered with the XML-RPC server:

    getbylocation(location): Forwards the query to the worker with the lowest number of requests handled. If that worker is down, the query is forwarded to the other worker. If both workers are down, an empty list is returned.
    getbyname(name): Forwards the query to the worker that handles the group of data where the name belongs. If the worker is down, the query is forwarded to the other worker. If both workers are down, an empty list is returned.
    getbyyear(location, year): Forwards the query to the worker with the lowest number of requests handled. If that worker is down, the query is forwarded to the other worker. If both workers are down, an empty list is returned.

The worker has the following functions:

    load_data(group): Loads data into the data_table dictionary based on which worker is handling the data.
    getbylocation(location): Returns a list of data that matches the location.
    getbyname(name): Returns a list of data that matches the name.
    getbyyear(location, year): Returns a list of data that matches the location and year.

The system also has a function monitor_workers() that periodically checks the status of each worker and marks them as down if they are not responding properly.

The system is designed to handle failures of workers and load balance the queries among the workers.
