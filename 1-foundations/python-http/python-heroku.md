# HTTP in the Real World

## Deploying to a hosting service

### Steps to deployment

1. Check your server code into a new local Git repository
   * Standard git process for adding new repo
2. Sign up for a free Heroku account
   * At https://signup.heroku.com/dc
3. Download the Heroku command-line interface (CLI)
   * Available on heroku website
4. Authenticate the Heroku CLI with your account: `heroku login`
5. Create Configuration files `Procfile`, `requirements.txt`, and `runtime.txt` and check them into your Git repository
   * `runtime.txt` should have the version of Python (`python-3.5.4`)
   * `requirements.txt` should have a list of required Python packages which are needed to run the application, for now just `requests>=2.12`
   * `Procfile` is used by Heroku to specify the command line for running the application. It can support running multiple servers, but for now we'll only be running a web server.
   * Heroku documentation here for process types: 
6. Modify your server to listen on a configurable port.
   * Heroku rund many users' processes on the same computer
   * Multiple processes cannot usually listen on the same port...so Heroku needs to tell our server which port to listen on
   * We can do this using an environment variable...a configuration variable that is passed to your server from the program that starts it (usually the shell)
   * Python code can access environment variables in the `os.environ` dicitonary. 
   * The names of environment variables are usually capitalized; and the environment variable we need here is called `PORT`
   * The port our server listens on is configured when it creates the `HTTPServer` instance, near the bottom of the server code in the `if __name__ == '__main__'` block
   * We can make it work with or without the environment variable like this:

```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, Shortener)
    httpd.serve_forever()
```
7. Create your Heroku app: `heroku create your-app-name`
    * Use `heroku create your-app-name` to tell Heroku about the app
    * We will access it at `https://your-app-name.herokuapp.com/`
8. Push your code to Heroku with Git: `git push heroku master`
   * If all goes well, the app will be accessible on the web
   * The URI will appear in the output from the `git` command

### Accessing server logs

If our app doesn't work, we can access the server logs at `https://dashboard.heroku.com/apps/<your-app-name>/logs`


## Handling More Requests

If we try to create a link where the target URI is the bookmark server's own URI we get an error becasue Python's `http.server` can only handle one request at a time, and when we do this we are performing both a `POST` and a `GET` request simultaneously. 

### Concurrency

Being able to handle two ongoing tasks at the same time is called *concurrency*, and the basic `http.server.HTTPServer` doesn't have it. 

We can add concurrency to the basic server by adding a mixin to the **HTTPServer** class. To do this we need to add the following code to our server:

```python
import threading
from socketserver import ThreadingMixIn

class ThreadHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    "This is an HTTPServer that supports thread-based concurrency."
```
...then further down at the bottom of our server code...
```python
if __name__=='__main__':
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = ThreadHTTPServer(server_address, Shortener)
    httpd.server_forever()
```

## What's an Apache or Nginx?

### Static Content and more

The Web was originally designed to serve *static content* (images, HTML files, videos, and other media stored on disk), not to deliver applications. Specialized web server programs -- like Apache, Nginx, or IIS -- can serve static content from disk storage very quickl and efficiently. They can also provide access contro, allowing only authenticated users to download particular static content. 

### Routing and load balancing

Some web applications have several different server components, each running as a separate process. A specialized web server can dispatch requests to the particular backend servers that need to handle each request. This is called *request routing* or *reverse proxying*

Some web apps need to do a lot of work on the server side for each request, and need many servers to handle the load. Splitting requests up among several servers is called *load balancing*  

Load balancing also helps handle conditions where one server becomes unavailable, allowing other servers to pick up the slack. A revers proxy can *health check* the backend servers, only sending requests to the ones that are currently up and running. This also makes it possible to do updates to the backend servers in stages without having an outage.

### Concurrent users

Handling a large number of network connections at once turns out to be complicated - even more so than pluggin concurrency support into your Python web service. 

It takes time for a server to respond to a request. The server has to receiver and parse the request, come up with the data that it needs to respond, and transmit the response back to the client. The network itself is not instantaneous; it takes time for data to travel from the client to the server. 

In addition, a browser is allowed to have multiple connections to the same server, for instance to request resources such as images, or to perform API queries.

All of this means that if a server ishandling many requests per second, there will be many requests in progress at once. These are sometimes called *in-flight requests* (the request has "taken off" from the client, but the response has not yet "landed" again back at the client). A web service must be able to handle many requests at the same time.

### Caching

Web services speed up their service by using a *cache*, a temporary storage for resources that are likely to be reuse. Web systems can perfrom caching in a number of places - but all of them are under control of the server that serves a particular resource. That server can set HTTP headers indicating that a particular resource is not intended to change quickly, and can be safely cached.

