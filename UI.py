import tkinter as tk
from tkinter import *
import sys

from game import *


class FinishGameWindow(Toplevel):
    def __init__(self, plays, transient):
        super().__init__()

        self.plays = plays

        # Forçando foco na janela de fim de jogo
        self.transient = transient
        self.focus_force()
        self.grab_set()

        self.resizable(False, False)

        self.initFinishWindow()
    

    # Inicializar janela
    def initFinishWindow(self):
        self.title('Fim')
        self.geometry('300x100')

        Label(self, text=f'Parabéns!\nJogo finalizado com {self.plays} jogada(s).').pack(side=TOP, fill=BOTH, expand=True)
        Button(self, text='Jogar novamente', command=self.playAgainButton).pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=5)
        Button(self, text='Sair', command=self.exitButton).pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=5)
    

    def exitButton(self):
        sys.exit(0)


    # Reiniciar o jogo
    def playAgainButton(self):
        self.transient.game = Game()
        self.transient.updateScreen()
        self.destroy()
        

class GameFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.game = Game()
        self.pixel = PhotoImage(width=1, height=1)

        self.initUI()
    
    #Inicializar interface
    def initUI(self):
        self.master.title('Jogo dos 8 números')
        self.grid()

        self.updateScreen()


    # Atualizar conteúdo com base nas posições em self.game.current_state
    def updateScreen(self):
        # Apagar widget atuais
        for widget in self.winfo_children():
            widget.destroy()
        
        # Criar novos widgets
        for number in self.game.current_state:
            self.createNumberButton(number, self.game.current_state[number])
        
        self.createEmptyFrame(self.game.empty)

    
    #Criar botão móvel com número
    def createNumberButton(self, number, position):
        command = lambda id=number : self.numbersClick(id)
        button = Button(self, image=self.pixel, name=str(number), text=str(number), bg='lightgreen', width=200, height=200, compound=LEFT, command=command)
        button.grid(row=position[0], column=position[1])

    
    # Criar espaço vazio
    def createEmptyFrame(self, position):
        frame = Frame(self, name='empty', bg='green', width=200, height=200, border=0)
        frame.grid(row=position[0], column=position[1])


    # Ação de clique nos números
    def numbersClick(self, number):
        # Caso o método move em self.game levante a exceção GameOverException, exibe a tela de fim de jogo[
        # Caso retorne False, a peça selecionada não pode se movimentar
        # Caso retorne True, a peça foi movida, mas o jogo não acabou
        try :
            move = self.game.move(number)
            if not move:
                return
        
        except GameOverException:
            # Apresenta tela de fim de jogo
            FinishGameWindow(self.game.plays, self)
        
        self.updateScreen()



root = Tk()
game = GameFrame()
root.resizable(False, False)
root.mainloop()