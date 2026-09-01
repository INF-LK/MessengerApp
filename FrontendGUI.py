from tkinter import Tk
import tkinter as tk


class FrontendGUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        # Additional GUI setup can be done here
    
    def contactList(self, contacts: list):
        for i in self.winfo_children():
            i.destroy()
        for g in contacts:
            button = tk.Button(self, text=g, command=lambda g=g:self.openChat(g))
            button.pack()
        
    
    def openChat(self, contact):
        for i in self.winfo_children():
            i.destroy()
        topBar = tk.Frame(self, height=50, bg="lightgray")
        topBar.pack(fill=tk.X, side=tk.TOP)
        contact = tk.Label(topBar, text=f"Chat with {contact}")
        contact.pack(side=tk.TOP)
        button = tk.Button(topBar, text="Back", command=lambda: self.contactList(self.getContacts()))
        button.pack(side=tk.TOP, anchor="w")
        entry = tk.Entry()
        entry.bind("<Return>", lambda event: self.sendMessage(entry.get()))
        entry.pack(side=tk.BOTTOM, fill=tk.X)

    def backToContacts(self):
        pass
    
    def getContacts(self):
        # Placeholder for getting contacts from the backend
        return ["Alice", "Bob", "Charlie"]
        
    def sendMessage(self, message):
        print(f"Sending message: {message}")
   
    def run(self):
        self.mainloop()
        
    
chat = FrontendGUI()

chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()
        
        
    
        

