#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import webapp2
from azure import *
from random import randint

linha = 0
coluna = 0

tentativas = 0

barco_linha = 0
barco_coluna = 0

board = []


def init_jogo():
    global linha, coluna, tentativas
    global barco_linha, barco_coluna
    global board

    linha = 0
    coluna = 0

    board = []

    tentativas = 0

    # Inicializacao do tabuleiro de jogo
    # Em vez de executar estas duas linhas
    # podemos criar uma função e chama-la,
    # nesse caso comenta-se as duas linahas
    # seguintes e descomenta-se a linha init_board()
    for x in range(1, 6):
        board.append([""] * 5)

    # Posicao inicial do barco no tabuleriro
    # Em vez de executar estas duas linhas
    # podemos criar uma função e chama-la,
    # nesse caso comenta-se as duas linahas
    # seguintes e descomenta-se a linha posicao_barco()
    barco_linha = randint(1, 5)
    barco_coluna = randint(1, 5)

    # As duas linhas seguintes sao apenas para diagnostico
    # logging.debug("Barco Linha: %s", str(barco_linha))
    # logging.debug("Barco Coluna %s", str(barco_coluna))

    # init_board()
    # posicao_barco()


def init_board():
    # Esta funcao so e chamada se a inicializacao do jogo
    # nao limpar o tabuleiro
    global board
    for x in range(1, 6):
        board.append([""] * 5)


def posicao_barco():
    # Esta funcao so e chamada se a inicializacao do jogo
    # nao obtiver a nova posicao do barco
    global barco_linha, barco_coluna
    barco_linha = randint(1, 5)
    barco_coluna = randint(1, 5)

    # As duas linhas seguintes sao apenas para diagnostico
    # logging.debug("Barco Linha: %s", str(barco_linha))
    # logging.debug("Barco Coluna %s", str(barco_coluna))


class MainPage(webapp2.RequestHandler):
    def get(self):
        # Se a variavel tentativas se encontra a zero entao
        # inicializamos o jogo (tabuleiro, posicao do barco
        # e restantes variaveis)
        if tentativas == 0:
            init_jogo()

        # Ou executamos estas duas linhas seguintes, na primeira
        # constroi-se a string que pretendemos escrever
        # e depois excutamos o comando para escrever ...
        html_board = """
            <html><head><title>AAS Battleship</title>
            </head><body><div class="container"><h2> AAS Battleship </h2>
            <h3> Trabalho Laboratorial 2 </h3>
            <form action="/sign" method="post">
            <div>Linha: <input type="text" name="linha">&nbsp;&nbsp;&nbsp;Coluna:
            <input type="text" name="coluna">&nbsp;&nbsp;
            <input type="submit" value="Jogar">
            </div><br/>"""

        self.response.out.write(html_board)

        # ... ou entao executamos a escrita linha a linha
        # self.response.out.write('<html><head>')
        # self.response.out.write('<title>AAS Battleship</title>')
        # self.response.out.write('</head><body>')
        # self.response.out.write('<h1> AAS Battleship </h1>')
        # self.response.out.write('<h2> Trabalho Laboratorial 2 </h2>')
        # self.response.out.write('<form action="/sign" method="post">')
        # self.response.out.write('<div>Linha:&nbsp;<input type="text" name="linha">')
        # self.response.out.write('&nbsp;&nbsp;&nbsp;Coluna:&nbsp;')
        # self.response.out.write('<input type="text" name="coluna">&nbsp;&nbsp;')
        # self.response.out.write('<input type="submit" value="Jogar"></div><br/>')

        # Apresentar o tabuleiro de jogo no formato de tabela de 5 x 5
        # com possibilidade de exibir coluna de topo e lateral esquerda
        # com a respectiva numeracao das casas
        self.response.out.write('<div><table border="1" style="border-collapse: collapse;">')
        for i in range(len(board)):
            # Com numeracao no topo do tabuleiro. Comentar
            # o bloco total de if i == 0 caso nao se queira
            # esta numeracao
            # Este bloco so e executado uma vez, logo no
            # inicio da primeira linha da matriz
            if i == 0:
                for j in range(len(board[i]) + 1):
                    if j > 0:
                        self.response.out.write('<th height="30px" align="center">')
                        self.response.out.write(str(j))
                        self.response.out.write('</th>')
                    else:
                        self.response.out.write('<th height="30px" align="center">')
                        self.response.out.write('\\')
                        self.response.out.write('</th>')
            self.response.out.write('<tr>')
            # Com numeracao do lado esquerdo. Comentar
            # as 3 linhas seguintes caso nao se queira
            # esta numeracao
            self.response.out.write('<th width="30px" align="center">')
            self.response.out.write(str(i + 1))
            self.response.out.write('</th>')
            for j in range(len(board[i])):
                self.response.out.write('<td width="50px" height="50px" align="center">')
                # A linha seguinte e apenas para diagnostico
                # logging.debug("Value for row is %s", str(board[i][j]))
                self.response.out.write(str(board[i][j]))
                self.response.out.write('</td>')
            self.response.out.write('</tr>')
        self.response.out.write('</table></div>')

        # E agora por fim terminamos a construcao da pagina
        self.response.out.write('</form></div></body></html>')


class Jogar(webapp2.RequestHandler):
    def post(self):
        global linha, coluna, tentativas
        global board
        valido = False
        afundou = False

        # Apanha os valores introduzidos pelo
        # jogador, validar se estao entre os valores
        # considerados validos para tabela e se estiverem
        # actualizar a matriz do tabuleiro com o valor
        # introduzido e processar se atingiu o barco ou
        # se foi agua
        linha = self.request.get('linha')
        coluna = self.request.get('coluna')

        # As 4 linhas seguintes sao apenas para diagnostico
        logging.debug("Linha: %s", str(linha))
        logging.debug("Coluna %s", str(coluna))
        logging.debug("Barco Linha: %s", str(barco_linha))
        logging.debug("Barco Coluna %s", str(barco_coluna))

        # Teste para ver se o jogador introduziu um
        # numero de linha e/ou de coluna valido
        # e se nao se trata de uma repeticao de
        # jogada anterior
        if linha != "" and 0 < int(linha) < 6:
            if coluna != "" and 0 < int(coluna) < 6:
                if board[int(linha)-1][int(coluna)-1] != "X" or board[int(linha)-1][int(coluna)-1] != "0":
                    valido = True

        if valido is True:
            tentativas = int(tentativas) + 1
            # A linha seguinte e apenas para diagnostico
            logging.debug("Tentativas: %s", str(tentativas))

            # Tiro certeiro? Ou h2o?
            if int(linha) == int(barco_linha) and int(coluna) == int(barco_coluna):
                afundou = True

            # Agora finalmente actualizamos a matriz com
            # o resultado da jogada
            # Na realidade a matriz (list) vai de 0 a 4
            # portanto temos que subtrair 1 as coordenadas
            if afundou is False:
                board[int(linha)-1][int(coluna)-1] = "0"
            else:
                board[int(linha)-1][int(coluna)-1] = "X"

        self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Jogar)
], debug=True)
