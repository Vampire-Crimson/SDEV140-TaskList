"""
Program: Task List
Author: Morgan Hutton
Purpose: Allows the user to create and manage a to-do list.

Change Log:
    Version 0.1 (April 27, 2025)
        Created the basic interface design.
    Version 0.2 (April 30, 2025)
        Added basic program functionality.
            Created a variable to count the number of items in the list.
        Changed interface design to accommodate functionality.
            Removed column 3 header "delete"
            Added new column header "deadline" in column 3.
    Version 0.2.1 (April 6, 2025)
        Bugfix. The delete functionality now deletes only the expected items.
    Version 0.9 (April 7, 2025)
        Rewrote code for consistency and readability.
        Created functionality to checkboxes to count the number of completed items.
        Added new text to the header that tracks user progress.
        Added new buttons "save", "load", and "help".
            Added file management functionality.
            Added in-program tutorial.
        Added scrollbar to accommodate large lists.
"""

### HOUSEKEEPING
# IMPORT
import tkinter as tk # used for GUI
from tkinter import filedialog # used for file management - processing
import json # used for file management - writing/reading

# INITIALIZE
tasksInList = 0 # counts the items in the list
tasksCompleted = 0 # counts the tasks completed
dataReferences = {}

# DEFINE FUNCTIONS (BUTTON COMMANDS)
"""
Functions are defined in reverse order of user interaction.
Some functions involve the creation of new windows.
"""

def saveToFile():
    filePath = filedialog.asksaveasfilename( # determines the constraints of the file explorer
        defaultextension = ".json",
        filetypes = [("JSON files (*.json)", "*.json"), ("All files", "*.*")],
        title = "Save as"
    )
    
    if filePath: # will only save the file if the user chose a location and file name
        tasksToSave = {} # organizes saved data
        
        for widget in tasksFrame.winfo_children(): # records data to be saved
            rowInfo = widget.grid_info() # gathers necessary data for proper organization
            rowNumber = rowInfo["row"]
            columnNumber = rowInfo["column"]
            
            if rowNumber not in tasksToSave: # organizes data by row number
                tasksToSave[rowNumber] = {}
            
            if columnNumber == 1 and isinstance(widget, tk.Checkbutton):
                if rowNumber in dataReferences:
                    completionStatus = dataReferences[rowNumber].get()
                    tasksToSave[rowNumber]["completed"] = completionStatus
            elif columnNumber == 2 and isinstance(widget, tk.Label): # records a task's description
                tasksToSave[rowNumber]["task"] = widget.cget("text")
            elif columnNumber == 3 and isinstance(widget, tk.Label): # records a task's deadline
                tasksToSave[rowNumber]["deadline"] = widget.cget("text")
        
        try: # actually saves the file
            with open(filePath, 'w') as saveFile:
                json.dump(tasksToSave, saveFile, indent = 4)
                print(f"File saved successfully as \"{filePath}\".")
        except Exception as error:
            print(f"An unexpected error occurred: {error}")

def deleteTask(buttonWidget):
    global tasksInList # will be updated in the function
    deletingRow = buttonWidget.grid_info()["row"] # ensures the button deletes only its own row
    deletingWidgets = [] # temporarily stores the items to be deleted
    
    for widget in tasksFrame.winfo_children(): # checks to see if an item is valid for deleting
        examine = widget.grid_info()
        if examine["row"] == deletingRow: # if the item is on the same row as the delete button
            deletingWidgets.append(widget) # it is added to the list of items to be deleted
    
    for widget in deletingWidgets:
        widget.destroy() # deletes the items
    
    for widget in tasksFrame.winfo_children(): # repositions remaining items
        examine = widget.grid_info()
        if examine["row"] > deletingRow: # if the row was below the deleted one
            widget.grid_configure(row = examine["row"] - 1) # it's moved up to remove blank space
    
    tasksInList -= 1 # reduces the count of total list items
    taskCompletion.config(text = f"{tasksCompleted}/{tasksInList} Tasks Completed") # updates the tracker

