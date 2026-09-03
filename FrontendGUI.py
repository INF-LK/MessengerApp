from tkinter import Tk
import tkinter as tk


class FrontendGUI(Tk):

    def __init__(self):
        #standard init shenanigans
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        
    
    def contactList(self, contacts: list):
        """
        Displays a list of contacts as buttons. Clicking a button opens the chat with that contact.
        """
        for i in self.winfo_children():
            i.destroy()
        for g in contacts:
            button = tk.Button(self, text=g, command=lambda g=g:self.openChat(g))
            button.pack()
        
    
    def openChat(self, contact):
        """
        Opens the chat window for the selected contact. 
        """
        for i in self.winfo_children():
            i.destroy()
        #top bar for buttons and contact name
        topBar = tk.Frame(self, height=50, bg="lightgray")
        topBar.pack(fill=tk.X, side=tk.TOP)
        contact = tk.Label(topBar, text=f"Chat with {contact}")
        contact.pack(side=tk.TOP, anchor="center")
        button = tk.Button(topBar, text="Back", command=lambda: self.contactList(self.getContacts()))
        button.pack(side=tk.LEFT, anchor="nw")
        #button.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        #I can't get this FUCKASS BUTTON TO BE ON THE SAME HEIGHT AS THE NAME LABEL., I HATE TKINTER!Q!! I HATE IT SO MUCH!!!!!!! AAAGGHDGZHSASKD
        #text field for chat messages
        bottomBar = tk.Frame(self, height=100, bg="lightgray")
        bottomBar.pack(fill=tk.X, side=tk.BOTTOM)
        entry = tk.Entry(bottomBar, width=100)
        entry.bind("<Return>", lambda event: self.sendMessage(entry.get()))
        entry.pack(side=tk.BOTTOM)

    def backToContacts(self):
        pass
    
    def getContacts(self):
        #placeholder for getting contacts from backend
        return ["Alice", "Bob", "Charlie"]
        
    def sendMessage(self, message):
        #placeholder for sending message to backend
        print(f"Sending message: {message}")
   
    def run(self):
        self.mainloop()
        
    
chat = FrontendGUI()

chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()
        
        
    
        

