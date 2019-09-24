# gitautopush

Watch a local git repository for any changes and automatically push them to GitHub.

Useful as a live synchronization tool for teaching.
Say you've got a Jupyter notebook (or a markdown file) that you are populating with code while
you are teaching a class. As you add content to the file, you'd like students
to have access to the "latest" version at any moment in time.

`gitautopush` lets you automatically track the latest changes to a git repository,
and automatically push them to GitHub. You
can then ask students to visit a GitHub or nbviewer link, and they
will be able to see any changes that you've made.

See the GIF below for an example.

![gitautopush demo](doc/images/demo.gif)

## Installation

You can install with pip:

`pip install gitautopush`

## Usage

First, make sure that you've got a GitHub repository cloned to a local folder.

Next, run `gitautopush` and point it to that folder:

```
gitautopush /path/to/my/repo/folder
```

`gitautopush` will begin watching this folder for any changes. When it
finds them, it will commit them and push the folder contents to GitHub.
It will also display some links that you can share with students to help
them follow along.

## Parameters

Below are parameters you can use to customize the behavior of Gitautopush.

* `--sleep <INT>` - the amount of time (in seconds) to wait in between
  attempts to synchronize.
* `--path <STRING>` - a path to the folder you'd like to watch and synchronize

## Tutorial via an example use-case

Here's a common use-case for `gitautopush`:

You're teaching a Software Carpentry bootcamp and you'd like to do your work
in a Jupyter Notebook. You have a "master copy" that you're working from, but you
don't want to give the whole thing to students ahead of time. Your plan is to
do your work in an empty notebook as students watch, and you'd like students
to have access to the latest version of the notebook at all times.

First, you **create an empty GitHub repository** which we'll call `gitautopush-demo`.
Next, we'll create a folder where we'll be doing our work:

Next, you **clone this empty repository to your computer**:

```
git clone https://github.com/choldgraf/gitautopush-demo
```

Now, run `gitautopush` and point it to the new folder. We'll
tell it to sleep for 10 seconds after each check:

```
gitautopush --path ./gitautopush-demo --sleep 10
```

`gitautopush` will print a few useful links, and begin checking the
folder for any changes. When it finds one, it will commit the change to
the repository and push the result. It will also print an **nbviewer link**
for any Jupyter notebook that is changed. You can share these links with
your students.

Finally, open a new terminal window and use it to launch an application
(e.g. Jupyter Lab, Jupyter Notbeook, or your own text editor) to edit
the content.

As changes are made, note the links that are provided and share them
with your students.

## Acknowledgements

This tools was first thought up by John Lee, then adapted as a Python module
by Chris Holdgraf.
