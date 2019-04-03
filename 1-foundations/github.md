# Git Notebook

# Version Control

## Quick Summary

* Setup
  * `git config`
  * `git init`
* Repository Status
  * `git status`
  * `git log`
  * `git diff`
* Basic Committing
  * `git add`
  * `git reset`
  * `git commit`
* Taggging, Branching, Merging
  * `git tag`
  * `git branch` 
  * `git merge`
  * `git checkout`

## What is Version Control

Version control is a set of programming tasks combined with some code which when used together allows tracking of changes to a codebase over time and across multiple programmers. Git implements *distributed version control*, in which a codebase can be replicated in a local repository at the workstation of each person working on the code.

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
$ git config --global user.name <your name here>
$ git config --global user.email <your email here> 
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
  * We'll see how to do this soon using `$ git add`, but first we'll take a quick detour to see how we can *clone* a repository from outside of our local directory, and find out the status of whatever repository we happen to be working in.

## Clone an Existing Repository
* *add stuff here*

## Determine a Repository's Status

* We do this with `$ git status`
  * Returns info about what state our repository is in, specifically:
    * What branch we are on
    * If the branch of our local repository is up-to-date with the remote (master) repository
    * Whether we have any un-tracked (not-staged) changes
    * Whether we have any files waiting in the staging area to be commited
    * ...and more depending on what additonal flags we use
  * Some useful flags with `git status`:
    * add these later


# Reviewing a Repository's History

## Display a Repository's Commits

* Git autmatically records the date and time of every commit
* To help us track what we've done in our project, its useful to make commits often with descriptive messages
* We can use `$ git log` to see what we've done in the past
  * This gives us a list of all the commits in the current repository, who made them, when they were made, and the SHA associated with the commit
  * Displays in reverse chronological order (newest to oldest)
  * Scrollable
  * Exit by pressing `q, Enter`
* Some useful flags wtih `git log`:
  * `--oneline`: display just part of the SHA and the commit message
  * `--stat`: display how many files were chnaged, and the number of insertions/deletions
  * `--patch`: display, for each commit EXACTLY what lines were added and deleted (press `Enter` to get more out put, then scrollable)

* We can also use `$ git show` to view a specific commit
  * Without an additional argument, this shows the last commit
  * We Can see an specific commit by adding the SHA after show...`git show fdf5493`
  * The output is the same as the `git log --patch`, but for only a single commit


# Add Commits to a Repository

## Git Add

* Before we commit anything, its useful to check the status to see which files have changes, and to understand the curernt state of our repository.
* Staging files with `git add`
  * We have some files that we want Git to start tracking
  * For Git to track a file it needs to be committed to the repository
  * For a file to be committed, it needs to be in the staging index
  * `git add` followed by a list of filenames (separated by a space) moves the specified files into the staging area
    * Note: if we stage the wrong files, we can 'unstage' by using `git reset`, and then restaging the correct files
  * Rather than specifying individual files to stage, we can also stage the entire directory with the `-A` flag or the `.` special character

## Git Commit

* Commiting files with `git commit`
  * Once we've added all of the files we want to commit to the staging area, we should run `git status` one more time to make sure the staged files are the ones we want to commit
  * When we're ready to commit, we type `git commit `
  * Once we do this a vim editor will open, and we can type our commit message (witih the format as previously discussed)
  * Writing commit messages
    * Each commit subject line should be able to answer the following question:
    * If applied this commit will *[your subject line here]*
    * The structure of the commit should be as follows:
```
Imperative commit title (limited to 50 characters)
# Blank line
- More detailed commit message body
- List of key points and updates that the commit provides
- Lines need to be manually wrapped at 72 characters
```
* When our commit message is complete, we press save the message to commit the files and message to the local repository!

## Git Diff

