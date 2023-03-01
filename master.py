from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import sys
import time


worker_addresses = [
    "http://localhost:23001/",
    "http://localhost:23002/"
]

worker_requests = [0, 0]  # keep track of the number of requests handled by each worker
worker_status = [True, True]  # keep track of the status of each worker

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
    worker_index = worker_requests.index(min(worker_requests))
    query_result = query_worker(worker_index, 'getbylocation', location)
    if query_result is not None:
        # Update the number of requests handled by the worker
        worker_requests[worker_index] += 1
        print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
        return query_result
    
    # If the worker is down, try the other worker
    other_worker_index = 1 - worker_index
    if worker_status[other_worker_index]:
        print(f"Retrying with worker {other_worker_index+1}...")
        query_result = query_worker(other_worker_index, 'getbylocation', location)
        if query_result is not None:
            # Update the number of requests handled by the worker
            worker_requests[other_worker_index] += 1
            print(f"Worker {other_worker_index+1}: {worker_requests[other_worker_index]} requests")
            # Update the status of the first worker, which is assumed to be up again
            worker_status[worker_index] = True
            return query_result

    # Both workers are down, return an empty list
    print("All workers are down.")
    return []

def getbyname(name):
 # Forward query to the appropriate worker based on the first letter of the name
    worker_index = ord(name[0].lower()) < ord('n')

    # Keep trying to query workers until a valid response is received
    for i in range(len(worker_addresses)):
        query_result = query_worker(worker_index, 'getbyname', name)
        if query_result is not None:
            # Update the number of requests handled by the worker
            worker_requests[worker_index] += 1
            print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
            return query_result
        else:
            # If the worker fails, mark it as down and try the next one
            print(f"Worker {worker_index+1} is down. Trying next worker...")
            worker_requests[worker_index] = sys.maxsize
            worker_index = 1 - worker_index

    # If all workers have failed, return an empty result
    return []

def getbyyear(location, year):
    # Forward query to the worker with the lowest number of requests handled
    worker_index = worker_requests.index(min(worker_requests))

    # Keep trying to query workers until a valid response is received
    for i in range(len(worker_addresses)):
        query_result = query_worker(worker_index, 'getbyyear', location, year)
        if query_result is not None:
            # Update the number of requests handled by the worker
            worker_requests[worker_index] += 1
            print(f"Worker {worker_index+1}: {worker_requests[worker_index]} requests")
            return query_result
        else:
            # If the worker fails, mark it as down and try the next one
            print(f"Worker {worker_index+1} is down. Trying next worker...")
            worker_requests[worker_index] = sys.maxsize
            worker_index = 1 - worker_index

    # If all workers have failed, return an empty result
    return []

def monitor_workers():
    # Check the status of each worker periodically
    while True:
        for i, worker_addr in enumerate(worker_addresses):
            try:
                # Send a ping request to the worker
                worker = ServerProxy(worker_addr)
                response = worker.ping()
                if response != "pong":
                    # Worker is not responding properly, mark as down
                    print(f"Worker {i+1} is down.")
                    worker_addresses.remove(worker_addr)
                    worker_requests.pop(i)
            except ConnectionRefusedError:
                # Worker is not responding, mark as down
                print(f"Worker {i+1} is down.")
                worker_addresses.remove(worker_addr)
                worker_requests.pop(i)
        # Wait for some time before checking again
        time.sleep(5)

def main():
    port = int(sys.argv[1])
    server = SimpleXMLRPCServer(("localhost", port))
    print(f"Listening on port {port}...")

    # Register RPC functions
    server.register_function(getbylocation)
    server.register_function(getbyname)
    server.register_function(getbyyear)
        
    server.serve_forever()


if __name__ == '__main__':
    main()

