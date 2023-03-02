# Distributed-master-worker-system

Blaine Steck
Melisa Nguyen
Thuy Huynh

This code implements a distributed information retrieval system using XML-RPC protocol. The system consists of a master server and two worker servers that handle user queries. 

The master server distributes queries to the workers based on their current load, choosing the one with the lowest number of requests.
The workers store the data and provide methods for querying it based on name, location, and year. 
Additionally, the workers periodically send ping requests to the master server to inform it of their status. 
The system is fault-tolerant, as the master server can handle worker failures by choosing the other worker to handle the query. The code demonstrates a simple but effective use of threading and distributed systems principles to provide a scalable and reliable information retrieval system.