* `git diff` tells us what uncommitted changes exist in our project
* An example of when this might be useful is if we are working on our project, and are interrupted, but forget to commit the changes we had made. When we come back to continue working we've forgotten exactly what we changed, and as we know from our lesson on commit messages, its important to know what we've done so that we can write accurate commit messages.
* `git diff` gives us the same output as `git log -patch`, which is
  * The files that have been modified
  * The location of lines that have been added or removed
  * The acutal (character by character) changes that have been made

## Having Git Ignore files

* Often when we want to commit multiple file changes, we'll use `git add .` to stage everything in the cwd
* A `.gitignore` file enables us to use this simpple syntax AND still exclude certain files from being staged
  * A `.gitignore` file is just a text file with a list of the names of files in the directory that we don't want Git to track
  * In a `.gitignore` we can also use wildcards (to ignore all instances of a certain type of file)...and...
  * ...regular expressions, to ignore files with a certain structure to their name, `.gitignore` uses the following conventions:
    * Blank lines for spacing
    * `#` is a comment
    * `*` matches 0 or more characters
    * `?` matches 1 character
    * `[abc]` - match a, or b, or c
    * `**` - matches nested directories - `a/**/z` matches
      * `a/z`
      * `a/b/z`
      * `a/b/c/z`
    * Example: Assuming we have 50 pictures in our project directory, and that we don't want Git to track any of them. They are all `.jpg`, and all in a subdirectory called `samples`. We would use `samples/*.jpg` in our `.gitignore` file to accomplish this.

# Tagging, Branching, and Merging

## Git Tag

* At some point in the course of working on our project, our code will reach a state where it is functional: running with all major required features, and having had the required amount of testing completed. The code may still have undiscovered bugs, but at this point we would say it is a 'releasable' version, and we might to label this as version 1.0.
* To do this, we would use the `git tag` commmand:
* Assuming the most recent commit is what we consider to be v1.0
* Then to tag this most recent commit with the appropriate tag we type:
  * `$ git tag -a v1.0`
    * The `-a` flag is the *annotate* version, which includes quite a bit more information about the commit that we've tagged, and is preferred in almost all cases.
    * We can optionally add a `-m` flag with a message, or leave it off and have Git take us into the editor to add a message if we want to add a detailed message.
* If we need to tag a previous commit we simply add the SHA (or part of it) after the tag like so:
  * `$ git tag -a v0.9 a39ckrkf9`
* Finally, we can use `git tag` on its own to display a list of all the tags associated with our repository.
* A Tag can be deleted by typing:
  * `$ git tag -d v1.0`

## Git Branching

### What is Branching?

* By default the first branch name is master
* When a commit is made, its added to the *branch*, and the *branch pointer* moves to point at it.
  * Thus, a branch pointer always points at the most recent commit on the branch, in contrast to a tag pointer, which stays fixed on a single commit.
* *Branches* let us work on the same project in different, isolated environments
* The *Head* pointer is an additional pointer, 
  * The Head pointer always points to the branch that is active, and...
  * We can change where Head is pointed using the `git checkout` command
