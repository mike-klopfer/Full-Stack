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

## 12. Removing things (rm, rmdir)

## 13. Searching and pipes (grep, wc)

## 14. Shell and environment variables

## 15. Startup files (.bash_profile)

## 16. Controlling the shell prompt ($PS1)

## 17. Aliases

## 18. Keep learning!