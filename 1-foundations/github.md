# Git Notebook

## Getting Started

* Create account at github.com
* Download git software
* Set config values
  * Name and Email using
```
$ git config --global user.name <your    name here>
$ git config --global user.email<your email here> 
```

  
## Creating First Repository

* Assume we have a codebase on our local machine which we want to store remotely 
* In this case we'll be storing it on GitHub, but we could also store it to a 
  network machine by using the appropriate URL
* Change directory to the highest level folder we want to use version control for
  * Suppose we have the following file structure
``` 
\projects\new-project\<many files and directories which contain all of the code we want to track>
```
  * In this case we would `$ cd new-project`
* Once our cwd is set accordingly, we start the process of tracking our code by
   typing at the command line `$ git init`
  * This creates a `.git` directory which contains all of the files related to
   tracking our project directory
* Now that we've specified which directory we want to track, we need to indicate 
  to git that we intend to stage all of the files in the directory for storage 
  in the remote repository.
  * We can do this using `$ git add -A` or `$ git add .`
* To really understand what is happening when we do this lets quickly pause to
   look at the version control process used by git

## How does git implement version control?

Version control is a set of programming tasks combined with some code which when
used together allows tracking of changes to a codebase over time and across 
multiple programmers. Git implements distributed version control in which a 
codebase can be replicated in a local repository at the workstation of each 
person working on the code.


| What are we doing? | Working Directory | Staging Area | Local Repository | Remote repository |
|:------------------:|:-----------------:|:------------:|:----------------:|:-----------------:|
| Writing new code or making changes to existing code that is in our local repository  | X | | | |
| `git add` to tell git that we have changes we want to send to the remote repository | -> | X | |
| `git commit` to store the changes in the staging area to our local repository | | -> | X | |
| `git push` to send our version of the local repository to the Remote repository to be in the new codebase for all other users to see | | | -> | X |
| `git pull` to 'checkout' code from the remote repository and pull it to our local repository. Once we've done this we can start making changes to the code | X | | | <- |

So in a normal git workflow we would
* Checkout the code from the remote repository using `git pull`
* Make changes or write new code in the directory tracked by git
* **Stage** changes for tracking with `git add`
* **Commit** the staged changes to the local repository with `git commit`
* Update the remote repository with our commits since checkout with `git push`

We'll talk in more detail about the specific syntax later, but this is a generic
look at how we would use git as part of our workflow.

