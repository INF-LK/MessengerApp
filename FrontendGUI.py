from tkinter import Tk
import tkinter as tk


class FrontendGUI(Tk):

    def __init__(self):
        #standard init shenanigans
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        self.resizable(False, False)
        self.configure(bg="#44576D")

        
        
    
    def contactList(self, contacts: list):
        """
        Displays a list of contacts as buttons. Clicking a button opens the chat with that contact.
        """
        for i in self.winfo_children():
            i.destroy()
        for g in contacts:
            button = tk.Button(self, text=g, bg="#AAC7D8",fg="black", activebackground="#768A96", borderwidth = -2,relief = "flat", command=lambda g=g:self.openChat(g))
            button.pack(pady=10)
        
    
    def openChat(self, contact):
        """
        Opens the chat window for the selected contact. 
        """
        self.update()
        geometry = self.winfo_geometry().split("+")[0]
        print(geometry)
        for i in self.winfo_children():
            i.destroy()
        # top bar for buttons and contact name
        topBar = tk.Frame(self, height=50, bg="#29353C")
        topBar.pack(fill=tk.X)

        topBarLeft = tk.Frame(topBar, height=50, bg="#29353C")
        topBarLeft.grid(row=0, column=0, sticky="ew")

        topBarCenter = tk.Frame(topBar, height=50, bg="#29353C")
        topBarCenter.grid(row=0, column=1, sticky="ew")
        
        topBarRight = tk.Frame(topBar, height=50, bg="#29353C")
        topBarRight.grid(row=0, column=2, sticky="ew")

        #i don't fully understand column weights but ai suggested i add this and it helps?
        topBar.grid_columnconfigure(0, weight=1)
        topBar.grid_columnconfigure(1, weight=2)
        topBar.grid_columnconfigure(2, weight=1)

        #buttons and contact name
        contactButton = tk.Button(topBarLeft, text="Back", bg="#DFEBF6",fg="black", activebackground = "#AAC7D8", bd = 0, relief = "flat", command=lambda: self.contactList(self.getContacts()))
        contactButton.pack(side=tk.LEFT, padx=10, pady=10)
        
        menuButton = tk.Button(topBarRight, text="Menu", bg="#DFEBF6",fg="black", activebackground = "#AAC7D8", bd = 0, relief = "flat", command=lambda: print("Menu button clicked"))
        menuButton.pack(side=tk.RIGHT, padx=10, pady=10)
        
        contactLabel = tk.Label(topBarCenter, text=f"Chat with {contact}", bg="#DFEBF6",fg="black")
        contactLabel.pack(fill=tk.X, anchor="center")
        
        #chat Bubbles 
        #this is gonna be one hell of a ride o7
        
        #
    
        # text field for sending chat messages
        bottomBar = tk.Frame(self, height=100, bg="#29353C")
        bottomBar.pack(fill=tk.X, side=tk.BOTTOM)
        entry = tk.Entry(bottomBar, width=100, bg="#DFEBF6",fg="black", borderwidth = -2,relief = "flat")
        entry.bind("<Return>", lambda event: self.sendMessage([contact, entry.get()]))
        entry.pack(anchor="center", pady=10)
        
        
    def chatBubble(self, message: list):
    #entirely ai so far, test later
        """
        Creates a chat bubble for the given message.
        message: [unread:bool, sender: str (self/foreign), message: str]
        """
        unread, sender, msg = message
        bubble = tk.Frame(self, bg="#DFEBF6", bd=2, relief="solid")
        bubble.pack(pady=5, padx=10, anchor="w" if sender == "foreign" else "e")
        label = tk.Label(bubble, text=msg, bg="#DFEBF6",fg="black", wraplength=400)
        label.pack(padx=10, pady=5)
        
    def backToContacts(self):
        pass
    
    def getContacts(self):
        #placeholder for getting contacts from backend
        return ["Alice", "Bob", "Charlie"]
        
    def getChatLog(self, contact):
        #placeholder for getting messages from backend
        #format: [[unread:bool, sender: str (self/foreign), message: str], ...]
        return [[0, "mine", "Hello!"], [0, "foreign", "Hi there!"], [0, "mine", "How are you?"], [1, "foreign", "I'm good, thanks!"]]
    
    def sendMessage(self, message):
        #placeholder for sending message to backend
        msg = " ".join(message)
        
        print(f"Sending message: {msg}")
   
    def run(self):
        self.mainloop()
        
    
chat = FrontendGUI()

chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()





