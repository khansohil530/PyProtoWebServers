import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()
messages = [b"Message 1 from client.", b"Message 2 from client."]

def start_connections(host, port, num_conns):
    server_addr = (host, port)
    for i in range(0, num_conns):
        connid = i + 1
        print(f"Starting connection {connid} to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=connid,
            msg_total=sum(len(m) for m in messages),
            recv_total=0,
            messages=messages.copy(),
            outb=b"",
        )
        sel.register(sock, events, data=data)

def service_connection(key, mask):
     sock = key.fileobj
     data = key.data
     if mask & selectors.EVENT_READ:
         recv_data = sock.recv(1024)  # Should be ready to read
         if recv_data:
             print(f"Received {recv_data!r} from connection {data.connid}")
             data.recv_total  += len(recv_data)
         if not recv_data or data.recv_total == data.msg_total:
             print(f"Closing connection {data.connid}")
             sel.unregister(sock)
             sock.close()
     if mask & selectors.EVENT_WRITE:
         if not data.outb and data.messages:
             data.outb = data.messages.pop(0)
         if data.outb:
             print(f"Sending {data.outb!r} to connection {data.connid}")
             sent = sock.send(data.outb)  # Should be ready to write
             data.outb = data.outb[sent:]

try:
    host, port, num_conns = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    start_connections(host, port, num_conns)
    while sel.get_map():
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()