import copy
from random import randint


class GameOverException(Exception):
    pass


class Game():
    def __init__(self):
        # Formato = Número : (Linha, Coluna)
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
        self.current_state, self.empty = self.__randomPositions()
        
        self.plays = 0

    
    # Move a peça selecionada. Caso seja uma peça válida, retorna True. Para peças inválidas retorna False.
    # Quando o jogo é concluído, levanta a exceção GameOverException.
    def move(self, number):
        number_position = self.current_state[number]
        empty_position = self.empty

        row_compare = number_position[0] == empty_position[0]
        column_compare = number_position[1] == empty_position[1]

        #Verificar se são vizinhos diretos
        valid_positions = False

        if row_compare ^ column_compare:
            if row_compare:
                if abs(number_position[1] - empty_position[1]) == 1:
                    valid_positions = True

            elif column_compare:
                if abs(number_position[0] - empty_position[0]) == 1:
                    valid_positions = True

        #Trocar espaço vazio com número selecionado
        if valid_positions:
            self.__switchPosition(number)
            self.plays += 1
            
            # Verifica se o jogo acabou
            self.win_condition()

            return True

        return False


    def __switchPosition(self, number):
        self.current_state[number], self.empty = self.empty, self.current_state[number]


    # Levanta a GameOverException caso o jogo tenha alcançado a condição de vitória, caso contrário, só sai do método
    def win_condition(self):
        for i in range(1, 9):

            if self.current_state[i] != self.finish_state[i]:
                return
        
        raise GameOverException()

    
    # Retorna uma tupla:
        # Posição 0: Dicionário com posições(tuplas) únicas e aleatórias para cada chave. Dicionário é sempre diferente de self.finish_state
        # Posição 1: Tupla para o espaço vazio
    def __randomPositions(self):
        while True:
            numbers_positions = dict()
            empty_position = tuple()
            positions = list()
            
            # Gerar tuplas únicas e aleatórias
            while len(positions) < 9:
                rand_pos = randint(0,2), randint(0,2)
                
                if rand_pos not in positions:
                    positions.append(rand_pos)
            
            # Associar cada tupla a uma chave no dicionário
            for i in range(1,9):
                numbers_positions[i] = positions[i-1]

            # Espaço vazio recebe a última tupla
            empty_position = positions[8]

            # Verificar se dados gerados não são iguais ao self.finish_state
            if numbers_positions != self.finish_state:
                return numbers_positions, empty_position
