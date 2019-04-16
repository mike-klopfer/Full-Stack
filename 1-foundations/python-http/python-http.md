# Introduction to the Web from Python

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


## What about `.encode()?`

An HTTP response could contain almost any kind of data (depending in part on what the user asked for). The trouble is, the `self.wfile.write` method in the handler expects to be given a `bytes` object (a piece of binary data), which it writes over the network in the HTTP response body.

If you want to send a string over the HTTP connection, you have to `encode` the string into a `bytes` object. The `encode` method on strings does exactly that. Of course, there is also a `decode` method for turning `bytes` objects into strings.

UTF-8 is the default encoding in Python, and this is what Python will use when we call the `encode` method on a string.

## The echo server

We'll modify our hello server to echo back whatever request path we send it...so for instance if we access the page `http://localhost:8000/bears`, we will see "bears" in the browser. We call this an **echo server**. 

In order to do this, the servrer needs to be able to look at the request information. `http.server` can do this. 

### Exercise: Making the echo server

We modify the HelloHandler code to make an EchoHandler. Here is the final code:

```python
rom http.server import HTTPServer, BaseHTTPRequestHandler


class EchoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()

        # Now, write the response body.
        msg = self.path[1:]
        self.wfile.write(msg.encode())

if __name__ == '__main__':
    server_address = ('', 8000)  # Serve on all addresses, port 8000.
    httpd = HTTPServer(server_address, EchoHandler)
    httpd.serve_forever()
```

Things we had to do to make this work/short description
1. Create the message we want to send. In this case we use the instance variable `self.path` to grab everything that is on the path, including the root, `/`, so for example if the path is `http://localhost:8000/bears`, then `self.path` is `/bears`. We slice the resulting string in order to drop off the `/`.
2. Change the name of the class to `EchoHander` in the class creation line, and in the `name==main` execution section.

Thats it! When we tried it out we realize that it will grab the whole path in the URI except for any fragments (anything appearing after a `#`). These fragments only affect the browser, so they don't get sent as part of an HTTP GET request.

## Queries and Quoting

When you take a look at URI for a major web service we often see several *query parameters*, which are a sort of variable assignment that occurs after a `?` in the URI. Here is an example from a Google image search URI: `https://www.google.com/search?q=gray+squirrel&tbm=isch`

The **query** part of the URI is the part after the `?`. Normally query parameters are written as `key=value` and separated by `&` signs. Thus the query above has two query parameters, `q` and `tbm` wiht the values `gray+squirrel` and `isch` (where `isch` is for image search).

A Python library called `urllib.parse` knows how to upack query parametrs and other parts of an HTTP URL. (`urllib.parse` doesn't work on all URI's, only on some URLs.)

### Exercise:

A demo of `urllib.parse`. 
* In a Python interpreter we import relevant parts of `urllib.parse` (specifically `urlparse` and `parse_qs`).
* Store an adress (`https://www.google.com/search?q=gray+squirrel&tbm=isch`) to a variable `address`
* Run `urlparse` with argument `address` to use the URL parser that we imported on the Google search address, and store in a variable `parts`...this variable will be the parts of the URL
* Print the result

What we end up with is:
```
ParseResult(scheme='https', netloc='www.google.com', path='/search', params='', query='q=gray+squirrel&tbm=isch', fragment='')
```
So we can see that this URL parser has divided up the URL we entered giving us
* Scheme is https
* Server we are trying to access is at location `www.google.com`
* The path we are trying to access at that location is `/search`
* The query (`?`) has two parts, q = gray squirrel AND tbm = image search

We can ask to see just the queries by typing `print(parts.query)`, and we'll get back `q=gray+squirrel&tbm=isch`. 

Finally, if we try to store these parts of the query, we do:

```python
>>> query = parse_qs(parts.query)
>>> query
{'q': ['gray squirrel'], 'tbm': ['isch']}
```
And we see that we have the queries stored in a dictionarty, by using the parse_qs method that we imported. Note that when Python and `urllib.parse` store the queries in a dictionary, they automatically strip out some of the HTML encoding (replacing a `+` with a space for example). Things in URLs are formatted in very specific manner. 

