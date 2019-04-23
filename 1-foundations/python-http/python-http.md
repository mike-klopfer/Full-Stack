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
  * Define a method on the handler class for each **HTTP verb** you want to handle
    * The mehtod for GET requests has to be called `do_GET`
    * Inisde the method, call built-in methods of the handler class to read the HTTP request and write the response.
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

`self.wfile` represents the connection from the server to the client and it is write-only, hence the name. Any binary data written to it with its write method gets sent to the client as part of the response. 
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

This code will run when we run this module as a Python program (vs. importing). The `HTTPServer` constructor needs to know what address and port to listen on (in this case all addresses on port 8000), taking these as a tuple `server_address`. The `HelloHandler` class is used to handle each incoming client request. 

At the very end, we call `serve_forever` on the instance of `HTTPServer`, telling it to start handling HTTP requests...and off it goes!


## What about `.encode()?`

An HTTP response could contain almost any kind of data (depending in part on what the user asked for). The trouble is, the `self.wfile.write` method in the handler expects to be given a `bytes` object (a piece of binary data), which it writes over the network in the HTTP response body.

If you want to send a string over the HTTP connection, you have to `encode` the string into a `bytes` object. The `encode` method on strings does exactly that. Of course, there is also a `decode` method for turning `bytes` objects into strings.

UTF-8 is the default encoding in Python, and this is what Python will use when we call the `encode` method on a string.

## The echo server

We'll modify our hello server to echo back whatever request path we send it...so for instance if we access the page `http://localhost:8000/bears`, we will see "bears" in the browser. We call this an **echo server**. 

In order to do this, the server needs to be able to look at the request information. `http.server` can do this. 

### Exercise: Making the echo server

We modify the HelloHandler code to make an EchoHandler. Here is the final code:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler


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
And we see that we have the queries stored in a dictionary, by using the parse_qs method that we imported. Note that when Python and `urllib.parse` store the queries in a dictionary, they automatically strip out some of the HTML encoding (replacing a `+` with a space for example). Things in URLs are formatted in very specific manner. 

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
This example takes the user input in the "Search Term" field, and with a selection from dropdown "Corpus" (to choose which type of media to search), composes a GET request formatted to use Google search. Importantly, we note that the "form action" field tells the browser which URI to send the request to. 


## GET and POST

### Form methods: GET and POST

When a browser submits a form via `GET` it puts all of the form fields into the URI that it sends to the server. These are sent as a query (we did this in the first exercise, previous lesson). They're all jammed together into a single line. Since they're all in the URI the user can bookmark the result, reload, etc.

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
If we listen on port 9999 with `$ ncat -l 9999`, we get the following:
```
POST / HTTP/1.1
Host: localhost:9999
Content-Type: application/x-www-form-urlencoded
Origin: null
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15
Content-Length: 27
Accept-Language: en-us
Accept-Encoding: gzip, deflate

magic=mystery&secret=spooky
```

 A few notes on this output:
 * We notice that unlike a GET request, the browser has not encoded the data in the URI path like it does with a GET request
 * Instead, it sends the form data in the request body, underneath the heades.

## A server for POST

In this lesson we'll be building a **messageboard server**. This server will be designed to host a messageboard which will display a form for writing messages as well as a list of previously written messages, and thus will need both GET and POST HTTP methods (GET for viewing messages, POST for submitting them).

### POST handlers read the request body

In an earlier lesson working on the HelloServer, we wrote some handler classes that had just a single method, `do_GET`. This handler will ned to have a `do_POST` method to support the required POST requests.

Outline of methods:
* `do_GET`
  * Send the HTML form...and
  * Send current messages
* `do_POST`
  * POST request implies that there is a new message
  * Server will store the message in a list...and...
  * REturn all the messages it's seen so far
  * Remembering that the message to be posted will be in the request body of the HTTP reuqest, so `do_POST` will need to read the request body by calling the built-in `self.rfile.read` method.
    * `self.rfile` is af file object, like the `self.wfile` we say earlier, except `rfile` is for reading the request, rather than writing the response
    * `self.rfile.read` needs to be told how many bytes to read...in other words, how long the request body is...something like `self.rfile.read(140)`
    * The browser will send the length of the request body in the `Content-Length` header

### Headers are strings (or missing)

In the previous section we discussed the requirement of our `do_POST` method to use `self.rfile.read(length)` to extract the message part of the HTTP request (in a POST request). This technique encounters two main difficulties:
1. Extracting `Content-Length` from the HTTP request
   * We handle this by using the instance variable `self.headers`
   * This instance variable acts like a Python dictionary, where the keys are the header names, except they're case insensitive, so we can look up `content-length` or `Content-Length`
   * The values in this dictionary are strings, we will need to convert these into integers in order for `self.rfile.read` to work correctly
