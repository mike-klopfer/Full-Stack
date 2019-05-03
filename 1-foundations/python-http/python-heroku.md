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



