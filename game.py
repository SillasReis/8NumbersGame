import tkinter as tk
from tkinter import *

class Game(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.numbers = dict()
        self.finish_state = {
            1:(0,0),
            2:(0,1),
            3:(0,2),
            4:(1,2),
            5:(2,2),
            6:(2,1),
            7:(2,0),
            8:(1,0)
        }
        self.empty = None
        self.plays = 0

        self.initUI()
        self.initNumbers()
    

    def initUI(self):
        self.master.title('Jogo dos 8 números')
        self.grid()


    def initNumbers(self):
        self.pixel = PhotoImage(width=1, height=1)

        for i in range(8):
            number = i+1
            self.numbers[number] = Button(self, image=self.pixel, name=str(number), text=str(number), bg='lightgreen', width=200, height=200, compound=LEFT)
            bt = self.numbers[number]
            bt.configure(command = lambda bt=bt : self.numbersClick(bt))

        self.numbers[1].grid(row=0, column=0)
        self.numbers[2].grid(row=0, column=1)
        self.numbers[3].grid(row=0, column=2)
        self.numbers[4].grid(row=1, column=2)
        self.numbers[5].grid(row=2, column=2)
        self.numbers[6].grid(row=2, column=1)
        self.numbers[7].grid(row=2, column=0)
        self.numbers[8].grid(row=1, column=0)

        self.empty = Frame(self, name='empty', bg='green', width=200, height=200, border=0)
        self.empty.grid(row=1, column=1)


    def numbersClick(self, number_button):
        number_position = number_button.grid_info()
        empty_position = self.empty.grid_info()

        row_compare = number_position['row'] == empty_position['row']
        column_compare = number_position['column'] == empty_position['column']

        #Verificar se são vizinhos diretos
        valid_positions = False

        if row_compare ^ column_compare:
            if row_compare:
                if abs(number_position['column'] - empty_position['column']) == 1:
                    valid_positions = True

            elif column_compare:
                if abs(number_position['row'] - empty_position['row']) == 1:
                    valid_positions = True

        #Trocar espaço vazio com número selecionado
        if valid_positions:
            number_button.grid_forget()
            self.empty.grid_forget()

            number_button.grid(row=empty_position['row'], column=empty_position['column'])
            self.empty.grid(row=number_position['row'], column=number_position['column'])

            self.plays += 1

        # Verifica se o jogo acabou
        if self.win_condition():
            print(f'Parabéns! Jogo finalizado com {self.plays} jogada(s).')


    # Retorna True se o jogo tiver alcançado a condição de vitória
    def win_condition(self):
        for i in range(1, 9):
            grid_info = self.numbers[i].grid_info()
            current_pos = grid_info['row'], grid_info['column']
            
            if current_pos != self.finish_state[i]:
                return False
        
        return True



root = Tk()
game = Game()
root.resizable(False, False)
root.mainloop()
