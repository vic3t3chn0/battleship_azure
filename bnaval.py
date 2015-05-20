from  random import randint

linha=0
coluna=0

tentativas = 0

barco_linha=0
barco_coluna=0

board = []

def init_jogo():
    global linha, coluna, tentativas
    global barco_linha, barco_coluna
    global board
    
    linha=0
    coluna=0
    
    tentativas = 0

    init_board()
    posicao_barco()

# Esta funcao so e chamada se a inicializacao do jogo
# nao limpar o tabuleiro
def init_board():
    global board
    for x in range(1, 6):
        board.append(["?"]*5)

# Esta funcao so e chamada se a inicializacao do jogo
# nao obter a nova posicao do barco
def posicao_barco():
    global barco_linha, barco_coluna
    barco_linha = randint(1, 5)
    barco_coluna  = randint(1, 5)

class main():
#    init_jogo()

    posicao_barco()

#   Para diagnostico apenas
    print barco_linha, barco_coluna

    init_board()

#   Para diagnostico apenas
    for i in range(len(board)):
        for j in range(len(board[i])):
            print board[i][j]

#   Para diagnostico apenas
    for row in board:
        print row