def updateTaskCompletion(checkVar):
    global tasksCompleted
    
    if checkVar.get() == 1:
        tasksCompleted += 1
    else:
        tasksCompleted -= 1
    
    taskCompletion.config(text = f"{tasksCompleted}/{tasksInList} Tasks Completed")

def addNewTask(newTask, newDeadline):
    global tasksInList
    tasksInList += 1 # increases the count of total list items
    
    createCheck = tk.IntVar() # used for checkbox generation
    newListCheck = tk.Checkbutton( # generates item checkbox
        tasksFrame,
        variable = createCheck,
        command = lambda: updateTaskCompletion(createCheck),
        selectcolor = "#1A558C", # colors checkbox - dark blue
        bg = "#1A558C",
        activebackground = "#1A558C",
        fg = "#FFFFFF", # colors check mark - white
        activeforeground = "#FFFFFF"
    )
    newListCheck.grid(row = tasksInList, column = 1, padx = 5, sticky = "ew") # places checkbox in the main window list
    
    newListTask = tk.Label( # generates item task
        tasksFrame,
        text = newTask,
        font = ("Arial Rounded MT Bold", 15), # changes the font and text size
        fg = "#FFFFFF", # colors the text - white
        wraplength = 300, # enables word-wrapping on the text
        bg = "#1A558C" # prevents a gray block in the window
    )
    newListTask.grid(row = tasksInList, column = 2, padx = 5, sticky = "ew")
    
    newListDeadline = tk.Label( # generates item task
        tasksFrame,
        text = newDeadline,
        font = ("Arial Rounded MT Bold", 15), # changes the font and text size
        fg = "#FFFFFF", # colors the text - white
        bg = "#1A558C" # prevents a gray block in the window
    )
    newListDeadline.grid(row = tasksInList, column = 3, padx = 5, sticky = "ew")
    
    newListDelete = tk.Button( # generates delete button unique to the new item
        tasksFrame,
        command = lambda: deleteTask(newListDelete), 
        text = "Delete",
        font = ("Arial Rounded MT Bold", 15),
        bg = "#00A2E8",
        fg = "#FFFFFF",
        activeforeground = "#00A2E8"
    )
    newListDelete.grid(row = tasksInList, column = 4, padx = 5, sticky = "ew")
    
    dataReferences[tasksInList] = createCheck # enables checkbox status
    taskCompletion.config(text = f"{tasksCompleted}/{tasksInList} Tasks Completed") # updates the tracker

