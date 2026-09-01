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
            print(g)
            button = tk.Button(self, text=g, command=lambda g=g:self.openChat(g))
            button.pack()
        
    
    def openChat(self, contact):
        for i in self.winfo_children():
            i.destroy()
        contact = tk.Label(text=f"Chat with {contact}")
        contact.pack()
        button = tk.Button(text="Back", command=self.contactList)
        button.pack()
        entry = tk.Entry()
        entry.bind("<Return>", lambda event: self.sendMessage(entry.get()))
        entry.pack()

    def backToContacts(self):
        pass
        
    def sendMessage(self, message):
        print(f"Sending message: {message}")
   
    def run(self):
        self.mainloop()
        
    
chat = FrontendGUI()

chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()
        
        
    
        

