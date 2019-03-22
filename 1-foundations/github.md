# Git Notebook

# Version Control

## What is Version Control

Version control is a set of programming tasks combined with some code which when used together allows tracking of changes to a codebase over time and across multiple programmers. Git implements distributed version control in which a codebase can be replicated in a local repository at the workstation of each person working on the code.

## Version Control in Daily Use

* Most of us use version control every day if we use the undo-redo features of our document editors, and in these cases we're using something more like Google Docs revision history
* As good as this isn't powerful enough for programming
* Notably, we're missing the abilities to ...
  * label a change
  * give a detailed explanation of why a change was made
  * move between different versions of code
  * undo change A, make edit B, then get back change A with out affecting edit B


## Git and Version Control Terminology

### Version Control System / Source Code Manager

* A **version control system** (VCS) is a tool that manages different versions of source cod. A **source code manager** (SCM) is another name for a version control system. Git is an SCM (and thus a VCS)

### Commit

* Git thinks of its data like a set of snapshots of a mini filesystem. Every time you **commit** (save the state of your project in Git), it basically takes a picture of what all of your files look liek at that moment and stores a reference to that snapshot.

* Everything you do in Git is to help you make commits, so a commit is then the fundamental unit in Git.

### Repository

* A **repository** is a directory which contains your project work, as well as a few hidden files which are used to communicate wiht Git. Repositories can exist either locally on your computer or as a remote copy on another computer. A repository is made up of commits.

### Working Directory

* The **Working Directory** is the collection of files that you see in your computer's file system. When you open your project files up on a code editor, you're working with files in the Working Directory.

### Checkout

* A **checkout** is when content in the repository has been copied to the Working Directory

### Staging Area / Staging Index

* A file in the Git directory that stores information about what will go into your next commit. Think of **staging** like a preparatory step just prior to a commit where we double check to make sure we have included just the files that we want to include in a commit.

### SHA

* A **SHA** is used to identify each individual commit. It is a 40-character string composed of characters (0-9 and a-f) and calculated based on the contents of a file or directory structure in Git. SHA is short for Secure Hash Algorithm.

### Branch

* A **branch** is when a new line of development is created that diverges from the main line of development. This alternative line of development can continue without altering the main line.

### How do these things interact?

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

## Getting Started

* Create account at github.com
* Download git software
* Set config values
  * Set up our local system with the useer name and email we plan to use:
```
$ git config --global user.name <your    name here>
$ git config --global user.email<your email here> 
```


# Create a Repository

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
  * This creates a `.git` directory within the current working directory which contains all of the files related to
   tracking our project directory
* Now that we've specified which directory we want to track, we need to indicate 
  to git that we intend to stage all of the files in the directory for storage 
  in the remote repository.
  * We can do this using `$ git add -A` or `$ git add .`
    * The `-A` flag adds all files and directories in the current working directory, and the `.` refers to the current working directory.

## Clone an Existing Repository

## Determine a Repository's Status

* We do this with `$ git status`
  * Returns info about what state git is in, specifically
    * What branch we are on
    * If the branch of our local repository is up-to-date with the remote (master) repository
    * Whether we have any un-tracked (not-staged) changes
    * Whether we have any files waiting in the staging area to be commited
    * ...and more depending on what additonal flags we use
  * Some useful flags with `git status`:
    * add these later


## Reviewing a Repository's History

* Git autmatically records the date and time of every commit
* Top help us track what we've done in our project, its useful to make commits often with descriptive messages


* We can use `$ git log` to see what we've done in the past
  * This gives usa list of all the commits in the current repository, who made them, when they were made, and the SHA associated with the commit
  * Display in reverse chronological order (newest to oldest)
  * Scrollable
  * Exit by pressing `q, Enter`
* Some useful flags wtih `git log`:
  * `--oneline`: display just part of the SHA and the commit message
  * `--stat`: display how many files were chnaged, and the number of insertions/deletions
  * `--patch`: display, for each commit EXACTLY what lines were added and deleted (press `Enter` to get more out put, then scrollable)

* We can also use `$ git show` to view a specific commit
  * Without an additional argument shoes the last commit
  * Can see an specific commit by adding the SHA after show...`git show fdf5493`
  * The output is the same as the `git log --patch`, but for only one commit


## Add Commits to a Repository

* `git add`
  * Write some stuff
* `git commit`
  * Write some stuff about commits
  * Writing commit messages
    * Each commit subject line should be able to answer the following question:
    * If applied this commit will *[your subject line here]*
    * Then the structure of the commit should be as follows:
```
Imperative commit title (limited to 50 characters)
# Blank line
- More detailed commit message body
- List of key points and updates that the commit provides
- Lines need to be manually wrapped at 72 characters
```