def newTaskWindow():
    newTaskCreation = tk.Toplevel(taskList) # creates a new window
    newTaskCreation.title("Add Task") # titles the window
    newTaskCreation.config(bg = "#1A558C") # colors the window - dark blue
    
    creationFrame = tk.Frame( # creates a frame for user interaction
        newTaskCreation,
        bg = "#1A558C" # colors the frame - dark blue
    )
    creationFrame.pack( # places the frame within the window
        side = "top",
        fill = "both"
    )
    
    creationLabelFrame = tk.Frame( # creates a sub-frame for labels
        creationFrame,
        bg = "#1A558C"
    )
    creationLabelFrame.pack( # places the sub-frame within its parent frame
        side = "left",
        fill = "both",
        padx = 10,
        pady = 20
    )
    
    creationEntryFrame = tk.Frame( # creates a sub-frame for text entry
        creationFrame,
        bg = "#1A558C"
    )
    creationEntryFrame.pack( # places the sub-frame within its parent frame
        side = "right",
        fill = "both",
        padx = 10,
        pady = 20
    )
    
    textNewTask = tk.Label( # creates a label for the first text entry
        creationLabelFrame,
        text = "New Task: ",
        font = ("Arial Rounded MT Bold", 15, "bold"), # changes the font and text size
        fg = "#FFFFFF", # colors the text - white
        bg = "#1A558C" # prevents a gray block in the window
    )
    textNewTask.pack( # places the label within the frame
        side = "top",
        anchor = "w",
        pady = 5
    )
    
    textNewDeadline = tk.Label( # creates a label for the second text entry
        creationLabelFrame,
        text = "Deadline: ",
        font = ("Arial Rounded MT Bold", 15, "bold"), # changes the font and text size
        fg = "#FFFFFF", # colors the text - white
        bg = "#1A558C" # prevents a gray block in the window
    )
    textNewDeadline.pack( # places the label within the frame
        side = "bottom",
        anchor = "w",
        pady = 5
    )
    
    entryNewTask = tk.Entry( # creates the first entry field 
        creationEntryFrame,
        width = 25,
        font = ("Arial Rounded MT Bold", 15), # changes the font and text size
        fg = "#00A2E8" # colors the text - light blue
    )
    entryNewTask.pack( # places the entry field within the frame
        side = "top",
        pady = 5
    )
    
    entryNewDeadline = tk.Entry( # creates the second entry field
        creationEntryFrame,
        width = 25,
        font = ("Arial Rounded MT Bold", 15), # changes the font and text size
        fg = "#00A2E8" # colors the text - light blue
    )
    entryNewDeadline.pack( # places the entry field within the frame
        side = "bottom",
        pady = 5
    )
    
    confirmationFrame = tk.Frame( # creates a frame for the button
        newTaskCreation,
        bg = "#1A558C" # colors the frame - dark blue
    )
    confirmationFrame.pack( # places the frame within the window
        side = "bottom",
        fill = "both"
    )
    
    confirmAddition = tk.Button( # creates a button to confirm item geneation
        confirmationFrame,
        command = lambda: [addNewTask(entryNewTask.get(), entryNewDeadline.get()), newTaskCreation.destroy()], 
        text = "Add New Task",
        font = ("Arial Rounded MT Bold", 15), # changes font and text size
        bg = "#00A2E8", # colors the button
        activebackground = "#FFFFFF",
        fg = "#FFFFFF", # colors the text
        activeforeground = "#00A2E8"
    )
    confirmAddition.pack(fill = "x") # places the button within the frame
    
    newTaskCreation.grab_set() # makes this window take priority over the main window
    taskList.wait_window(newTaskCreation) # fully pauses the main window while this window is open

