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

* 

## 8. Parameters and options (ls -l)

## 9. Organizing your files (mkdir, mv)

## 10. Downloading (curl)

## 11. Viewing files (cat, less)

## 12. Removing things (rm, rmdir)

## 13. Searching and pipes (grep, wc)

## 14. Shell and environment variables

## 15. Startup files (.bash_profile)

## 16. Controlling the shell prompt ($PS1)

## 17. Aliases

## 18. Keep learning!