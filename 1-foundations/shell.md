# Shell Workshop Notebook

## 1. The Command Line

* Alternative to the GUI based interface
* More flexible than GUI style interfaces
  * Command line is programmable, so for instance we could write a script to rename files in bulk, or separate them based on their timestamps

## 2. Intro to the Shell

* Command line interface for running programs on our computer
* Type commands at a prompt, shell runs commands and shows you the output
* Frequently used because fast and flexible
* Majority of servers are deployed on Linux, which makes heavy use of shell for deployment and remote admin
* A terminal is a program that we use to interact with the shell
* Unix style shell is the professional standard
  * Comes standard on Mac or Linux

## 3. Windows: Installing Git Bash
* Skipped

## 4. Opening a terminal

* Terminal is in utilities folder on Mac
* Can have multiple terminals open at once
  * Each has its own instance of shell running


## 5. Your first command (echo)

* echo is a command which tells the shell to print whatever text is after it
``` 
$ echo Hello!
Hello!
```
* There are some characters that have a special meaining to the shell, and exclamation is one of these. If we run into one of these symbols, we can just put single quotes around what we want to echo to prevent these special characters from being interpreted by shell as something other than text

## 6. Navigating directories (ls, cd, ..)

* We can use the ls command to *list* the directories in current directory
* We can also type `ls Downloads` to view the contents of the *Downloads* directory which might be located inside our current directory
* Changing the directory the shell is looking at is accomplished using cd
  * After you cd into a directory, ls will show the contents of the new current directory which we changed into
  * Many shell commands default to looking at/working with the current directory
* We can go back a directory with the special command `cd ..` where the `..` stands for the parent directory
* Putting a `;` on the command line lets you run two commands in order, one after the other
  
## 7. Current working directory (pwd)

* The commmand `pwd` prints the working directory that the shell is currently looking at
* When shell prints the working directory it separates directory names with a forward slash, like on url's for webpages
* The entire string, composed of several directory names, which specifies our current directory is called a path
* Special Directory names
  * `..` parent directory
  * `.` current directory
  * `~` home directory

## 8. Parameters and options (ls -l)

* Many shell commands support options or 'flags' which turn on special behavior associated with a command
* Example: `ls -l` is an option to ls which prints out a more detail listing of files, the -l stands for long
* Another Example: The `*.<type>` is called *Wildcard* syntax, and lists all files of type `<type>` in the current working directory (or whatever directory we specify with the ls command)
  * So the command `$ ls -l Documents/*.pdf` will return a list of all files in the Documents directory whose filenames end in .pdf

## 9. Organizing your files (mkdir, mv)

* To make directories and move files in a GUI we end up doing a lot of dragging and dropping
* In a shell, we can do this with just a few commands
  * `mkdir` is a command which makes a directory
    * Note: we don't need to cd to a directory to make a sub-directory in it. Say we wanted to make a directory `Books` which will be contained in a directory `Documents`, which is in our home folder. So the path to the directory that we want to make would be `~/Documents/Books`. We can make the `Books` directory while in the home directory by typing the command `mkdir Documents/Books`.
  * `mv` is a command which moves a directory or file
    * In order to move something we need to specify where it is, (i.e. the current path to the file we want to move), and where its going, (i.e. the path to the *directory* we want to place the file in). 
    * Continuting our previous example, lets assume we have a file `Awesome Book.pdf` which is located in `Documents`, and we want to move it to the new directory we created, `Books`. We would do this by typing `mv 'Documents/Awesome Book.pdf' Documents/Books`. (we use single quotes around the first path to avoid escaping the spaces)
    * We could also move all items of a given file type from one directory to another using the wildcard, like so... `mv Documents/*.pdf Documents/Books`. This command would move all of our pdfs from `Documents` into `Documents/Books`.


## 10. Downloading (curl)

* If we want to download files from the web we use the `curl` command
  * stands for C-URL as in see-URL
* Can use curl to get the source code for any webpage
* Typing `curl 'http://google.com'` doesn't seem to work, it gets some HTML code which seems to want to send us somewhere else
* Typing `curl -L 'http://google.com'` adds the flag `-L` which tells `curl` to follow redirects.
  * This command will display the HTML for google in the terminal, but it doesn't save it anywhere useful
  * To save the code or file somewhere we need to add the `-o` flag, and specify the name of the output file we want to write to
    * Lets say we type 
  ```
  curl -o google.html -L 'http://google.com'
  ```
    * This would take all of the HTML for google.com and save it to a file called google.html, which shell will make in our current directory.
* The structure of this last command is somewhat common in shell commands
* We called a command `curl`, with a flag `-o` and two separate entities, where we want to put some data, and where we want to get the data that we want to put.