2. Its also possible that the HTTP request body will be empty, and the browser might not send a `Content-Length` at all
   * Thus when accessing the headers from `self.headers` we should use the `.get` dictionary method (instead of a pure lookup...preventing a `KeyError`). 

The following code snippet can be used in the `do_POST` handler to find the length of the request body and read it:

```python
length = int(self.header.get('Content-Length', 0))
data = self.rfile.read(length).decode()
```

Once we've read the body we can use `urllib.parse.parse_qs` to extract the POST parameters

### Messageboard Part One

Here is the starter code, it is located in the Messageboard PartOne folder in this repository at `1-foundations/python-http/course-ud303/Lesson-02:
```python
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message? (Use the Content-Length header.)

        # 2. Read the correct amount of data from the request.

        # 3. Extract the "message" field from the request data.

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
```

I've created a local copy of this file which is just in the `python-http` folder

1. First I used `self.headers.get('Content-Length',0))` in the `do_POST` method to get the length of the message. 
   * One mistake I made during this step was calling `self.header` (incorrect) instead of `self.headers` (correct)
2. Next I extracted and decoded the message with `self.rfile.read(length).decode()` 
  * During this step I was unsure how to proceed with extracting only the message, so I passed the outcome from this step directly into a variable called `message` and just displayed the whole thing
  * In this case, the only thing contained in the output was `message=[whatever stuff I typed in]`
3. Since I was unsure exactly how to extract only the message, I used `urllib.parse.parse_qs` to change the HTTP message into a python dictionary.
   * I tried to display the whole dictionary, but received an `AttributeError` since a dictionary doesn't have the `.encode()` method
   * Based on the output during step 2 (`message=[stuff]`), I guessed that the key I'd need would be `message`
     * This still returned an error, since data type returned by calling the key was a list...presumably a list of all the messages
     * Since I only want the first message, I indexed `[0]`, and this produced the result I wanted.
* Extra: I also slighly changed the import statements, to avoid using `from package-x import module-y` type syntax.

Here is the code at the end of part one:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message?
        length = int(self.headers.get('Content-length', 0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()

        # 3. Extract the "message" field from the request data.
        message = parse_qs(data)["message"][0]

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
```


----

### Messageboard Part Two

I'll keep working from the same file that I started last exercise. In the previous exercise, we had to manually load the HTML form each time we wanted to use the form. In this exercise we'll modify our messageboard code so that it automatically serves the form. 

We'll do this in two steps:
1. Create a string variable which contains the HTML code we want to serve
   * This part was easy...just grab the HTML text from Messageboard.html, and store it as a triple-quoted string in our python script. 
2. Create a `do_GET` method that serves this form when the server is running.
   * This was slightly more difficult. We had to do several steps
     * Make do_GET method with appropriate items, including
     * `self.wfile.write(msg_html.encode())`
     * However, because I copied the formatting from the `do_POST` method, when I ran the server, it displayed the HTML as text
       * This was because I had in the `self.send_header` the `Content-type` as `text/plain`
       * Once I changed it to `HTML` everything worked

Here is the code at the end of part two:
```python
import http.server as hs
import urllib

msg_html = '''
<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
'''

class MessageHandler(hs.BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message? (Use the Content-Length header.)
        length = int(self.headers.get('Content-Length', 0))

        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()

        # 3. Extract the "message" field from the request data.
        message = urllib.parse.parse_qs(data)['message'][0]
        
        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/HTML; charset=utf-8')
        self.end_headers()
        self.wfile.write(msg_html.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = hs.HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()
```

## Post-Redirect-Get

This is a common design paradigm for interactive HTTP applications and API's. Here's the basic structure

* A client `POST`s to a server to create or update a resource
* On success, the server replies with a `303`
* This redirect causes the client to `GET` the created or updated resource.

For our messageboard server, Post-Redirect-Get entails the following:
1. Go to http://localhost:8000/ in browser. Browser sends a `GET` request to teh server, which replies with a `200 OK` and a piece of HTML
2. Write a comment in the form and submit it. The browser sends it via a `POST` to the server.
3. THe server updates the list of comments, adding your comment to the lsit. Then it replies with a `303` redirect, setting the `Location: /` header to tell the browser to request the main page via `GET`.
4. The redirect response causes the browser to go back to the same page we started with, sending a `GET` request, which replies with a `200 OK` and a piece of HTML...and so on