More details in the documentation for `urllib.parse.quote here: https://docs.python.org/3/library/urllib.parse.html#url-quoting. Translating URLs to the correct format makes them "URL-safe" or "URL-quoted" or "URL-encoded" or "URL-escaped" (terms used interchangably).

## HTML and forms

In most cases, users of a browser don't input their search queries (or other info) into a URI to accomplish a search, rather they input required items into an HTML form. This lesson will look at using forms to pass information to a server.

### Exercise: HTML and forms

Quick refresher on HTML forms here:
https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms

We open up the HTML in our browser by navigating to the directory where it is stored, and typing open [file name] at the command line. This piece of HTML for this exercise looks like this:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Login Page</title>
    <style>
        label, input, button {
            margin: 8px;
        }
    </style>
</head>
<body>
    <form action="http://localhost:8000/" method="GET">
        <h2>Login</h2>
        <label for="username">Username:</label>
        <input type="text" name="username" id="username">
        <br>
        <label for="pw">Password:</label>
        <input type="password" name="pw" id="pw">
        <br>
        <button type=submit>Log in!</button>
    </form>
</body>
</html>
```
Since the form action is on localhost port 8000, we can see the results by initializing our echo server on port 8000. The result is that any entries we make to the form fields "username" and "password" are simply displayed on the screen in the form of an HTML query. (Keeping in mind that the "GET" HTML method asks the server to GET a certain resource. HTTP 1.1 reformats this into the appropriate query, and passes it to the server, in this case our echo server, so this query is then echoed as output!)

Lets try a more complicated form:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Search wizardry!</title>
    <style>
        label, input, button {
            margin: 8px;
        }
    </style>
</head>
<body>

    <form action="http://www.google.com/search" method="GET">
        <label>Search term:
            <input type="text" name="q">
        </label>
        <br>
        <label>Corpus:
            <select name="tbm">
                <option selected value="">Regular</option>
                <option value="isch">Images</option>
                <option value="bks">Books</option>
                <option value="nws">News</option>
            </select>
        </label>
        <br>
        <button type="submit">Go go!</button>
    </form>
</body>
</html>

```
This example takes the user in put in the "Search Term" field, and with a selection from dropdown "Corpus" (to choose which type of media to search), composes a GET request formatted to use Google search. Importantly, we note that the "form action" field tells the browser which URI to send the request to. 


## GET and POST

### Form methods: GET and POST

When a browser submits a form via `GET` it puts all of the from fields into the URI that it sends to the server. These are sent as a query (we did this in the first exercise, previous lesson). They're all jammed together into a single line. Since they're all in the URI the user can bookmark the result, reload, etc.

This is good for search engine queries, but not as good for posts on a comment board or an e-commerce shopping cart. As we've seen `GET` methods are fine for search forms and actions that are intended to *look something up*, but not as good for actions that are intended to alter or create a resource. For this sort of action, HTTP uses the verb `POST`.

----
### Idempotence

An action is **idempotent** if doing it twice (or more) produces the same result as doing it once (Ex: *"Show me the search results for 'polar bear'"* is idempotent where as *"Add a polar bear to my shopping cart"* is not). 

`POST` requests are not idempotent. If you've ever seen a warning from your browser asking if you really mean to resubmit a form, what its really asking is if you want to do a non-idempotent action a second time.

----
### Exercise: Be a server and receive a POST request

Here is some HTML that sends a `POST` request to localhost 9999:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Testing POST requests</title>
    <style>
        label, input, button {
            margin: 8px;
        }
    </style>
</head>
<body>
    <form action="http://localhost:9999/" method="POST">
        <label>Magic input:
            <input type="text" name="magic" value="mystery">
        </label>
        <br>
        <label>Secret input:
                <input type="text" name="secret" value="spooky">
        </label>
        <br>
        <button type="submit">Do a thing!</button>
    </form>
</body>
</html>
```