Caching usually happens in the following places:
* Browser caching - On the users browser (images from recently-viewed web pages)
* Web proxy - Can perform caching on behalf of many users
* Reverse proxy - Cache results so that they don't need to be recomputed by a slower application server or database

All HTTP caching is governed by *cache control* headers set by the server. More info here: https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching

### Capacity

Python code is capabale of sending images or video via HTTP, but we serve static requests out of cache (from a chace...or static web server) because - all else being equal - handling a request faster provides a better user experience. If your web service becomes popular you don't want it to bog down under the strain of more traffic...so it helps to handle different kinds of request with software that can perform that function most efficiently.

## Cookies

Cookies are a way that a server can ask a browser to retain a piece of information, and sit it back to the server when the browser makes subsequent requests. Every cookie has a name and a value, much like a variable in your code; it also has rules that specify when the cookie should be sent back.

What are cookies for?
* Used to tell clients apart...can then implement higher-level concepts on tomp of HTTP requests and responses - things like sessions and login
* Used by analytics and advertising systems to track user activity from site to site
* Used to store user preferences for a site

### How cookies happen

The first time the client makes a request to the server, the server sends back the response with a **Set-Cookie** header. This header contains three things: a cookie *name*, a *value* and some *attributes*. Every subsequent time the browser makes a request to the server, it will send that cookie back to the server. THe server can update cookies, or ask the browser to expire them.

### Seeing Cookies in your browser

Browsers don't make it easy to find cookies that have been set, because removing or altering cookies can affect the expected behavior of web services you use. What are all the pieces of data in a cookie? The eight most common fields are:
* 1)Name and 2)Content - analagous to dictionary Key and Value (respectively) in Python
* 3)Domain and 4)Path - describe the scope fo the cookie - that is to say, which queries will include it. By default, the domain of a cookie is the hostname form the URI of the response that set the cookie. A server can also set a cookie on a broader domain, within limits...for example a response from `www.udacity.com` can set a cookie for `udacity.com` but not for `com`
* 5)Secure (Send for) and 6)HttpOnly (Accessible to script) - boolean flags...if Secure is set to True, then the cookie will only be sent over HTTPS connections. If the HttpOnly flag is set, the cookie will not be accessible to JavaScript code running on the page
* 7)Created and 8)Expires - Deal with the lifetime of the cookie. If no expiration is set, then a cookie is expired whtn the browser closes.

### Using cookies in Python

To set a cookie from a Python HTTP server, all you need to do is set the `Set-Cookie` header on an HTTP response. Similarly, to read a cookie in an oncoming request, you read the `Cookie` header. Formatting these headers is a bit tricky...Python's `http.cookie` module provides handy utilities for doing so.

To create a cookie on a Python server, use the `SimpleCookie` class. This class is based on a dictionary, but has some special behavior once you create a key within it:

```python
from https.cookies import SimpleCookie, CookieError

out_cookie = SimpleCookie()
out_cookie["bearname"] = "Smokey Bear"
out_cookie["bearname"]["max-age"] = 600
out_cookie["bearname"]["httponly"] = True
```

Then you can send the cookie as a header form your request handler:
```python
self.send_header("Set-Cookie", out_cookie["bearname"].OutputString())
```

To read incoming cookies, create a `SimplyCookie` from the `Cookie` header:
```python
in_cookie = SimpleCookie(self.headers["Cookie"])
in_data = in_cookie["bearname"].value
```

If a request doesn't have a cookie on it, accessing the Cookie header will raise a `KeyError` exception. Likewise, if the cookie is not valid the SimpleCookie constructor will raise `http.cookies.CookieError`. For more documentation on cookie handling in Python see the documentation for `the http.cookies` module here: https://docs.python.org/3/library/http.cookies.html

### Exercise: A server that remembers you

We'll build a server that asks for your name, and then stores your name in a cookie on your browser. You'll be able to see that cookie in your browser's cookie data. Then when you visit the server again, it'll already know your name. Here is the starter code edited to the final solution:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
from http import cookies
from urllib.parse import parse_qs
from html import escape as html_escape

form = '''<!DOCTYPE html>
<title>I Remember You</title>
<p>
{}
<p>
<form method="POST">
<label>What's your name again?
<input type="text" name="yourname">
</label>
<br>
<button type="submit">Tell me!</button>
</form>
'''


class NameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # How long was the post data?
        length = int(self.headers.get('Content-length', 0))

        # Read and parse the post data
        data = self.rfile.read(length).decode()
        yourname = parse_qs(data)["yourname"][0]

        # Create cookie.
        c = cookies.SimpleCookie()

        # 1. Set the fields of the cookie.
        #    Give the cookie a value from the 'yourname' variable,
        #    a domain (localhost), and a max-age.
        c['yourname'] = yourname
        c['yourname']["max-age"] = 600
        c['yourname']["domain"] = 'localhost'

        # Send a 303 back to the root page, with a cookie!
        self.send_response(303)  # redirect via GET
        self.send_header('Location', '/')
        self.send_header('Set-Cookie', c['yourname'].OutputString())
        self.end_headers()

    def do_GET(self):
        # Default message if we don't know a name.
        message = "I don't know you yet!"

        # Look for a cookie in the request.
        if 'cookie' in self.headers:
            try:
                # 2. Extract and decode the cookie.
                #    Get the cookie from the headers and extract its value
                #    into a variable called 'name'.

                in_cookie = cookies.SimpleCookie(self.headers["Cookie"])
                name = in_cookie["yourname"].value

                # Craft a message, escaping any HTML special chars in name.
                message = "Hey there, " + html_escape(name)
            except (KeyError, cookies.CookieError) as e:
                message = "I'm not sure who you are!"
                print(e)

        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # Send the form with the message in it.
        mesg = form.format(message)
        self.wfile.write(mesg.encode())


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NameHandler)
    httpd.serve_forever()
```

Notes on steps in CookieServer.py
1. Set the fields of the cookie
   * The cookie was created using the `http.cookies` class `SimpleCookie`, and the instance was assigned to instance variable `c`.
   * In this instance, we assign to Name `yourname` and to Content the user input name from the HTML form at the `<input>` flag. 
   * We also set the Domain to `localhost` and we give a `max-age` value
   * The work of sending the cookie back to the server is done using the `.send_header('SetCookie',...)` line
2. Extract and decode the cookie
   * The default message is sent if `'cookie'` is not present in `self.headers`
   * If `'cookie'` is present, we enter a try-except block
     * This block tries to extract the Content (value) associated with the Name `yourname` cookie
   * Once extracted we set the variable `name` to be the Content (Value) of the cookie with Name (key) `"yourname"`

### DNS domains and cookie security

A DNS domain links a particular hostname to a computer's IP address. It also indicates that the owner of that domain intends for that computer to be treated as part of that domain. 

If an unscrupulous user could convince your browser that their server `evilbox` was part of (say) Facebook, and get you to request a Facebook URL from `evilbox` instead of from Facebook's real servers. Your browser would send your `facebook.com` cookies to `evilbox` along with that request. But these cookies are what prove your identity to Facebook, so the bad guy could use those cookies to access your Facebook account. 

In short: if a bad guy can take control of your site's DNS domain, they can send all your web traffic to their evil server...and if the bad guy can fool users' browsers into sending that traffic their way, they can steal the users' cookies and reuse them to break into those users' accounts on your site.

## HTTPS for security

### What HTTPS does for you

When a browser and server use HTTPS, they're still using the same protocol (HTTP), just over an encrypted connection. The encryption follows a standard protocol called Transport Layer Security, or  **TLS** for short. TLS does the following:
* **Privacy**: TSL Keeps the connection private by encrtypring everything sent over it.
* **Authentication**: TSL lets the browser authenticate the server, to prevent an imposter server from stealing cookies/data
* **Integrity**: TSL checks that data sent over the connection has not been accidentally or delibrately modified or replaced.

### Inspecting TLS on your service

Our Heroku app was deployed to an address with an `https://` prefix. We can find more information about the TLS on various browsers by checking their documentation. (most browsers have a lock or shield icon in the web address bar to indicate a secure connection)

### Keys and certificates

Server-side configuration for TLS consists of two pieces of data:
* Private key: Secret, held on the server and never leaves there
* Certificate: Sent to every browser that connects to that server via TLS. 

These two pieces of data are mathematically related to each other in a way that makes encryption possible. The server's certificate i sissued by an organization called a certificate authority (CA). The CA's job is to make sure that the server really is who it says it is (similar to what a notary does for documents).


### How does TLS assure privacy?

Data in the TLS certificate and the server's private key are mathematically related through a system called public-key cryptography. Wikipedia article here: https://en.wikipedia.org/wiki/Public-key_cryptography

In short, the two endpoints (browser and server)can securely agree on a shared secret which allows them to encrypt the data sent between them so that only the other endpoint (and not any eavesdropper) can unscramble it.

### How does TLS assure authentication?

As previously discussed, the CA (certificate authority) issues certifications to the companies who actually run their domains (i.e. the CA would issue a cert for udacity.com to the company which actually runs that domain). Each certificate also contains metadata that syat what DNS domain the certificate is good for. When a browser connects to a particular server, if the TLS domain metadata doesn't match the DNS domain, the browser will reject the certificate and provide a warning.

### How does TLS assure integrity

Every request and response sent over a TLS connection is sent with a message authentication code that the other end of the connection can verify.


## Beyond GET and POST

