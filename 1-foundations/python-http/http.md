# HTTP and Web Servers

## First Web Server

* HTTP was originally created to serve hypertext documents, but today is used for many things
* An HTTP transaction always involves a client and a server
* We use HTTP clients all the time (like web browsers)
* Browsers send HTTP requests to web servers, and servers send responses back to browsers
  * Loading a page may take many requests, sometimes to different servers. A video might be stored on one server while the webpage with the video built in is stored on a different server. When we visit the page, then try to watch the video we actually send (at least) two requests, one to get the information about the page then another to get the video
* Browsers are not the only web client around
* HTTP is powerful and widely supported, so it's a common choice for programs that need to talk to each other across the network.
* As regular users of the internet we're pretty familiar with the client side of things, but what about the other end...the server?
* A web server can be much simpler than a browser because it must only do one thing: handle incoming requests
* The Python `http.server` module, can run a built-in web server on your computer. 
  * Note: this is just a simple demo server, not a production level one...it implements only limited security checks

### Demo Web Server
* In a terminal cd to a directory that has some files in it
* Run `python -m http.server 8000`
* This will return a message that we are serving HTTP on 0.0.0.0 port 8000. More on what this means later, but for now lets investigate with a web browser
* In a browser type `http://localhost:8000`
* When we do this, our browser sends a HTTP request to the Python server we implemented in the terminal. 
  * Specifically, we will see displayed all of the files in the directory where we ran the server


### What is a server anyway?

* A server is a program that accepts connectinos from other programs on the network
  * When you start a server program, it waits for clients to connect to it - like our demo server waiting for the web browser to ask it for a page. 
  * Then when a connection comes in, the server runs a piece of code -like calling a function- to handle each incoming connection.
* While our server was running it displayed a log with information related to each interaction with a client. In the next section we'll go in to detail on what the different parts of the log tell us.

## Parts of a URI
* A web address is also called a URI (for Uniform Resource Identifier)
* A URI is a name for a *resource*, such as a Wikipedia article, video on the web, or a data source like the Google Maps API.
  * This is similary but slightly different to a URL (Uniform Resource Locater). A URL is a URI for a resource on the network.
* A URI has three visible parts, separated by punctuation. Take `https://en.wikipedia.org/wiki.Fish` as an example:
  * `https` is the **scheme**
  * `en.wikipedia.org` is the **hostname**
  * `/wiki/Fish` is the **path**

### Scheme
* The first part of URI is the **scheme** which tells the client how to go about accessing the resource. Some examples of URI schemes are: `http`, `https`, and `file`. File URIs tell the client to access a file on the local file system. HTTP and HTTPS URIs point to resources served by a web server
* HTTPS URIs use an encrypted connection
* There are many other URI schemes...the official list is here: http://www.iana.org/assignments/uri-schemes/uri-schemes.xhtml

### Hostname

* In an HTTP URI the **hostname** appears after the scheme -- something like `www.udacity.com` or `localhost`
* The hostname tells the client which server to connect to
* Note that when embedding a link in an HTML document, we cannot only include the hostname (like `www.google.com`), instead we must also include the scheme

### Path

* In an HTTP URI, the **path** appears after the hostname
* This path identifies a particular resources on a server
  * Since a given server can have many resources on it, the path tells the server exactly which resource the client is looking for
* In the real world, paths don't *necessarily* correspond to specific file names
  * We might do a Google search, and see a URI path like `/search?q=ponies`
  * In cases like this, the server interprets the path, then sends back a search result page (that maybe never existed before)
  * If we write a URI *without* a path, the browser fills in the default path `/`...the root (this is not necessarily the root of the server, rather its the root of the resources served by the web server)

### Relative URI references

* Some URI's dont have a scheme or a hostname
* These are **Relative URI References** and they are relative to the context in which they appear
* Since they don't include a scheme or a hostname, the client has to figure it out from context
  * If we click on one of these, the browser knows that it needs to fetch it from the same server that it got the original page from.

### Other URI parts

* We've already seen **queries**, indicated with a `?q=<something>`
* We can also have **fragments** which get a specific part of an HTML page, liked by HTML `id` tags


## Hostnames and Ports

### Hostnames

* A full HTTP or HTTPS URI includes the hostname of the web server, like www.udacity.com
* A hostname in a URI could also be on IP address (if you put `http://216.58.194.174/` in the browser you end up at Google)
* The internet is distinguished into parts by **IP addresses**
  * Every piece of network traffic on the Internet is labeled with the IP address of the sending and receiving computers
  * In order to connect to a web server a client needs to trnaslate the hostname into an IP address.
  * The Operating systems network configuration does this by using the Domain Name Service (DNS)
    * DNS is a set of servers maintained by Internet Service Providers and other network users to look up hostnames and get back IP addresses.
  * In the terminal we can use the **host** program to look up hostnames in DNS:
```
$ host www.google.com
www.google.com has addresss 216.58.194.164
www.google.com has IPv6 address 2607:f8bo:4005:804::2004
```
* IP addresses come in two different varieties: the older IPv4 and the newer IPv6.
  * An address like `127.0.0.1` or `216.58.194.164` are IPv4 addresses
  * An address like `2607:f8bo:4005:804::2004` is an IPv6 address, but in some cases they can be abbreviated

### Localhost

* The IPv4 address `127.0.0.1` and the IPv6 address `::1` are special addresses that mean "this computer itself"
  * Used when a client is accessing a server on your own computer
  * The hostname localhost refers to these special addresses
* When we ran our Python demo server earlier, a message was printed saying that the server is listening on `0.0.0.0`
  * This is a special code for "every IPv4 address on this computer"

### Ports

* When we told our browser earlier to connect to the demo server, we gave it the URI `http://localhost:8000/`
  * This URI has a port number of 8000
  * Most web addresses out on the internet don't have port numbers, the client usually figures out the port number from the URI scheme
    * For instance, HTTP URI's imply a port number of 80
    * Whereas, HTTPS URI's imply a port number of 443
  * Since we want our Python demo web server to run on port 8000 (which is not the default), we need to write the port number in the URI for it

#### What is a port number anyway?
* All network traffic that computers send and receive (everything from web requests to login session to file sharing) is split into messages called **packets**.
* Each packet has the IP addresses of the computer that sent it, adn the computer which should receive it
* With the exception of some low-level packets, each packet ALSO has the port number for the sender and receiver
* IP addresses distinguish computers, port numbers distinguish between *programs* running on the same computer.
* When a server starts up and begins "listening" on a given port, its telling its operating system that it wants to receive connections from clients on a particular port number
  * When a client (such as a web browser) "connects to" that port and sends a request, the OS knows to forward that request to the sever that's listening on that port

## HTTP GET Requests

* If we look at the server logs on the terminal where the demo server is running, when we request a page from the demo server, we get an entry like:
```
12.0.0.1 - - [08/Apr/2019 10:47:44] "GET /Untitled.ipynb HTTP/1.1" 200
```
* Lets break this down to see what each part is telling us:
  * `GET /Untitled.ipynb HTTP/1.1` - this is the text of the request line that the client (browser) sent to the server. This log entry is the server telling us that it received a request that literally said: "GET <some resource>"
  * This request has multiple parts that we need to breakdown too:
    * The word `GET` is the **method** or **HTTP verb** being used. `GET` is used by a client when it wants a server to send a resource
    * `/Untitled.ipynb` is the **path** of the resource being requested. Notice that the client doesn't send the whole URI...just the path (which is relative to the server its requesting from)
    * Finally `HTTP/1.1` is the **protocol** of the request...HTTP/1.1 is the most common variety 

## HTTP Responses