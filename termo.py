#!/usr/bin/env python3

from rich.console import Console

console = Console()

style = {
    "G": "green underline",
    "Y": "yellow",
    "B": "",
}


def ler_todas_palavras():
    """
    Lê todas as palavras do arquivo e retorna uma lista com elas.
    Remove palavras com letras maiusculas ou com acentos ou com ç.
    """
    with open("palav.txt", "r") as f:
        palavras = f.readlines()

    palavras = [p.strip() for p in palavras]
    palavras = [p for p in palavras if p.islower()]
    palavras = [p for p in palavras if not any(c in p for c in "çáéíóúãõâêîôû")]
    palavras = [p for p in palavras if len(set(p)) == len(p)]

    # print(len(palavras))
    return palavras


class Termo:
    todas_palavras = ler_todas_palavras()

    def __init__(self, verbose=False):
        self.pontuacao = 0
        self.tentativas = 0
        self.letras_erradas = set()
        self.palavra_secreta = self._palavra_secreta()
        self.verbose = verbose
        self._print(f"Segredo: {self.palavra_secreta}", style="yellow")

    def _print(self, *args, **kwargs):
        """
        Imprime na tela.
        """
        if self.verbose:
            console.print(*args, **kwargs)

    def _reset(self):
        self.pontuacao += max(7 - self.tentativas, 0)
        self._print("Pontuação:", self.pontuacao, style="yellow")
        self.tentativas = 0
        self.letras_erradas = set()
        self.palavra_secreta = self._palavra_secreta()

    def _palavra_secreta(self):
        from random import choice

        return choice(Termo.todas_palavras)

    def chute(self, tentativa):
        """
        Retorna uma lista com os seguintes valores:
        G - letra correta e na posição correta
        Y - letra correta e na posição errada
        B - letra errada

        Caso a palavra não tenha 5 letras ou não esteja na
        lista de palavras, retorna uma lista vazia.
        """
        if len(tentativa) != 5:
            self._print("A palavra deve ter 5 letras", style="red")
            return []

        if tentativa not in Termo.todas_palavras:
            self._print("Palavra não encontrada", style="red")
            return []

        self.tentativas += 1
        ret = []
        for i in range(len(tentativa)):
            if tentativa[i] == self.palavra_secreta[i]:
                ret.append("G")
            elif tentativa[i] in self.palavra_secreta:
                ret.append("Y")
            else:
                ret.append("B")

        if self.tentativas >= 7:
            self._print(
                "Você perdeu! A palavra era:", self.palavra_secreta, style="red"
            )
            self._reset()
            return []

        if ret == ["G", "G", "G", "G", "G"]:
            self._print(
                f"Você ganhou {max(7 - self.tentativas, 0)} pontos!", style="green"
            )
            self._reset()
            return ret

        self._print_feedback(tentativa, ret)

        return ret

    def _print_feedback(self, tentativa, ret):
        """
        Imprime o feedback do chute.
        """
        self._print("--", end=" ")
        for i in range(len(tentativa)):
            self._print(tentativa[i], end="", style=style[ret[i]])
            if ret[i] == "B":
                self.letras_erradas.add(tentativa[i])
        print(" --", *self.letras_erradas)

    def iterativo(self):
        """
        Método iterativo para jogar o jogo.
        """
        while True:
            self._print(">> ", end="")
            tentativa = input().strip()
            ret = self.chute(tentativa)

            if ret == ["G", "G", "G", "G", "G"]:
                return self.tentativas


if __name__ != "__main__":
    # import sys
    # from io import StringIO
    ...
    # sys.stdout = StringIO()
else:
    termo = Termo(verbose=True)
    termo.iterativo()
