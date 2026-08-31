from tkinter import Tk

class FrontendGUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        self.mainloop()
        # Additional GUI setup can be done here
    
    def contactList(self, contacts: list):
        for i in self.winfo_children():
            i.destroy()
        for i in contacts:
            self.button(text=i, command=lambda i=i: self.openChat(i)).pack()

    def openChat(self, contact):
        for i in self.winfo_children():
            i.destroy()
        self.label(text=f"Chat with {contact}").pack()
        self.button(text="Back", command=self.backToContacts).pack()
        self.update()
        
    def run(self):
        self.mainloop()
        
    
chat = FrontendGUI()

chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()
        
        
    
        

