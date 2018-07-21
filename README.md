# TOC-Generator
A table of contents generator for markdown, written in python.  Inspired by many of the table-of-contents generators that already exist, particularly [markdown-toc](https://github.com/jonschlinkert/markdown-toc).

# Premise
I maintain a [github project](https://github.com/Chris3606/GoRogue) that has a wiki, and needed a lightweight method to automatically generate tables of contents for select pages.  I wanted to automatically insert and update those tables of contents with minimal effort.  Thus, I created a python script to accomplish this.

# Installation/Prerequisites
The system consists of a single python script, requiring >= Python v3.5 to run.

# Usage
1. In all markdown files in your project that you want to generate tables of contents for, insert the following tags into the file, where you want the table of contents to be placed:
```
<!--ts-->
<!--te-->
```

When the script is run, all text in between those two tags will be replaced with the table of contents.  Furthermore, the tags themselves will (obviously) not appear in the markdown view on GitHub, as they are html comments.

2. Run the included python script, passing as a command-line argument the directory of your project.  The script will automatically locate any markdown files (with .md extensions) within that folder and all subfolders.  It will scan them for the above tags.  If found, it will generate the table of contents for them, and replace any text inside the tags with the new table of contents.  Any file in which the tags can't be located will not be modified.
