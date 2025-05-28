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
    copia = palavras.copy()
    tentativas = 0
    while True:
        tentativas += 1
        p = choice(copia)
        ret = jogo.chute(p)
        for i, c in enumerate(p):
            if not ret:
                break
            if ret[i] == "B":
                copia = [p for p in copia if c not in p]
            if ret[i] == "Y":
                copia = [p for p in copia if c in p]
            if ret[i] == "G":
                copia = [p for p in copia if p[i] == c]

        # time.sleep(0.1)

        if tentativas >= 7 or ret == ["G", "G", "G", "G", "G"]:
            return


def game():
    jogo = Termo(verbose=False)
    while True:
        estrategia(jogo)
        print(jogo.pontuacao)


# Código principal para medição de performance
import statistics  # Para calcular média e desvio padrão
import time
from typing import Dict, List

from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def simular_estrategia_com_tempo_limite(tempo_limite_segundos: int = 60) -> List[int]:
    pontuacoes: List[int] = []
    tempo_inicio = time.monotonic()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("Jogos: {task.fields[jogos]:>5d}"),
        "•",
        TextColumn("Pontuação: {task.fields[pontuacao]:>5d}"),
        "•",
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            description="[cyan]Simulando jogos...",
            total=tempo_limite_segundos,
            pontuacao=0,
            jogos=0,
        )
        jogo = Termo(verbose=False)
        ultima_pontuacao = 0
        ultimo_tempo = 0
        qtd_jogos = 0
        while time.monotonic() - tempo_inicio < tempo_limite_segundos:
            estrategia(jogo)
            pontuacoes.append(jogo.pontuacao - ultima_pontuacao)
            ultima_pontuacao = jogo.pontuacao
            qtd_jogos += 1

            if time.monotonic() - ultimo_tempo >= 0.25:
                # Atualiza o progresso a cada segundo
                ultimo_tempo = time.monotonic()
                progress.update(
                    task, advance=0.15, pontuacao=jogo.pontuacao, jogos=qtd_jogos
                )

    # --- Estatísticas ---
    print(f"Total de jogos simulados: {len(pontuacoes)}")
    print(f"Pontuação média: {statistics.mean(pontuacoes):.2f}")
    if len(pontuacoes) > 1:
        print(f"Desvio padrão da pontuação: {statistics.stdev(pontuacoes):.2f}")
    print(f"Pontuação mínima: {min(pontuacoes)}")
    print(f"Pontuação máxima: {max(pontuacoes)}")

    # Distribuição de pontuações (para Termo, isso é interessante)
    distribuicao: Dict[int, int] = {}
    for p in pontuacoes:
        distribuicao[p] = distribuicao.get(p, 0) + 1
    print("\nDistribuição das pontuações:")
    for score, count in sorted(distribuicao.items()):
        percentage = (count / len(pontuacoes)) * 100
        print(f"  Pontuação {score}: {count} vezes ({percentage:.2f}%)")

    return pontuacoes


if __name__ == "__main__":
    # game()
    simular_estrategia_com_tempo_limite(tempo_limite_segundos=60)
