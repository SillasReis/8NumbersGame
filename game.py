import tkinter as tk
from tkinter import *

class Game(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.numbers = dict()
        self.empty = None

        self.initUI()
        self.initNumbers()
    
    def initUI(self):
        self.master.title('Jogo dos 8 números')
        self.grid()

    def initNumbers(self):
        pixel = PhotoImage(width=1, height=1)

        for i in range(8):
            number = i+1
            self.numbers[number] = Button(self, image=pixel, name=str(number), text=str(number), bg='lightgreen', width=200, height=200, compound='c')
        
        self.numbers[1].grid(row=0, column=0)
        self.numbers[2].grid(row=0, column=1)
        self.numbers[3].grid(row=0, column=2)
        self.numbers[4].grid(row=1, column=2)
        self.numbers[5].grid(row=2, column=2)
        self.numbers[6].grid(row=2, column=1)
        self.numbers[7].grid(row=2, column=0)
        self.numbers[8].grid(row=1, column=0)

        self.empty = Button(self, image=pixel, name='empty', text='', bg='green', width=200, height=200, compound='c')
        self.empty.grid(row=1, column=1)


root = Tk()
game = Game()
root.resizable(False, False)
root.mainloop()
