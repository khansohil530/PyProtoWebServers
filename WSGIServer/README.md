# **Problem Statement**
- How do you run a Django application, Flask application, under your freshly minted Web server without making a single change to the server to accommodate all those different Web frameworks?

# **Solution**
- `Python Web Server Gateway Interface` (or `WSGI`)
- `WSGI` is a Python standard defined in `PEP 3333` that enables web servers and applications to interact in a consistent way.
- `WSGI` allowed developers to mix b/w Web framework and Web server that suits the needs provided both of them have implemented support for `WSGI`
- You can run `Django`, `Flask`, for example, with `Gunicorn` or `Nginx`.


# **Implementation**

The Key Components of WSGI are:
1. `Application`: A `callable object` (`function` or `class`) that receives an `environ` dictionary and a `start_response` `callable`, and `returns` an `iterable producing the HTTP response body`.
2. `Server`: A `component` that handles the `HTTP protocol`, interacts with the application through the `WSGI interface`, and `serves HTTP responses`.

# How it works?
- The framework provides an `application` callable
- The server invokes the `application` callable for each request it receives from an `HTTP` client.
- It passes a dictionary `environ` containing `WSGI/CGI` variables and a `start_response` callable as arguments to the `application` callable.
- The `framework/application` generates an `HTTP status` and `HTTP response headers` and passes them to the `start_response` callable for the `server` to store them. The `framework/application` also returns a `response body`.
- The `server` combines the `status`, the `response headers`, and the `response body` into an `HTTP response` and transmits it to the client


# Demo

- Using a simple wsgi app
```bash
python wsgiserver.py simpleapp:simple_app
```
- Using a flask app
```bash
docker build -t flaskserver .

docker container run -p 8888:8888 flaskserver
```

# Enhancements for a `Real Server`
- `Error Handling`: Requires robust `error handling` for `malformed requests` and `internal server errors`.
- `Concurrency`: Supports `multiple connections` using `threading`, `forking`, or `asynchronous I/O`.

# Common terms and tech

1. **File Descriptors**
- a non-negative integer that the `kernel` returns to a `process` when it opens an `existing file`, creates a `new file` or when it creates a `new socket`.
- You’ve probably heard that in UNIX everything is a file.
- The `kernel` refers to the `open files` of a `process` by a `file descriptor`.
- When you need to `read` or `write` a `file` you identify it with the `file descriptor`.
- `Python` gives you `high-level objects` to deal with `files` (and `sockets`) and you don’t have to use `file descriptors` directly to identify a `file` but, under the hood, that’s how `files` and `sockets` are identified in `UNIX`: by their `integer file descriptors`.
By default, `UNIX shells` assign `file descriptor 0` to the `standard input` of a process, `file descriptor 1` to the `standard output` of the process and `file descriptor 2` to the `standard error`.
- You can access file no associated with file descriptor in python using `.fileno()` method
- You can also use `file descriptors` to make system calls  to perform ur task
- Example
    ```python
    import sys
    import os
    res = os.write(sys.stdout.fileno(), 'hello\n')
    print(res)
    >> hello
    ```
