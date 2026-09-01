from tkinter import Tk
import tkinter as tk


class FrontendGUI(Tk):

    def __init__(self):
        super().__init__()
        self.title("Infcord")
        self.geometry("1020x1019")
        button1 = tk.Button(self, text="Button 1", command=lambda: print("Button 1 clicked"))
        button1.pack()
        self.mainloop()
        # Additional GUI setup can be done here
    


        
    
chat = FrontendGUI()



        
        
    
        

