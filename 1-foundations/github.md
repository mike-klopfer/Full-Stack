# Git Notebook

## Getting Started

* Create account at github.com
* Download git software
  
## Creating First Repository

* Assume we have a codebase on our local machine which we want to store remotely 
* In this case we'll be storing it on GitHub, but we could also store it to a network machine by using the appropriate URL
* Change directory to the highest level folder we want to use version control for
  * Suppose we have the following file structure
``` \projects\new-project\<many files and directories which contain all of the code we want to track>```
  * In this case we would `$ cd new-project`
* Once our cwd is set accordingly, we start the process of tracking our code by typing at the command line `$ git init`
  * This creates a `.git` file which tells git that we want to track this directory