def tutorialScreen():
    tutorialWindow = tk.Toplevel(taskList) # creates a new window
    tutorialWindow.title("Help")
    tutorialWindow.config(bg = "#1A558C") # colors the window - dark blue
    
    pageNumber = 0 # the current page. Python indices begin at 0
    totalPages = 8
    
    tutorialTexts = [ # stores text, organized by page
        "Page 1: Table of Contents\nPage 2: Add Task\nPage 3: Task Completion\nPage 4: Completion Tracker\nPage 5: Deleting Tasks\nPage 6: Saving Data\nPage 7: Loading Data\nPage 8: Help",
        "To add a new item to list, click the Add Task button. This will take you to a new window, where you can type in the description of the task and its deadline. There is no required format for either. Once done, click \"Add New Task\" to add it to the list in the main window, or cancel by clicking the x button in the top right corner.",
        "When you complete a task, you can mark it by clicking the box to the left. This will place a checkmark inside the box. You can remove the checkmark by clicking the box again.",
        "As you add and complete tasks, you may notice text in the window header changing. This text tracks your progress in the form of a fraction: the number of tasks you have marked as completed over the total number of tasks in the list. These numbers update automatically as you add, complete, and delete tasks.",
        "If you add a task by accident, or simply no longer need it, you can click the Delete button on the same row as that task. This will remove the task description, deadline, completion status, and the button itself from the list. Note that items that are deleted this way will be lost forever; it is recommended to save program data when tasks are added or completed.",
        "To save your progress, click the Save button in the main window. This will cause your computer system's file explorer to appear, allowing you to choose the location and name of the file. It is recommended to store it in a location that is easily accessed, with a file name that indicates the purpose of the list.",
        "The Load button on the main window allows you to restore program data from a previous session, so long as you have previously saved it. When you load data from a file, all existing data in the file is lost, so be careful not to lose anything by mistake! The program comes with a sample \"StarterPack\" save file, so you can test this right away if you haven't already.",
        "You can review this tutorial at any time by pressing the Help button on the main window. A more in-depth guide exists in the User Manual that came with the program."
    ]
    tutorialImagePaths = [ # stores images, organized by page
        None,
        "assets/images/HelpPage2.png",
        "assets/images/HelpPage3.png",
        "assets/images/HelpPage4.png",
        None,
        None,
        None,
        None
    ]
    tutorialAltTexts = [ # stores image description text, organized by page
        "",
        "[Image description: A screenshot of the Add Task window. There are two text entry fields and a button. The first entry field is labeled \"New Task:\" and the second entry field is labeled \"Deadline:\". The button is labeled \"Add New Task\". End of description.]",
        "[Image description: A cropped screenshot of the main window, displaying two checkboxes. The first has a checkmark, and the second does not. End of description.]",
        "[Image description: A cropped screenshot of the main window, displaying the progress tracker. It reads \"3/4 Tasks Completed\". End of description.]",
        "",
        "",
        "",
        ""
    ]
    
    textDisplay = tk.Label( # label that will hold the page text
        tutorialWindow,
        text = "",
        wraplength = 675,
        justify = tk.CENTER,
        font = ("Arial Rounded MT Bold", 15),
        fg = "#FFFFFF",
        bg = "#1A558C"
    )
    textDisplay.pack( # places the label within the window
        side = "top",
        padx = 30)
    
    imageDisplay = tk.Label( # label that will hold the page image
        tutorialWindow,
        image=None,
        bg = "#1A558C"
    )
    imageDisplay.pack(pady=5) # places the label within the window
    
    descriptionDisplay = tk.Label( # label that will hold the alt-text
        tutorialWindow,
        text = "",
        wraplength = 675,
        justify = tk.CENTER,
        font = ("Arial Rounded MT Bold", 15),
        fg = "#FFFFFF",
        bg = "#1A558C"
    )
    descriptionDisplay.pack(padx = 30) # places the label within the window
    
    pagination = tk.Frame(
        tutorialWindow,
        bg = "#00A2E8" # colors the frame - light blue
    )
    pagination.pack(side = "bottom")
    
    pageCount = tk.Label(
        pagination,
        text = f"Page {pageNumber + 1} of {totalPages}",
        font = ("Arial Rounded MT Bold", 15), # changes the font and text size
        fg = "#FFFFFF", # colors the text - white
        bg = "#00A2E8" # prevents a gray block in the window
    )
    pageCount.grid(
        row = 0,
        column = 1
    )
    
    def updatePage():
        textDisplay.config(text = tutorialTexts[pageNumber]) # updates the on-screen text
        descriptionDisplay.config(text = tutorialAltTexts[pageNumber]) # updates the on-screen alt-text
        imagePath = tutorialImagePaths[pageNumber] # determines the specific image to be used
        if imagePath: # if there is an image on the current page
            try:
                currentImage = tk.PhotoImage(file = imagePath)
                imageDisplay.config(image = currentImage)
                imageDisplay.image = currentImage
            except tk.TclError as error:
                print(f"Error loading image: {error}")
                imageDisplay.config(image = None)
        else:
            imageDisplay.config(image = None)
            imageDisplay.image = None
        pageCount.config(text = f"Page {pageNumber + 1} of {totalPages}")
    
    def flipPageBack():
        nonlocal pageNumber
        if pageNumber > 0:
            pageNumber -= 1
            updatePage()
    
    def flipPageNext():
        nonlocal pageNumber
        if pageNumber < totalPages - 1:
            pageNumber += 1
            updatePage()
    
    prevPage = tk.Button(
        pagination,
        command = flipPageBack,
        text = "Back",
        font = ("Arial Rounded MT Bold", 15), # changes font and text size
        bg = "#00A2E8", # colors the button
        activebackground = "#FFFFFF",
        fg = "#FFFFFF", # colors the text
        activeforeground = "#00A2E8"
    )
    prevPage.grid(
        row = 0,
        column = 0
    )
    
    nextPage = tk.Button(
        pagination,
        command = flipPageNext,
        text = "Next",
        font = ("Arial Rounded MT Bold", 15), # changes font and text size
        bg = "#00A2E8", # colors the button
        activebackground = "#FFFFFF",
        fg = "#FFFFFF", # colors the text
        activeforeground = "#00A2E8"
    )
    nextPage.grid (
        row = 0,
        column = 2
    )
    
    updatePage()

