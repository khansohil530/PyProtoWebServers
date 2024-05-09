# Concurrent server
- simplest way to write a `concurrent server` under `Unix` is to use a `fork()` system call.
- When a parent forks a new child, the child process gets a copy of the parent’s `file descriptors`
- Notice we've closed the TCP connection immediatly for parent process and client still receives the data regardless if child is requested laters. 
    - This is because kernel uses `descriptor` reference counts to decide whether to close a socket or not.
    - this reference count increases by 1 for child process, when we use `fork`

## What if we don't close duplicate socket discriptor?
- You'll notice that we've received the response in client, but the socket is still expecting data
- This is because when we close a socket, it send back a `termination packet` (`FIN`) to notify client the request was completed.
- Soon, OS will run out of file discriptors for new request and we'll receive related error

### Another issue even if we close duplicate sockets, `Zombie` processes 
- Looks at [2nd point](#notes) in notes to find more info
- to resolve this, we need to wait for child processes and collect their termination status in parent process
- we can't directly use `.wait()` call since this will block the program execution until child process is completed affecting its concurrency.
- Solution is to used a combination of signal handlers and wait call
- When child process exits, the kernel sends a `SIGCHLD` signal
- parent process can setup a signal handler to asynchronously notify of `SIGCHILD` signals which will then call `wait` to collect termination status.
- This can be done in python using `signal` module. 
    - Example, below code will attach the signal_handler function to parent process and execute the function whenever the kernel raises `SIGCHILD` signal
        ```python
        ...
        import signal

        def signal_handler(signum, frame):
            ...
        
        signal.signal(signal.SIGCHLD, signal_handler)
        ```
- You might also need to ignore few cases where false signal is raised when accept call is blocked

### Another issue with signals is they are not queued.

- If the parent process received a flood of signal at the same time, it might miss some signals
- **Solution** is to setup a `SIGCHLD` event handler but instead of `wait` use a `waitpid` system call with a `WNOHANG` option in a loop to make sure that all terminated child processes are taken care of.
    - Example
        ```python
        def grim_reaper(signum, frame):
            while True:
                try:
                    pid, status = os.waitpid(
                        -1,          # Wait for any child process
                        os.WNOHANG  # Do not block and return EWOULDBLOCK error
                    )
                except OSError:
                    return

                if pid == 0:  # no more zombies
                    return
        ```

# Notes
1. `os.fork()`
    - low-level system call that creates a new process
    - only available on `UNIX` like operating systems
    - **How it works?**
        - `Parent Process`: The `process` that calls `os.fork()`.
        - `Child Process`: A new process created as a copy of the parent process. It inherits most of the parent’s resources (`memory`, `file descriptors`, etc.).
        - `child process` starts executing at the same point as the parent process, immediately after the `os.fork()` call.
        - The return value of `os.fork()` determines the execution path:
            - for `parent process` it returns the `process ID (PID)` of the `child process`.
            - for `child process` it returns 0.
    - **Pros**
        - `Efficient Process Creation`: Forking is fast because the child process initially shares the memory of the parent process (copy-on-write mechanism).
        - `Simplicity`: Provides a straightforward way to create a new process in Unix-like systems.
        - `Inheritance`: The child process inherits the parent’s memory, open file descriptors, environment variables, and other resources, making resource sharing easier.
    - **Cons**
        - `Platform Limitation`: `os.fork()` is not available on `Windows`.
        - `Complexity in Resource management`
            - can cause race conditions or data corruption
            - changes in child process are not handled in parent process
        - `Not thread safe`
        - `Greater overhead` compared to multithreading
        - `More debugging efforts`

2. `zombie processes`
    - a `child process` that has completed execution but still has an entry in the `process table`.
    - It occurs when the `parent process` has not yet called `wait()` (or a similar function) to retrieve the `child process`'s `termination status`.
    - Since the `process table` entry is not freed, the `zombie process` exists in a `defunct` state.
    - problematic because:
        - consumes entries in the `process table`, which is a finite resource.
        - many zombie processes accumulated can exhaust system's resource and cause issue for other processes
    