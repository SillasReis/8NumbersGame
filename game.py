import copy


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
        self.current_state = copy.deepcopy(self.finish_state)
        self.empty = (1,1)
        
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

