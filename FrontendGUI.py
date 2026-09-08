from tkinter import Tk
import tkinter as tk
import FrontendToBackend
import threading

class FrontendGUI(Tk):

    def __init__(self):
        #standard init shenanigans
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        self.resizable(False, False)
        self.colorscheme = "trans"
        self.setColorscheme(self.colorscheme)
        self.configure(bg=self.windowColor)
        self.username = "Alice"
        #test feature, put into login function later:
        self.initializeBackend(self.username)
        self.chatLogs = None  # Initialize chatLogs to None
        self.currentContact = None 
        self.updateLoop()  # Start the update loop for receiving messages


    def setColorscheme(self, scheme):
        self.colorscheme = scheme
        """
        other color schemes except for frosted are not intended for actual use
        """
        schemes = ["darkmode","#000000","#000000","#000000","#000000","#000000","#000000",
           "lightmode","#ffffff","#ffffff","#ffffff","#ffffff","#ffffff","#ffffff",
           "frosted","#29353c","#44576d","#768a96","#aac7d8","#dfebf6","#e6e6e6",
           "trans","#1fa6de","#df859a","#cbb3f7","#55cdfc","#f5a9b8","#ffffff",
           "pride", "#e50000", "#ff8c00", "#ffef00", "#00811f", "#0044ff", "#760089"
           ]
        if scheme not in schemes:
            raise ValueError(f"Unknown colorscheme: {scheme}")
        idx = schemes.index(scheme)
        self.windowColor = schemes[idx+1]
        self.buttonHoverColor = schemes[idx+2]
        self.buttonColor = schemes[idx+3]
        self.entryColor = schemes[idx+3]
        self.labelColor = schemes[idx+3]
        self.topBarColor = schemes[idx+4]
        self.bubbleColor = schemes[idx+5]
        self.spareColor = schemes[idx+6]
    
    
    
    def initializeBackend(self, username):
        """
        Initializes the backend connection with the given username.
        """
        self.backend = FrontendToBackend.MessengerClient(username)
        self.backend.connect()    
        
    def contactList(self, contacts: list):
        """
        Displays a list of contacts as buttons. Clicking a button opens the chat with that contact.
        """
        for i in self.winfo_children():
            i.destroy()
        for g in contacts:
            button = tk.Button(self, text=g, bg=self.buttonColor,fg="black", activebackground=self.buttonHoverColor, borderwidth = -2,relief = "flat", command=lambda g=g:self.openChat(g))
            button.pack(pady=10)
        
        self.currentContact = None  # Reset current contact when showing contact list
    
    def openChat(self, contact):
        """
        Opens the chat window for the selected contact. 
        """
        self.update()
        geometry = self.winfo_geometry().split("+")[0]
        for i in self.winfo_children():
            i.destroy()
        
        #this is important to know what messages to fetch from the backend  
        self.currentContact = contact
            
        # top bar for buttons and contact name
        topBar = tk.Frame(self, height=50, bg=self.topBarColor)
        #topBar.pack(fill=tk.X)
        topBar.grid(row=0, column=0, sticky="ew")

        topBarLeft = tk.Frame(topBar, height=50, bg=self.topBarColor)
        topBarLeft.grid(row=0, column=0, sticky="ew")

        topBarCenter = tk.Frame(topBar, height=50, bg=self.topBarColor)
        topBarCenter.grid(row=0, column=1, sticky="ew")
        
        topBarRight = tk.Frame(topBar, height=50, bg=self.topBarColor)
        topBarRight.grid(row=0, column=2, sticky="ew")

        #i don't fully understand column weights but ai suggested i add this and it helps?
        topBar.grid_columnconfigure(0, weight=1)
        topBar.grid_columnconfigure(1, weight=2)
        topBar.grid_columnconfigure(2, weight=1)

        #buttons and contact name
        contactButton = tk.Button(topBarLeft, text="Back", bg=self.buttonColor,fg="black", activebackground = self.buttonHoverColor, bd = 0, relief = "flat", command=lambda: self.contactList(self.getContacts()))
        contactButton.pack(side=tk.LEFT, padx=10, pady=10)
        
        menuButton = tk.Button(topBarRight, text="Menu", bg=self.buttonColor,fg="black", activebackground = self.buttonHoverColor, bd = 0, relief = "flat", command=lambda: self.openMenu())
        menuButton.pack(side=tk.RIGHT, padx=10, pady=10)
        
        contactLabel = tk.Label(topBarCenter, text=f"Chat with {contact}", bg=self.labelColor,fg="black")
        contactLabel.pack(fill=tk.X, anchor="center")
        
        #chat Bubbles 
        #this is gonna be one hell of a ride o7
        
        #first a frame for the chat bubbles, i'll have to find out how to make it scrollable later
        bubbleFrame = tk.Frame(self, bg=self.windowColor)
        bubbleFrame.grid(row=1, column=0, sticky="nsew")
        
        #this makes sure the bubbleFrame fills up the window without pushing the top and bottom bars out of the way.. i think?
        #i just played around with weights until it worked 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        #
        self.buildChatBubbles(bubbleFrame, self.getChatLog(contact))

        # text field for sending chat messages
        bottomBar = tk.Frame(self, height=100, bg=self.topBarColor)
        bottomBar.grid(row=2, column=0, sticky="ew")
        entry = tk.Entry(bottomBar, width=100, bg=self.entryColor,fg="black", borderwidth = -2,relief = "flat")
        entry.bind("<Return>", lambda event: self.sendMessage([contact, entry.get()]))
        entry.pack(anchor="center", pady=10)
        
        
    def chatBubble(self, bubbleFrame, message: list):
    #entirely ai so far, test later
    #works after a few changes
        """
        Creates a chat bubble for the given message.
        message: [unread:bool, sender: str (mine/foreign), message: str]
        """
        unread, sender, msg = message
        bubble = tk.Frame(bubbleFrame, bg=self.bubbleColor, bd=2)#, relief="solid")
        bubble.pack(pady=5, padx=10, anchor="w" if sender == "foreign" else "e")
        label = tk.Label(bubble, text=msg, bg=self.bubbleColor,fg="black", wraplength=400)
        label.pack(padx=10, pady=5)
    
    
    def buildChatBubbles(self, bubbleFrame, messages: list):
        """
        Builds chat bubbles for a list of messages.
        messages: [[unread:bool, sender: str (mine/foreign), message: str], ...]
        """
        for i in messages:
            self.chatBubble(bubbleFrame, i) 
        
        
    def getContacts(self):
        #placeholder for getting contacts from backend
        return ["Alice", "Bob", "Charlie"]
        
        
    def getChatLog(self, contact):
        #placeholder for getting messages from backend
        #format: [[unread:bool, sender: str (mine/foreign), message: str], ...]
        if self.chatLogs == None:
            self.chatLogs = {
                "Alice": [[0, "mine", "Hello!"], [0, "foreign", "Hi there!"], [0, "mine", "How are you?"], [1, "foreign", "I'm good, thanks!"]],
                "Bob": [[0, "mine", "Hey Bob!"], [1, "foreign", "Hey!"], [0, "mine", "What's up?"], [0, "foreign", "Not much, you?"]],
                "Charlie": [[0, "mine", "Hey Charlie!"], [0, "foreign", "Hey!"], [0, "mine", "How's it going?"], [1, "foreign", "Good, you?"]]
            }
        return self.chatLogs.get(contact)
    
    
    def updateChatLog(self, contact):
        newChatLog = self.getChatLog(contact)
        
        for i in self.backend.messageList[:] : 
             
            if i[0] == contact and i[1] == True:
                newChatLog.append(i[1:])
                self.backend.messageList.remove(i)
                
        self.chatLogs[contact] = newChatLog
        return newChatLog
                        

    
    def updateLoop(self):
        """
        Continuously updates the chat log with new messages from the backend.
        """
        #try:
        while self.currentContact != None and len(self.backend.messageList) > 0:
            # Update the chat log for the relevant contact
            self.updateChatLog(self.currentContact)
            # Refresh the chat bubbles
            self.openChat(self.currentContact)
            #self.update_idletasks()
        #except Exception as e:
            #print(f"Error in updateLoop: {e}")
        self.after(2500, self.updateLoop)  # Check for new messages every second
                
    
    
    def openMenu(self):
        #placeholder for opening menu
        #self.updateLoop()
        print("Menu opened")
    
    
    def sendMessage(self, message):
        #placeholder for sending message to backend
        self.backend.send_message(message[0], message[1])
        self.chatLogs[message[0]].append([0, "mine", message[1]])  # Append sent message to the chat log
        msg = " ".join(message)
        
        #print(f"Sending message: {msg}")
   
   
    def run(self):
        
        self.mainloop()
        
    
chat = FrontendGUI()
chat.contactList(["Alice", "Bob", "Charlie"])
chat.run()