## 11. Viewing files (cat, less)

* We can view the contents of a file as output in the terminal by typing `cat <filename>`
  * cat is short for concatenate
  * The trouble with this is that it shows the whole file at once, and this might display so much output that it fills multiple screens
* Fortunately there is another command called `less`
  * Works similar to `cat`, but we can view the content screen by screen, even scrolling up and down with the arrow keys
  * We can also search for a specific word using the forward slash followed by the word we're looking for.
  * In `less` we use q to quit when we're done viewing a particular file


## 12. Removing things (rm, rmdir)

* `rm` is the command we use in shell to remove a file
  * If we `rm` a file it is permenantly gone, no questions asked, no recycle bin
  * We can get a little more warning by adding the -i flag
* `rmdir` is the command we use to remove a directory

## 13. Searching and pipes (grep, wc)

* `grep` is a shell command which allows us to search through a text file to find a line which contains a given (input) string. 
  * We use `grep` as follows: `$ grep <string to find> <file to search>
  * As we saw with `cat`, this will output all of the matching strings to the terminal, which might be more than we can handle.
* We use the pipe `|` to join two commands together, and pass data in between them
  * In the case of `grep`, we would like to pass the output to `less` so that we can have an easier time seeing what is returned.
  * Example: Assume we have a text file called `dictionary.txt`, and we want to search it for any word which contains the string 'shell', then send this output to `less` we would type...
```
$ grep shell 'dictionary.txt' | less
```     
  * The lines containing 'shell' would be immediately displayed in `less`, with operation as expected in that program.

* `grep` can also operate on input from another program (like `curl`), so we can pass data directly to `grep` from the web, without having to save it in a local file first.
  * Example: in the command below, the output from the `curl` command gets sent directly to the `grep fish` command
```
curl -L https://tinyurl.com/zeyq9vc | grep fish
```
* We could also pipe this data directly to `wc` to get a count of the number of returned words, or use the `-c` (for count) flag with grep to do the same thing

## 14. Shell and environment variables

* The shell is a little programming language, and so it also has variables
* We can assign values to the variable using the equals sign, but with no spaces:
```
$ numbers='one two three'
$ echo $numbers
one two three
```
* Here we place a dollar sign in front of the variable when we want to refer to it, and we can see that using echo with it returns the value we stored.
* There are two different kind of variables...*Shell variables* like the numbers we made above...and
* *Environment variables*
  * These environment variables are shared with programs that we run from within the shell
  * The `PATH` variable is an example of this
    * We can see the PATH variable by typing `$PATH`
  * The purpose of the `PATH` variable is to tell shell where the program files are so when we type a command, it knows where to look to find the command we want to run
  * Often, the shell commands will be in the `/bin` directory
  * Sometimes we need to add on to the `PATH` variable so that shell knows to look somewhere else for new commands
    * The directories in the `PATH` variable are separated by colons, and shell searches them left to right
    * If we need to add the new directory to the end of `PATH` we do it by typing `$ PATH=$PATH:/new/dir/here`
    * This change will only last until we close the current terminal

## 15. Startup files (.bash_profile)

* Files containing shell commands are called *shell scripts*
  * This course won't cover much shell programming
* There is one file that is very usable to everyone who uses the shell
  * This is the shell configuration file
    * Most common use of config file is to add the /bin directory to `PATH`
  * There are a few different files that shell uses as configuration files
  * On Mac (or Windoes with git bash) the config file is `.bash_profile`
    * ...and we can access this file from any directory by typing `open .bash_profile`
  * On Linux the .bash_profile is only used for login shell sessions
    * Non-login shell sessions use `.bashrc` as the config file
* Any Command we put into the config file will automatically be run everytime we start the terminal


## 16. Controlling the shell prompt ($PS1)

* When we start a terminal we see a shell prompt
* We can change our shell prompt in the config file (`.bash_profile)
  * By changin the `PS1` shell variable we can change what is displayed in the prompt
  * The bash manual...`$ bash man`...gives us information on what we can put in the prompt (amogst other things)
  * There is a website available (http://bashrcgenerater.com) which we can use to construct long and complicated prompts

## 17. Aliases

* Use the `alias` command to assign a long command to a short command
  * Example: If we type `$ alias ll='ls -la'` then everytime we type `ll` at the prompt shell interprets it as if we had typed `ls -la`. 
* To see a list of all currently assigned aliases, just type `alias` at the prompt
* The aliased commands last only as long as the terminal window is open
  * As usual, we can make them sticky by adding them to the .bash_profile

## 18. Keep learning!