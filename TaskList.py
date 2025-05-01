"""
Program: To-Do List
Author: Morgan Hutton
Last Updated: April 30, 2025 (version 0.2)
Purpose: Allows the user to record to-do list items, mark as completed, or remove from the list.
Change Log:
    version 0.1:
        crafted basic interface
    version 0.2:
        changed existing column3 ("delete") to column4
        added new column "deadline" as column3 in to-do list
        created a new variable that counts the number of items in the total list
        created button functionality for adding and removing items from the list
        removed column4 header ("delete")
"""

# IMPORT
import tkinter as tk # used for the GUI

# INITIALIZE NEEDED VARIABLES
tasksInList = 0 # used for placement of generated items

### TASK LIST MAIN WINDOW
# BUILD WINDOW
taskList = tk.Tk() # creates the window
taskList.title("To-Do List") # titles the window
taskList.config(bg = "#1A558C") # colors the window background

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
listFrame.columnconfigure(3, weight = 1) # column3 weight - same as column2
listFrame.columnconfigure(4, weight = 0) # column3 weight
checkItem = tk.Label( # adds column1 header
    listFrame,
    text = "Done",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
checkItem.grid (row = 0, column = 1, padx = 5, sticky = "w") # places column1 header
listItem = tk.Label( # adds column2 header 
    listFrame,
    text = "Task",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
listItem.grid(row = 0, column = 2, padx = 5) # places column2 header
deadlineItem = tk.Label( # adds column3 header
    listFrame,
    text = "Deadline",
    font = ("Arial Rounded MT Bold", 14),
    fg = "#FFFFFF",
    bg = "#1A558C")
deadlineItem.grid(row = 0, column = 3, padx = 5) # places column3 header

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

# BUTTON FUNCTION DEFINITIONS
def deleteTask(rowNumber):
    global tasksInList # will be updated in the function
    
    for widget in listFrame.winfo_children(): #examines each item in the list (checkboxes, text, buttons)
        examine = widget.grid_info()
        if examine["row"] == rowNumber: # if the item is on the same row as the Delete button...
            widget.destroy() # ... that item is destroyed
    
    for widget in listFrame.winfo_children(): # now we need to move the remaining items in the list
        examine = widget.grid_info()
        if examine["row"] > rowNumber: # if there is a gap in the row numbers...
            widget.grid_configure(row = examine["row"] - 1) # the next row is moved down to remove the gap
    
    tasksInList -= 1 # reduces the count of rows in the list

def taskAddition(newTask, newDeadline, closeWindow):
    global tasksInList
    tasksInList += 1 # adds 1 to the count of items in the list
    
    createCheck = tk.IntVar() # used for checkbox generation
    newListCheck = tk.Checkbutton( # generates check box in column1
        listFrame,
        variable = createCheck,
        selectcolor = "#1A558C",
        bg = "#1A558C",
        activebackground = "#1A558C",
        fg = "#FFFFFF",
        activeforeground = "#FFFFFF"
    )
    newListCheck.grid(row = tasksInList, column = 1, padx = 5)
    
    newListItem = tk.Label( # generates task list item column2
        listFrame,
        text = newTask,
        font = ("Arial Rounded MT Bold", 14),
        fg = "#FFFFFF",
        bg = "#1A558C"
    )
    newListItem.grid(row = tasksInList, column = 2, padx = 5)
    
    newListDeadline = tk.Label( # generates task list item column3
        listFrame,
        text = newDeadline,
        font = ("Arial Rounded MT Bold", 14),
        fg = "#FFFFFF",
        bg = "#1A558C"
    )
    newListDeadline.grid(row = tasksInList, column = 3, padx = 5)
    
    newListDelete = tk.Button(
        listFrame,
        text = "Delete",
        font = ("Arial Rounded MT Bold", 14),
        bg = "#00A2E8",
        fg = "#FFFFFF",
        activeforeground = "#00A2E8",
        command = lambda rowNumber = tasksInList: deleteTask(rowNumber)
    )
    newListDelete.grid(row = tasksInList, column = 4, padx = 5, sticky = "e")

def addNewTask():    
    newListItem = tk.Toplevel(taskList) # creates a new window
    newListItem.title("Add Item to List") # titles the window
    newListItem.config(bg = "#00A2E8") # colors the window background
    
    itemCreationFrame = tk.Frame(newListItem) # prevents future frame placement error
    itemCreationFrame.config(bg = "#00A2E8") # colors the frame
    itemCreationFrame.pack(fill = "both", side = "top") # places the frame in the window
    
    newItemLabelFrame = tk.Frame(itemCreationFrame) # frame for on-screen text
    newItemLabelFrame.config(bg = "#00A2E8") # colors the frame
    newItemLabelFrame.pack(fill = "both", side = "left", padx = 10, pady = 20) # places the frame in the window
    typeNewTask = tk.Label( # labels the task entry box
        newItemLabelFrame,
        text = "New Task: ",
        font = ("Arial Rounded MT Bold", 14),
        fg = "#FFFFFF",
        bg = "#00A2E8"
    )
    typeNewTask.pack(side = "top", anchor = "w", pady = 5) # places the label
    typeNewDeadline = tk.Label( # labels the deadline entry box
        newItemLabelFrame,
        text = "Deadline: ",
        font = ("Arial Rounded MT Bold", 14),
        fg = "#FFFFFF",
        bg = "#00A2E8"
    )
    typeNewDeadline.pack(side = "bottom", anchor = "w", pady = 5) # places the label
    
    newItemEntryFrame = tk.Frame(itemCreationFrame) # frame for text entry
    newItemEntryFrame.config(bg = "#00A2E8") # colors the frame
    newItemEntryFrame.pack(fill = "both", side = "right", padx = 10, pady = 20) # places the frame in the window
    enterNewTask = tk.Entry( # text entry for task list
        newItemEntryFrame,
        width = 25,
        font = ("Arial Rounded MT Bold", 14),
        fg = "#1A558C"
    )
    enterNewTask.pack(side = "top", pady = 5) # places the text entry widget
    enterNewDeadline = tk.Entry( # text entry for deadline
        newItemEntryFrame,
        width = 25,
        font = ("Arial Rounded MT Bold", 14),
        fg = "#1A558C"
    )
    enterNewDeadline.pack(side = "bottom", pady = 5)
    
    newItemButtonFrame = tk.Frame(newListItem) # frame for confirmation
    newItemButtonFrame.config(bg = "#00A2E8") # colors the frame
    newItemButtonFrame.pack(fill = "both", side = "bottom") # places the frame in the window
    confirmNewItem = tk.Button( # button for confirmation
        newItemButtonFrame,
        text = "Confirm New Task",
        bg = "#1A558C",
        fg = "#FFFFFF",
        activeforeground = "#00A2E8",
        font = ("Arial Rounded MT Bold", 14),
        command = lambda: [taskAddition(enterNewTask.get(), enterNewDeadline.get(), newListItem), newListItem.destroy()]
    )
    confirmNewItem.pack(fill = "x")
    
    newListItem.grab_set() # makes the taskList window inoperable while this window is open
    taskList.wait_window(newListItem) # fully pauses interaction with taskList

# IMPLEMENT BUTTON INTERACTION
newItem = tk.Button(
    buttonFrame,
    text = "Add To List",
    bg = "#00A2E8",
    fg = "#FFFFFF",
    activeforeground = "#00A2E8",
    font = ("Arial Rounded MT Bold", 14),
    command = addNewTask)
newItem.pack(fill = "x")


### END OF PROGRAM
taskList.mainloop() # ends window generation