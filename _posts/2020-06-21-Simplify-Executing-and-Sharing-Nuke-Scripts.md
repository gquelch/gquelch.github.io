---
title: Simplify Executing and Sharing Nuke Scripts
layout: post
published: true
---

If we have written lots of one off scripts for Nuke, it can be annoying to paste them into the script editor over and over, there are a couple of ways around this, one being my [GQ_Tools panel](https://github.com/gquelch/Nuke-Public-Scripts#gq_tools), which allows you to import and run external scripts easily.

Underneath the hood, the panel is importing and reloading scripts as *[modules](https://www.w3schools.com/python/python_modules.asp)*. You can create a similar setup in just a few lines of code, it's comprised of:

- The script path
- The script name
- An if statement to add the path
- An if statement to import or reload the script

Here is an example:

```python
import sys

#the directory in which your scripts are saved
path = "F:\Resources\tools\nuke\scripts"

def runScript(scriptName):

    #if statement to see if directory is already included in the sys path
    if path in sys.path:
        pass
    else:
        sys.path.append(path)
        
    #if module isn't imported, import it
    #if it is imported, reload it
    if scriptName not in sys.modules:
        i = __import__(scriptName, fromlist=[''])
    else:
        reload(sys.modules[scriptName])
        

#run this function on the named script, dont include the .py extension!  
runScript("Script Name Here")
```

You can take the code above, add your own script path, and run the function with the name of any python scripts in that folder and they should execute!

Now, usually importing a module won't execute anything in that script, you would expect to execute a class or function from that module like this:

```python
import exampleScript
exampleScript.doNukeAction()
```

Here our script is called *exampleScript*, and inside that we have defined the function *doNukeAction*, which will perform the task

Relying on executing specific functions makes it impossible to dynamically import scripts and execute them, as there is no guarantee function names are the same across multiple scripts!

However, if we call that function at the end of the *exampleScript* script itself:

```python
def doNukeAction():
    print "executing nuke script"

doNukeAction() #this extra line executes the function
```

This script will execute when we import or reload it! Which means if all of our scripts are set up this way, we are able to import them from just their name, and not worry about specific function names within them

## Menu.py + Panels

You can take this a step further with a menu.py, I won't go into the many benefits of having one, there are plenty of great guides already, such as [Ben McEwan's](https://benmcewan.com/blog/2018/01/14/whats-a-menu-py-and-why-should-i-have-one/) and [Josh Parks'](https://www.compositingpro.com/improve-your-nuke-compositing-workflow-with-menu-py/). 

I will show you how I use the method above in my menu.py to import my Python Panels

```python
sys.path.append("F:\Resources\tools\nuke\scripts")
import nukePanel
```

We don't need any if statements here, as this is only being run when Nuke is launched.

As above, these scripts contain an execute function, in this case it adds them to the Nuke Panel menu, meaning I can call them whenever I need from the UI.

Working this way can make your scripting and script sharing workflow much simpler, not only is it easier to import and run different scripts, but you only need to share a few lines of code with your teammates, rather than emailing hundreds of lines of code around, which is easily lost and difficult to organize. You can also edit the script outside of Nuke, in the editor of your choice.

It also means you are able to update the script and others will have access to it straight away, so long as the file name doesn't change, the script for importing and reloading will continue to work.