def loadFromFile():
    global tasksInList
    global tasksCompleted
    global dataReferences
    
    filePath = filedialog.askopenfilename( # determines the constraints of the file explorer
        defaultextension = ".json",
        filetypes = [("JSON files (.json)", "*.json"), ("All files", "*.*")],
        title = "Open"
    )
    
    if filePath: # will only proceed if the user indicated a file
        try:
            with open(filePath, 'r') as loadFile:
                openedFile = json.load(loadFile)
            
            for widget in tasksFrame.winfo_children(): # clears current program status
                widget.destroy()
            tasksInList = 0
            tasksCompleted = 0
            dataReferences.clear()
            
            for rowNumber, taskData in openedFile.items(): # loads status from file into program
                completedStatus = taskData.get("completed", 0)
                taskDescription = taskData.get("task", "")
                taskDeadline = taskData.get("deadline", "")
                
                tasksInList += 1 # counts added tasks
                
                createCheck = tk.IntVar(value = completedStatus) # loads completion status
                newListCheck = tk.Checkbutton( # creates checkbox from loaded data
                    tasksFrame,
                    variable = createCheck,
                    command = lambda var=createCheck: updateTaskCompletion(var),
                    selectcolor = "#1A558C",
                    bg = "#1A558C",
                    activebackground = "#1A558C",
                    fg = "#FFFFFF",
                    activeforeground = "#FFFFFF"
                )
                newListCheck.grid(row = int(rowNumber), column = 1, padx = 5, sticky = "ew") # places checkbox in the main window list
                dataReferences[int(rowNumber)] = createCheck # automatically checks the box (if needed)
                if completedStatus == 1:
                    tasksCompleted += 1
                newListTask = tk.Label( # generates item task
                    tasksFrame,
                    text = taskDescription,
                    font = ("Arial Rounded MT Bold", 15), # changes the font and text size
                    fg = "#FFFFFF", # colors the text - white
                    wraplength = 300, # enables word-wrapping on the text
                    bg = "#1A558C" # prevents a gray block in the window
                )
                newListTask.grid(row = int(rowNumber), column = 2, padx = 5, sticky = "ew")
                newListDeadline = tk.Label( # generates item task
                    tasksFrame,
                    text = taskDeadline,
                    font = ("Arial Rounded MT Bold", 15), # changes the font and text size
                    fg = "#FFFFFF", # colors the text - white
                    wraplength = 300, # enables word-wrapping on the text
                    bg = "#1A558C" # prevents a gray block in the window
                )
                newListDeadline.grid(row = int(rowNumber), column = 3, padx = 5, sticky = "ew")
                newListDelete = tk.Button( # generates delete button unique to the new item
                    tasksFrame,
                    command = lambda: deleteTask(newListDelete), 
                    text = "Delete",
                    font = ("Arial Rounded MT Bold", 15),
                    bg = "#00A2E8",
                    fg = "#FFFFFF",
                    activeforeground = "#00A2E8"
                )
                newListDelete.grid(row = int(rowNumber), column = 4, padx = 5, sticky = "ew")
            
            taskCompletion.config(text = f"{tasksCompleted}/{tasksInList} Tasks Completed") # updates tracker
            print(f"File \"{filePath}\" loaded successfully.") # console terminal output
        except FileNotFoundError:
            print(f"Error: File not found at \"{filePath}\".")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from \"{filePath}\". The file might be corrupted.")
        except Exception as error:
            print(f"An unexpected error occurred: {error}")