### Exercise: Messagboard Part Three

Update the messageboard server to a full Post-Redirect-Get pattern as described above. 

Below is the code for the finished exercise and some notes on completing this exercise.

1. Send a 303 redirect back to the root page.
   * The key realizations here were: 
     * Each separate type of header needs to have a distinct `self.send_header` line, and the first argument in this defines which type of header we're creating
     * `Location: /` must be separated in the `.send_header` arguments

2. Put the response together out of the HTML form and the stored messages
   * For this I just looped over the stored messages, adding each message to a string `full_msg`
   *  At the end of the long string of messages, I added the HTML form, so that it would always be displayed at the bottom of the page.
     * I could have gotten more complicated with this (ex: Add in some HTML formatting between/around each message in the list to separate things out), but for now this meets the requirements of the exercise

3. Send the response
   * Simple...use `self.wfile.write` juse like we have in the past

```python
import http.server as hs
import urllib

memory = []

msg_html = '''
<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST" action="http://localhost:8000/">
    <textarea name="message"></textarea>
    <br>
    <button type="submit">Post it!</button>
  </form>
'''

class MessageHandler(hs.BaseHTTPRequestHandler):
    def do_POST(self):
        # How long was the message? (Use the Content-Length header.)
        length = int(self.headers.get('Content-Length', 0))

        # Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()

        # Extract the "message" field from the request data.
        message = urllib.parse.parse_qs(data)['message'][0]

        # Escape HTML tags in the message so users can't break world
        message = message.replace("<", "&lt;")

        # Store it in memory.
        memory.append(message)

        # 1. Send a 303 redirect back to the root page.
        self.send_response(303)
        self.send_header('Content-type', 'text/HTML; charset=utf-8')
        self.send_header('Location', '/')
        self.end_headers

        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode())
    
    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # 2. Put the response together out of the form and the stored messages.
        full_msg = ''
        for msg in memory:
          full_msg = full_msg + '\n' + msg
        
        full_msg = full_msg + msg_html
        # 3. Send the response.
        self.wfile.write(full_msg.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = hs.HTTPServer(server_address, MessageHandler)
    httpd.serve_forever()

```

## Making Requests

Python has a module called `requests` which we can use to make HTTP requests in a straightforward way. The documentation for this module is here: https://2.python-requests.org//en/master/user/quickstart/

A few things we learned in this section:
* We can make a `GET` request with `requests.get(<URI here>)`
* When we send a request, we get back a response object:
```python
>>> import requests
>>> a = requests.get('http://www.udacity.com')
>>> a
<Response [200]>
>>> type(a)
<class 'requests.models.Response'>
```
* If we send request to a non-existent site we should get a Python Exception
* If we send a request to a non-existent *page* on a real site, we should get a `.status_code` which is an HTTP error code (like 404)

## Using a JSON API

JSON is a compact and reaable data format based on the syntax of JavaScript, often used for web-based APIs. Many services let you send HTTP queries and get back structure data in JSON format. JSON data types are:
* Strings
* Numerics
* Boolean - True/False
* Arrays - An ordered list of 0 or more values, where each value many be of any type. (these are like Python lists)
* Objects - An unordered collection of name:value pairs where names (also called keys) are strings, and values can be of any type. (analagous to a Python dictinoary)

JSON data always starts and ends with curly brackets, here are examples of the data types:
```json
{
    "title":"JSON Notes",       // string
    "numCharacters":642,        // number
    "finished":false,           // boolean
    "topicCategories":[         // array
        "Computer Science",
        "Knowledge"
    ],
    "statistics":{              // object
        "viewCount": 12603,
        "numLines":"thirteen"
    }
}
```
Python has a built-in `json` module, and the `requests` module makes use of it. A `Response` object has a `.json` method; if the response data is JSON, you can call this method to translate the JSON data into a Pyhton dicitonary.

### Exercise: Use JSON with UINames.com

`UINames.com` is a website which produces imaginary user information, and can transmit it in JSON format. We'll use it to practice decoding JSON data, and extracting the parts we need. The solution code is below:
```python
import requests

def SampleRecord():
    r = requests.get("http://uinames.com/api?ext&region=United%20States",
                     timeout=2.0)
    # 1. Add a line of code here to decode JSON from the response.
    resp = r.json()
    
    return "My name is {} {} and the PIN on my card is {}.".format(
    # 2. Add the correct fields from the JSON data structure.
    resp['name'],
    resp['surname'],
    resp['credit_card']['pin']
    )

if __name__ == '__main__':
    print(SampleRecord())
```



