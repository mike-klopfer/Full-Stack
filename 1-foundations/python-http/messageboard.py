#!/usr/bin/env python3
#
# Step one in building the messageboard server:
# An echo server for POST requests.
#
# Instructions:
#
# This server should accept a POST request and return the value of the
# "message" field in that request.
#
# You'll need to add three things to the do_POST method to make it work:
#
# 1. Find the length of the request data.
# 2. Read the correct amount of request data.
# 3. Extract the "message" field from the request data.
#
# When you're done, run this server and test it from your browser using the
# Messageboard.html form.  Then run the test.py script to check it.

#from http.server import HTTPServer, BaseHTTPRequestHandler

#import http.server
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