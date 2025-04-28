"""
Program: To-Do List
Author: Morgan Hutton
Last Updated: April 27, 2025 (version 0.1)
Purpose: Allows the user to record to-do list items, mark as completed, or remove from the list.
"""

# IMPORT
import tkinter as tk # used for the GUI


### TASK LIST MAIN WINDOW
# BUILD WINDOW
taskList = tk.Tk()# creates the window
taskList.title("To-Do List") # titles the window
taskList.config(bg="#1A558C") # colors the window background

# BUILD WINDOW HEADER
titleFrame = tk.Frame(taskList) # establishes the header
titleFrame.config(bg="#00A2E8") # colors the header
headerTitle = tk.Label( # adds text to the header
    titleFrame,
    text = "To-Do List",
    font = ("Arial Rounded MT Bold", 30),
    fg = "#FFFFFF",
    bg="#00A2E8")
headerTitle.pack(expand = True, fill = "both", anchor = "center", padx = 30, pady = 15) # positions the text within the header
titleFrame.pack(fill = "x", side = "top") # positions the header within the window

# BUILD LIST FRAME
listFrame = tk.Frame(taskList, bg = "#1A558C") # establishes the frame
listFrame.pack(fill = "both", expand = True)
listFrame.columnconfigure(1, weight = 0) # column1 weight
listFrame.columnconfigure(2, weight = 1) # column2 weight - takes most space
listFrame.columnconfigure(3, weight = 0) # column3 weight
checkItem = tk.Label( # adds column1 header
    listFrame,
    text = "Done",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
checkItem.grid (row = 1, column = 1, sticky = "w") # places column1 header
listItem = tk.Label( # adds column2 header 
    listFrame,
    text = "Task",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
listItem.grid(row = 1, column = 2) # places column2 header
deleteItem = tk.Label( # adds column3 header
    listFrame,
    text = "Delete",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
deleteItem.grid(row = 1, column = 3, sticky = "e") # places column3 header

# BUILD BUTTON FRAME
buttonFrame = tk.Frame( # establishes the frame
    taskList,
    bg = "#1A558C",
    borderwidth = 0,
    relief = "solid",
    highlightthickness = 3, 
    highlightbackground = "#1A558C",
    highlightcolor = "#1A558C")
buttonFrame.pack(fill = "x", side = "bottom")

# IMPLEMENT BUTTON INTERACTION
newItem = tk.Button(
    buttonFrame,
    text = "Add To List",
    bg = "#00A2E8",
    fg = "#FFFFFF",
    activeforeground = "#00A2E8",
    font = ("Arial Rounded MT Bold", 14))
newItem.pack(fill = "x")


### END OF PROGRAM
taskList.mainloop() # ends window generation