### CREATE MAIN WINDOW

taskList = tk.Tk() # creates the window
taskList.title("Task List") # titles the window
taskList.config(bg = "#1A558C") # colors the window - dark blue

### CREATE MAIN WINDOW HEADER

headerFrame = tk.Frame( # creates the frame
    taskList,
    bg = "#00A2E8" # colors the frame - light blue
)
headerFrame.pack( # places the header in the main window
    side = "top",
    fill = "x" # ensures the header stretches with the window
)

toDoList = tk.Label( # creates text "To-Do List" in the header
    headerFrame,
    text = "To-Do List",
    font = ("Arial Rounded MT Bold", 30, "bold"), # changes the font and text size
    fg = "#FFFFFF", # colors the text - white
    bg = "#00A2E8" # prevents a gray block in the window
)
toDoList.pack( # places the text within the frame
    anchor = "center",
    expand = True,
    fill = "both",
    padx = 15,
    pady = 5
)

global taskCompletion
taskCompletion = tk.Label( # creates a label to track user progress
    headerFrame,
    text = f"{tasksCompleted}/{tasksInList} Tasks Completed",
    font = ("Arial Rounded MT Bold", 15), # changes the font and text size
    fg = "#FFFFFF", # colors the text - white
    bg = "#00A2E8" # prevents a gray block in the window
)
taskCompletion.pack( # places the tracker within the frame
    side = "bottom",
    anchor = "center",
    expand = True,
    fill = "both",
    pady = 10
)

### CREATE MAIN WINDOW BUTTON FRAME

buttonFrame = tk.Frame(taskList) # creates the frame
buttonFrame.pack( # places the frame in the main window
    side = "bottom",
    fill = "x" # ensures the frame stretches with the window
)
buttonFrame.config(bg = "#00A2E8") # colors the frame - light blue

newItem = tk.Button( # creates a button to generate new items
    buttonFrame,
    command = newTaskWindow,
    text = "Add Task",
    font = ("Arial Rounded MT Bold", 15), # changes font and text size
    bg = "#00A2E8", # colors the button
    activebackground = "#FFFFFF",
    fg = "#FFFFFF", # colors the text
    activeforeground = "#00A2E8"
)
newItem.pack( # places the button within the frame
    side = "top",
    fill = "x"
)

helpButton = tk.Button( # creates a button to load data from a file
    buttonFrame,
    command = tutorialScreen,
    text = "Help",
    font = ("Arial Rounded MT Bold", 15), # changes font and text size
    bg = "#00A2E8", # colors the button
    activebackground = "#FFFFFF",
    fg = "#FFFFFF", # colors the text
    activeforeground = "#00A2E8"
)
helpButton.pack( # places the button within the frame
    side = "left",
    fill = "x",
    expand = True
)

saveData = tk.Button( # creates a button to save data to a file
    buttonFrame,
    command = saveToFile,
    text = "Save",
    font = ("Arial Rounded MT Bold", 15), # changes font and text size
    bg = "#00A2E8", # colors the button
    activebackground = "#FFFFFF",
    fg = "#FFFFFF", # colors the text
    activeforeground = "#00A2E8"
)
saveData.pack( # places the button within the frame
    side = "left",
    fill = "x",
    expand = True
)

