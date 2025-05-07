#!/usr/bin/env python3
from random import choice

from rich.console import Console

console = Console()

style = {
    "G": "green underline",
    "Y": "yellow",
    "B": "",
}


def palavra_secreta():
    # lê o arquivo palav.txt
    # e retorna uma palavra secreta aleatória
    with open("palav.txt", "r") as f:
        palavras = f.readlines()

    return choice(palavras).strip()


def confere(palavra, tentativa):
    ret = []

    for i in range(len(tentativa)):
        if tentativa[i] == palavra[i]:
            ret.append("G")
        elif tentativa[i] in palavra:
            ret.append("Y")
        else:
            ret.append("B")

    return ret


def main():
    palavra = palavra_secreta()
    # print(f"A palavra secreta é: {palavra}")

    tentativas = 0
    letras_erradas = set()
    while True:
        tentativa = input(">> ").strip()

        if len(tentativa) != 5:
            print("A palavra deve ter 5 letras")
            continue

        tentativas += 1

        ret = confere(palavra, tentativa)

        console.print("--", end=" ")
        for i in range(len(tentativa)):
            console.print(tentativa[i], end="", style=style[ret[i]])
            if ret[i] == "B":
                letras_erradas.add(tentativa[i])
        print(" --", *letras_erradas)

        if ret == ["G", "G", "G", "G", "G"]:
            print(f"Você acertou em {tentativas} tentativas!")
            break


if __name__ == "__main__":
    main()
