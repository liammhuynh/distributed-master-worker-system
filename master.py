from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import time
import threading


worker_addresses = [
    "http://localhost:23001/",
    "http://localhost:23002/"
]

worker_requests = [0, 0]  # keep track of the number of requests handled by each worker
worker_status = [True, True]  # keep track of the status of each worker

def ping(index):
    result = query_worker(index,'ping')
    if result == True:
        return 'pong'
    
def choose_worker():
    # choose worker based on the minumum number of requests 
    worker_index = worker_requests.index(min(worker_requests))

    #check if the worker is still alive, choose the other if not
    if worker_status[worker_index] == True:
        return worker_index   
    else:
        return 1 - worker_index
    
def query_worker(worker_index, method, *args):
    # Helper function to send a query to a worker and return the result
    worker_addr = worker_addresses[worker_index]
    try:
        worker = ServerProxy(worker_addr)
        result = getattr(worker, method)(*args)
        if not result['error']:
            return result['result']
    except ConnectionRefusedError:
        print(f"Worker {worker_index+1} at {worker_addr} is down.")
        worker_status[worker_index] = False
    return None

def getbylocation(location):
    # Forward query to the worker with the lowest number of requests handled
    worker_index = choose_worker()
    query_result = query_worker(worker_index, 'getbylocation', location)
    if query_result is not None:
        # Update the number of requests handled by the worker
        worker_requests[worker_index] += 1
        print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
        return query_result

    # Both workers are down, return an empty list
    print("All workers are down.")
    return []

def getbyname(name):
 # Forward query to the appropriate worker based on the first letter of the name
    worker_index = choose_worker()
    query_result = query_worker(worker_index, 'getbyname', name)
    if query_result is not None:
        # Update the number of requests handled by the worker
        worker_requests[worker_index] += 1
        print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
        return query_result
    
       # Both workers are down, return an empty list
    print("All workers are down.")
    return []

def getbyyear(location, year):
    # Forward query to the worker with the lowest number of requests handled
    worker_index = choose_worker()
    query_result = query_worker(worker_index, 'getbyyear', location, year)
    if query_result is not None:
            # Update the number of requests handled by the worker
            worker_requests[worker_index] += 1
            print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
            return query_result

# If all workers have failed, return an empty result
    print("All workers are down.")  
    return []

def monitor_workers():
    # Check the status of each worker periodically
    while True:
        for i, worker_addr in enumerate(worker_addresses):
            if worker_status[i] == True:
                # Send a ping request to the worker
                worker = ServerProxy(worker_addr)
                response = ping(i)
                if response != "pong":
                    #Worker is not responding properly, mark as down
                    print(f"Worker {i+1} is down.")
                    worker_status[i] = False
            else:
                worker = ServerProxy(worker_addr)
                response = ping(i)
                if response == "pong":
                    print(f"Worker {i+1} is up.")
                    worker_status[i] = True
                    worker_requests[0] = 0
                    worker_requests[1] = 0
                
        # Wait for some time before checking again
        time.sleep(1)

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")
    

    # Register RPC functions
    server.register_function(getbylocation)
    server.register_function(getbyname)
    server.register_function(getbyyear)

    monitor_thread = threading.Thread(target=monitor_workers)
    monitor_thread.daemon = True
    monitor_thread.start()

    server.serve_forever()
   

if __name__ == '__main__':
    main()

