# Distributed-master-worker-system

Blaine Steck

Melisa Nguyen

Thuy Huynh

This code implements a distributed information retrieval system using XML-RPC protocol. The system consists of a master server and two worker servers that handle user queries. 

The master server distributes queries to the workers based on their current load, choosing the one with the lowest number of requests.

The workers store the data and provide methods for querying it based on name, location, and year. 

Additionally, the workers periodically send ping requests to the master server to inform it of their status. 

The system is fault-tolerant, as the master server can handle worker failures by choosing the other worker to handle the query. The code demonstrates a simple but effective use of threading and distributed systems principles to provide a scalable and reliable information retrieval system.

The master server has several functions:

    choose_worker(): This function selects the worker with the lowest number of requests and checks if it's still alive. If the selected worker is down, the other worker is chosen to handle the query.

    query_worker(worker_index, method, *args): This function sends a query to the specified worker and returns the result. It also handles ConnectionRefusedError exceptions that may occur if the worker is down.

    getbylocation(location): This function forwards a query to the worker selected by choose_worker(). The query retrieves all records with the specified location.

    getbyname(name): This function forwards a query to the worker selected by choose_worker(). The query retrieves a record with the specified name.

    getbyyear(location, year): This function forwards a query to the worker selected by choose_worker(). The query retrieves all records with the specified location and year.

    monitor_workers(): This function periodically checks the status of each worker by sending ping requests to them.

The worker server has these functions:

    ping(): This function returns a ping response to the master server to indicate that the worker is still alive.

    load_data(group): This function loads the data based on the specified group (am or nz) from two JSON files and merges them into a dictionary.

    getbyname(name): This function looks up a record with the specified name and returns it.

    getbylocation(location): This function retrieves all records with the specified location and returns them.

    getbyyear(location, year): This function retrieves all records with the specified location and year and returns them.
