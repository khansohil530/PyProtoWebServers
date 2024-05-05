import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# ...
def accept_wrapper(sock):
    """
    - We'll accept the connection at socket to establish the TCP connection
    - From here one, the events can be either read or write since we need to read incoming data
      from socket and write back once we've read all the data.
    """
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # If we've read event and receive data, we'll add the data to data key.
        # Else, we'll close the TCP connection and unregister it from our selector
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        # If we've outbound data present, we'll send the current data and update remaining data
        # in selector data key.
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]     
        
# Setup listening port and register it with selector    
# selector is initially registered with read event since we've to receive data to write back 
host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)



try:
    while True:
        # Start the event loop,
        # select with timeout=None will block the execution of program until event a available
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                # If no date has been received, we'll accept the TCP connection and save the
                # TCP socket
                accept_wrapper(key.fileobj)
            else:
                # If connection has been accepted, we'll read all the data and write back to it
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()