from game import *
from copy import deepcopy
import sys

# Aumenta o limite de recursão. Necessário para rodar o Solver.solve()
sys.setrecursionlimit(1000000)


# Nó para expansão na busca
class Node():
    def __init__(self, game):
        self.game = deepcopy(game)
    
    # Nós são iguais se o current_state dos seus games forem iguais
    def __eq__(self, other):
        return self.game.current_state == other.game.current_state

    def __ne__(self, other):
        return self.game.current_state != other.game.current_state
    
    # Um nó é maior ou menor que outro dependendo de seus pesos
    def __lt__(self, other):
        return self.getWeight() < other.getWeight()
    
    def __le__(self, other):
        return self.getWeight() <= other.getWeight()
    
    def __gt__(self, other):
        return self.getWeight() > other.getWeight()
    
    def __ge__(self, other):
        return self.getWeight() >= other.getWeight()

    def __repr__(self):
        return f'{self.game.current_state}\n{self.getWeight()}'


    # Heurística para definir peso/custo de um nó
    # weight = h1 + h2
    def getWeight(self):
        # h2 é a soma da menor distância de cada elemento até sua posição final
        h2 = 0
        for number in self.game.current_state:
            h2 += self.__origin_dist(number)

        # h1 representa a quantidade de elementos fora de suas posições finais 
        h1 = self.__outOfPosition()

        return h1 + h2


    # Retorna a menor distância de um elemento até sua posição final
    def __origin_dist(self, number):
        row_diff = abs(self.game.current_state[number][0] - self.game.finish_state[number][0])
        col_diff = abs(self.game.current_state[number][1] - self.game.finish_state[number][1])

        return row_diff + col_diff


    # Retorna a quantidade de elementos fora de posição
    def __outOfPosition(self):
        out_of_pos = 0
        
        for i in self.game.current_state:
            if self.game.current_state[i] != self.game.finish_state[i]:
                out_of_pos += 1
        
        return out_of_pos

# Algoritmo de busca em espaço de estados
# Recebe um jogo e o resolve a partir de seu estado atual
class Solver():
    def __init__(self, game):
        # Depois de resolvido o problema, as etapas de resolução ficarão em self.steps
        self.__steps = list()
        self.__visited_nodes = list()
        self.__solve(Node(game))

    # Solucionar jogo
    def __solve(self, node):
        # Caso o peso seja 0, o problema já foi resolvido
        # Nesse caso adiciona recursivamente os nodes da solução em self.steps
        if node.getWeight() == 0:
            self.__steps.append(node)
            return 1
        else:
            # Nodes na fronteira do node atual
            to_look = list()
            
            # Define movimentos possíveis a partir do node atual
            # Caso uma das jogadas possíveis levante a exceção GameOverException, começa a adicionar recursivamente os nodes da solução em self.steps
            for i in range(1,9):
                new_node = Node(node.game)
                try:
                    valid_move = new_node.game.move(i)
                except GameOverException:
                    self.__steps.append(new_node)
                    return 1

                # Confere se o possível node já não foi visitado para evitar ciclos infinitos
                if valid_move is True and new_node not in self.__visited_nodes:
                    # Adiciona o node em to_look e em self.__visited_nodes
                    to_look.append(new_node)
                    self.__visited_nodes.append(new_node)


            # Percorre os nodes recursivamente do menor para o maior procurando a solução
            to_look.sort()
            for i in to_look:
                # Se self.__solve(i) retornar 1, significa que o node atual faz parte do caminho até a solução
                ans = self.__solve(i)
                if ans == 1:
                    self.__steps.append(node)
                    return 1
            return 0
    
    # Retorna próximo passo para a solução
    # Se levantar a exceção GameOverException, os passos chegaram ao fim
    def getNextStep(self):
        try:
            return self.__steps.pop().game
        except IndexError:
            raise GameOverException()
    
    # Retorna a quantidade de passos restantes para a solução
    def stepsLeft(self):
        return len(self.__steps)
