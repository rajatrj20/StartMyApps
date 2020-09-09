from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from io import StringIO
import tkinter.ttk as ttk

class MyFirstGUI:
    def __init__(self, master):
        ttk.Style().theme_use('vista')
        
        self.master = master
        self.addedApps = {}
        self.launcherFileFormat = [('Batch Files', '*.bat'),  
             ('Shell Files', '*.sh')] 
        self.validInputFileFormat = [("All Files","*")]

        self.master.geometry("500x450")
        self.master.resizable(0, 0)
        self.master.title("StartMyApps")

        #Top Panel
        frame1 = Frame(master, height=100, width=300)
        frame1.grid(row=0, column=0)
        frame1.grid_propagate(0)

        image = Image.open("images/logo.png")
        image = image.resize((100,100))
        photo = ImageTk.PhotoImage(image)

        label = ttk.Label(frame1, image=photo)
        label.image = photo # keep a reference!
        label.grid(row=0, column=0, sticky="NW")

        var = StringVar()
        var.set("""Welcome to StartMyApps. One click solution to kick start your work enviornment.""")
        self.infoHeader = Message(frame1, textvariable=var, width=190)
        self.infoHeader.grid(row=0, column=1, sticky="E")
        
        #Left Sidebar
        frame2 = Frame(master, height=100, width=200)
        frame2.grid(row=0, column=1)
        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_rowconfigure(1, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_propagate(0)
        
        self.labelAddApp = ttk.Label(frame2, text="Find your apps here:")
        self.fileBoxButton = ttk.Button(frame2, text="Add", command=self.addNewApp)
        self.labelAddApp.grid(row=0, column=0, sticky='S')
        self.fileBoxButton.grid(row=1, column=0)
        
        #Right Sidebar
        frame3 = Frame(master, height=273, highlightbackground="black", highlightthickness=1)
        frame3.grid(row=1, columnspan=2, sticky='nsew')
        frame3.grid_columnconfigure(0, weight=10)
        frame3.grid_columnconfigure(1, weight=10)
        frame3.grid_columnconfigure(2, weight=1)
        frame3.grid_propagate(0)

        self.listLabel = ttk.Label(frame3, text="Select Apps:", anchor='w')
        self.listLabel.grid(row=0, column=0, sticky='W')

        self.openButton = ttk.Button(frame3, text="Edit Existing Launcher", command=self.openLauncher)
        self.openButton.grid(row=0, column=1, sticky='E')

        self.removeButton = ttk.Button(frame3, text="Remove App", command=self.removeApp)
        self.removeButton.grid(row=0, column=2, sticky='E')

        self.listBox = Listbox(frame3, selectmode='SINGLE', height=15)
        self.listBox.grid(row=1, columnspan=3, sticky='WE')

        #Bottom Panel
        frame4 = Frame(master, height=70)
        frame4.grid(row=3, columnspan=2, sticky='nsew')
        frame4.grid_rowconfigure(0, weight=1)
        frame4.grid_rowconfigure(1, weight=1)
        frame4.grid_columnconfigure(0, weight=1)
        frame4.grid_propagate(0)
        
        self.saveFileButton = ttk.Button(frame4, text="Generate Launcher", command=self.generateLauncher)
        self.saveFileButton.grid(row=0, column=0, sticky='NE')

        self.saveFileProgressVar = StringVar()
        self.saveFileProgressLabel = ttk.Label(frame4, textvariable=self.saveFileProgressVar, anchor='w')
        self.saveFileProgressLabel.grid(row=1, column=0)
        self.saveFileProgressLabel.grid_remove()

    def addNewApp(self):
        appName = filedialog.askopenfilename(filetypes = self.validInputFileFormat)
        if appName in self.addedApps:
            return
        self.listBox.insert('end', appName)
        self.addedApps.update({appName : self.listBox.size()})

    def removeApp(self):
        if(self.listBox.curselection() is None or len(self.listBox.curselection()) == 0):
            return
        currentSelectedApp = self.listBox.get(self.listBox.curselection())
        self.listBox.delete(self.listBox.curselection())
        del self.addedApps[currentSelectedApp]

    def openLauncher(self):
        launcherFile = filedialog.askopenfilename(filetypes = self.launcherFileFormat)
        if launcherFile:
        	existingApps = []
        	with open(launcherFile, "r") as file:
        		for line in file:
        			if line.startswith('start "" '):
        				existingApps.append(line.strip()
        					.replace('start "" ', '')
        					.replace('"', ''))
        	if len(existingApps):
        		for appName in existingApps:
        			self.listBox.insert('end', appName)
        			self.addedApps.update({appName : self.listBox.size()})
        	else:
        		self.saveFileProgressLabel.grid()
        		self.saveFileProgressVar.set("No apps found in launcher file, please check the file")
      
    def generateLauncher(self):
        self.saveFileProgressLabel.grid()
        self.saveFileProgressVar.set("Starting Launcher Generation...")
        if len(self.addedApps) == 0:
            self.saveFileProgressVar.set("Seems like no applications are added.")
            return
        file_str = StringIO()
        for line in self.addedApps:
            file_str.write('start "" ')
            file_str.write('"'+ line +'"\n')
        self.saveFileProgressVar.set("Please select location to save file...")
        file = filedialog.asksaveasfile(filetypes = self.launcherFileFormat, defaultextension = self.launcherFileFormat) 
        if file:
            file.write(file_str.getvalue())
            file.close()
            self.saveFileProgressVar.set("Launcher generated successfully.\nGo to "+ str(file.name))
            self.reset()
        else:
            self.saveFileProgressVar.set("You aborted operation. Please click on button again to continue.")

    def reset(self):
        self.addedApps.clear()
        self.listBox.delete(0, self.listBox.size())

if __name__ == "__main__":
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()