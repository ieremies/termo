#!/usr/bin/env python3

import time
from random import choice

from termo import Termo, ler_todas_palavras

palavras = ler_todas_palavras()

"""
Método chute(palavra) da classe Termo.
Retorna uma lista com os seguintes valores:
G - letra correta e na posição correta
Y - letra correta e na posição errada
B - letra errada

Caso a palavra não tenha 5 letras ou não esteja na
lista de palavras, retorna uma lista vazia.

Após 7 tentativas, ele perde e reinicia o jogo.
Após ganhar, ele reinicia o jogo.
"""


def estrategia(jogo: Termo):
    tentativas = 0
    while True:
        tentativas += 1
        ret = jogo.chute(choice(palavras))
        time.sleep(0.1)

        if tentativas >= 7 or ret == ["G", "G", "G", "G", "G"]:
            return


def game():
    jogo = Termo(verbose=True)
    while True:
        estrategia(jogo)


if __name__ == "__main__":
    game()
