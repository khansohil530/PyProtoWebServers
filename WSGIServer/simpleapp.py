def simple_app(environ, start_response):
    """A simple WSGI application."""
    path = environ['PATH_INFO']
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)

    if path == '/':
        return [b"Welcome to the WSGI server!"]
    elif path == '/hello':
        return [b"Hello, World!"]
    else:
        status = '404 Not Found'
        start_response(status, [('Content-Type', 'text/plain')])
        return [b"Not Found"]