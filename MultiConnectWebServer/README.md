# Handling Multiple Connection

- To handle multiple connections, we need to know when a socket is ready for reading and writing
- We can implement this using `selector` module in python using `.select()` method.
- The `.select()` method allows you to check for `I/O completion` on more than one socket.

## Working with `selector` in python

- `Selector` Object: This is the core object used to `monitor multiple I/O channels` (like sockets) for `readiness` to perform `I/O operations`.
- `Events`: The module defines two constants:
    - `selectors.EVENT_READ`: Wait for the channel to be ready for reading.
    - `selectors.EVENT_WRITE`: Wait for the channel to be ready for writing.
- `Key`: A `SelectorKey` object, returned when you register a socket, contains:
    - `fileobj`: The registered socket or file-like object.
    - `events`: The events being monitored.
    - `data`: Optional user-defined data attached to the registration.

## Steps to Use `selectors` for I/O Multiplexing
1. **Create a `Selector` Object**: Instantiate a selector object using `selectors.DefaultSelector()`.
2. **Register Sockets**: Register one or more sockets for `EVENT_READ` or `EVENT_WRITE`.
3. **Monitor for Events**: Use the `.select()` method to wait for events on the registered sockets.
4 **Handle Events**: Process the sockets ready for I/O based on the returned events.

## Key Benefits of `selectors` Module
- `Scalability`: Efficiently handles many sockets without spawning multiple threads or processes.
- Ease of Use: Provides a high-level API for event-driven programming.
- Portability: Abstracts platform-specific details like epoll, kqueue, or poll.


# Demo

```bash
python multiconn-server.py <host> <port>

python multiconn-client.py <host> <port> <num-conn>
```