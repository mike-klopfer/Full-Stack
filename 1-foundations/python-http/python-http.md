# Introductino to the Web from Python

In our last lesson we started using Python's http.server module to help us understand the basics of how a server works and what it does. In this lesson we'll take a deeper look at http.server to help us better understand HTTP.

## Python's `http.server` module

* `http.server` module defines classes for implementing HTTP servers
  * NOTE: http.server is not recommended for production, as it only implements basic security checks.

## Severs and handlers

* Web servers using http.server are made of two parts
  1. The `HTTPServer` class: 
     * This is built-in to the module and is the same for every web service
     * It knows how to listen on a port and accept HTTP requests from clients
     * When it receives a request, it hands that request off to...
  2. A request handler class:
     * This is different for every web service.

* We'll write some Python code to run a mini-web service, and it will need to:
  * Import `http:server`
  * Create a subclass of `http.server.BaseHTTPRequestHandler`. This is our **handler class**.
  * Define a method on the handler calss for each **HTTP verb** you watn to handle
    * The mehtod for GET requests has to be called `do_GET`
    * Inisde the method, call build-in methods of the handler class to read the HTTP request and write the response.
  * Create an instance of `http.server.HTTPServer`, giving it your handler class and server information
  * Call the `HTTPServer` instance's `serve_forever` method.
  
### Exercise: The hello server

In the files we downloaded, there is a simple server program called HelloServer.py:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class HelloHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Now, write the response body.
        self.wfile.write("Hello, HTTP!\n".encode())

if __name__ == '__main__'
    server_adderss = ('', 8000)     # Serve on all addresses, port 8000
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()
```
----
Breaking this code down section by section:
* Import: We use a `from` import to prevent having to type http.server
```python
class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
```
This creates the handler class (which we'll create an instance of in the `name==main` block at the bottom). It inherits from the `BaseHTTPRequestHandler` parent class defined in `http.server`. In this simple case we'll define only one method...the `do_GET` or HTTP GET method.

----
The first thing the server needs to do is send a 200 OK status code; we accomplish this with
```python
        # First, send a 200 OK response.
        self.send_response(200)
```
----
The next thing the server needs to do is send a header section. In this case, we only send a `Content-type` header. The parent class (BaseHTTPRequestHandler) supplies the `send_header` and `end_headers` methods:
```python
        # Then send headers
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
```
----
The last part of this writes the response body. The parent class gives us a variable called `self.wfile`, which is used to send the response. `wfile` stands for writeable file. Python makes an analogy between network connections and open files (they're things you can read and write data to).

`self.wfile` represents the connection from the server to the client and it is write-only, hence the name. Any binary data written to it with its write method gets send to the client as part of the response. 
```python
# Now, write the response body.
        self.wfile.write("Hello, HTTP!\n".encode())
```
----

```python
if __name__ == '__main__':
    server_address = ('', 8000) # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, HelloHandler)
    httpd.serve_forever()
```

This code will run when we run this module as a Python program (vs. importing). The `HTTPServer` constructor needs to know what address and port to listen on (in this case all addresses on port 8000), taking these as a tuple `server_address`. The `HelloHandler` class is used to handle each incomeing client request. 

At the very end, we call `serve_forever` on the instance of `HTTPServer`, telling it to start handling HTTP requests...and off it goes!


