# TextTk: Python/Tkinter texteditor out of boredom

## Disclaimer
This was made out of boredom. It is not serious in any way as actual software.
This library/repository is meant as an example of how one could make an application
using tkinter (Tk for Python) and freeze is as a standalone application.
If you unironically mean to use this as an actual texteditor, seek help...

## What does it have?
  - Python code containing the application and functionality.
  	Can be opened via the interpreter.

  	```sh
  	from texttk import gui

  	gui()
  	```

  - .spec files. This is what pyinstaller uses to freeze the application.

  	```sh
  	# cmd
  	pyinstaller xxx.spec
  	```

  - .iss file. A file used by Inno Script Setup to create an installer of 
  	an application

## What is it meant for?
Just to poke around in and learn about creating gui's in python and freezing it.

## Some documentation
  - https://docs.python.org/3/library/tkinter.html
  - https://pyinstaller.org/en/stable/
  - https://jrsoftware.org/isinfo.php