* Our commits are always added to wherever the head pointer is pointing
  * Its imporant to note that as we add commits to a certain branch, other branches do NOT get any of the changes we have made (until we merge the branches...which we'll cover later)
  * We can also create branches from any past or current commits...so if we find a problem in our code which has propogated through several commits, we can go back to the last commit that doesn't have the error, and work forward from there.

### The `git branch` command

* The `git branch` command is used to interact with Git's branches
* It can be used to 
  * list all branch names in the repository
    * We use `git branch` with no other arguments to do this
  * create new branches
  * delete branches

### Create a Branch

* Using `git branch <branch-name>`
* After we create a branch, the head pointer stays where it was until we change it...it does NOT automoatically switch to the new branch

### The `git checkout` command

* This command will:
  * remove all files and directories from the current working directory that Git is tracking (files that Git tracks are stored in the repository, so nothing is lost as long as our commits are up to date)...and...
  * ...got into the repository and pull out all of the files and directories of the commit that the branch points to
* Since this command removes all of the files that are reference by commits, its important to commit any changes and run `git status` before we `git checkout`
* In some cases, two branches will point at the same commit, and the only way to know which branch we are on is to run `git status`, `git log`, `git branch`, or to look at our prompt (if we have it configured to display this)

### Branches in the Log

* We can very clearly see branch information in the log if we type `git log --decorate`

### The Active Branch

* Depending on how we have our .bash_profile (or .bashrc) set up, the command prompt will display the active branch.
* If we don't have our prompt confiured, the fastest way to know what branch we are on is to use the `git branch` command. An asterisk will appear next to the name of the active branch.

### Deleting a Branch

* Once we've merged any changes from a branch back into the master branch, we'll want to delete the branch. 
* We can delete a branch with the `-d` flag, so we'd type
  * `git branch -d <name of branch to delete>`
* Git won't let us delete a branch that has commits that aren't on any other branch. So if we create the `sidebar` branch, added commits to it, and then tried to delete it with `git branch -d sidebar`, Git would not let us.
  * The only way to delete a branch with commits that aren't on another branch is to use the `-D` flag.

## Merging

* Git can automatically combine the changes on different branches
* How does merging work? See example below.
  * When a merge happens, it makes a commit
  * Wherever the head pointer is, the merge commit will be placed there, and that branch will move forward, with the same branch name
  * In this example case, we'll see a **Regular Merge Commit**, which links two different earlier commits, with the `git merge sidebar` command
    * This doesn't effect the sidebar branch, we can switch back to it and still make commits, BUT changes to Sidebar after the merge won't be propogated to Master until another merge.
 
Before Merge 
* Commit with SHA 1... is on the Master
* Commit with SHA b... is on Sidebar 
```
             b--1   : Master (Head)
e==2==a==3 <      
             7--b      : Sidebar

```
After Merge
* Commit 8... is on Master
* Commits 7, b are on Master *AND* Sidebar
```

             b--1--8    : Master (Head)
e==2==a==3 <     /
             7==b      : Sidebar

```
* We could also have a **Fast-Forward Merge Commit**, if we have a branch with commits *ahead* of the master. In this type of merge, the Master branch pointer is just moved to point at the "future" commit in the more developed branch.

### KNOW THE BRANCH

* Its very imoprtant to know which branch you're on when you are about to merge branches together. Remember that making a merge makes a commit.

### The Merge Command

* The `git merge` command is used to combine Git branches:
```
$ git merge <name-of-branch-to-merge-with-current-active-branch>
```

* When a merge happens, Git will:
  * look at the branches that it's going to merge
  * consider the history of the branch's to find a single commit that *both* branches have in their commit history
  * combine the lines of code that were changes on the separate branches
    * generally speaking, Git will try to get all the features that were changed in both branches and include all of those changes into a single commit. If there is a conflict where the *SAME* line of code is changed in different ways in both branches, Git will have an error and will need programmer intervention to proceed. We'll cover this more later
  * make a commit to record the merge

* Fast-forward Merge
  * This is basically a merge used to bring one branch up to speed with another branch which is ahead in development. In the example below, we have some feature in the `footer` branch (which has been developed further than our master branch), and now that we know everything in `footer` is working, we want to incorporate it into the master branch.
  * A Fast-forward merge will just move the currently checked out branch *forward* unitl it points to the same commit that the other branch (in this case footer) is pointing to.
  * We do this by switching to the `master` branch, then running `$ git merge footer`.
  * The two diagrams below display the before and after of this type of merge:

Before Fast-forward merge
```
e==2==a--3--z--7
      |        |
    master    footer
```
After Fast-forward merge
```
e==2==a==3==z==7
               |
              master,footer
```

* Regular Merge
  * A regular merge combines two divergent branches
  * The actual commant is very similar, and the result is diagrammed in the earlier **Merging** section.
  * Its important to remember that whichever branch the HEAD pointer is pointing at, is the branch that will have the merge commit.