loadData = tk.Button( # creates a button to load data from a file
    buttonFrame,
    command = loadFromFile,
    text = "Load",
    font = ("Arial Rounded MT Bold", 15), # changes font and text size
    bg = "#00A2E8", # colors the button
    activebackground = "#FFFFFF",
    fg = "#FFFFFF", # colors the text
    activeforeground = "#00A2E8"
)
loadData.pack( # places the button within the frame
    side = "left",
    fill = "x",
    expand = True
)

### CREATE LIST FRAME

listFrame = tk.Frame(taskList) # creates the frame
listFrame.pack(fill = "both", expand = True) # places the frame in the main window, ensures it stretches with the window
listFrame.config(bg = "#1A558C") # colors the frame - dark blue

columnFrame = tk.Frame(listFrame) # creates a frame for column headers
columnFrame.pack( # places the frame in the window
    side = "top",
    fill = "x"
)
columnFrame.config(bg = "#1A558C") # colors the frame - dark blue
columnFrame.columnconfigure(1, weight = 0, minsize = 30) # spaces columns
columnFrame.columnconfigure(2, weight = 1, minsize = 200)
columnFrame.columnconfigure(3, weight = 1, minsize = 150)
columnFrame.columnconfigure(4, weight = 0, minsize = 80)
columnFrame.columnconfigure(5, weight = 0, minsize = 35)

columnTask = tk.Label( # creates column2 header "Task"
    columnFrame,
    text = "Task",
    font = ("Arial Rounded MT Bold", 20, "bold"), # changes the font and text size
    fg = "#FFFFFF", # colors the text - white
    bg = "#1A558C" # prevents a gray block in the window
)
columnTask.grid( # places the text within the frame
    row = 0,
    column = 2,
    padx = 5
)

columnDeadline = tk.Label( # creates column3 header "Deadline"
    columnFrame,
    text = "Deadline",
    font = ("Arial Rounded MT Bold", 20, "bold"), # changes the font and text size
    fg = "#FFFFFF", # colors the text - white
    bg = "#1A558C" # prevents a gray block in the window
)
columnDeadline.grid( # places the text within the frame
    row = 0,
    column = 3,
    padx = 5
)

tasksCanvas = tk.Canvas(taskList) # creates a canvas for the list
tasksCanvas.pack( # places canvas in the window
    side = "left",
    fill = "both",
    expand = True
)
tasksCanvas.config(bg = "#1A558C", highlightthickness = 0) # colors the canvas - dark blue

scrollbar = tk.Scrollbar( # adds a scrollbar to the task list
    taskList,
    orient = "vertical",
    command=tasksCanvas.yview
)
scrollbar.pack( # places the scrollbar in the window
    side="right",
    fill="y")
tasksCanvas.configure(yscrollcommand=scrollbar.set) # connects the scrollbar to the canvas
tasksCanvas.bind('<Configure>', lambda e: tasksCanvas.configure(scrollregion = tasksCanvas.bbox("all"))) # enables scrolling functionality

tasksFrame = tk.Frame(tasksCanvas) # creates a frame for added items
tasksFrame.pack(fill = "both", expand = True) # places the frame in the window
tasksFrame.config(bg="#1A558C") # colors the frame - dark blue
tasksFrame.columnconfigure(1, weight = 0, minsize = 30) # spaces columns
tasksFrame.columnconfigure(2, weight = 1, minsize = 200)
tasksFrame.columnconfigure(3, weight = 1, minsize = 150)
tasksFrame.columnconfigure(4, weight = 0, minsize = 80)

### ENABLE SCROLLING

tasksCanvas.create_window((0, 0), window=tasksFrame, anchor="nw")

def updateScrollRegion(event):
    tasksCanvas.configure(scrollregion=tasksFrame.bbox("all"))

tasksFrame.bind("<Configure>", updateScrollRegion)

def resizeTasksFrame(event):
    tasksCanvas.itemconfig(tasksCanvas.find_all()[0], width=event.width)

tasksCanvas.bind("<Configure>", resizeTasksFrame)

### END OF PROGRAM
taskList.mainloop() # prevents the program from closing prematurely