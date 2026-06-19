#!/usr/bin/env python3
"""
Dever 4 - Subset Sum.

Dado um conjunto S e um alvo T, o script verifica se existe um subconjunto de S
cuja soma seja exatamente T. A versao abaixo usa busca com backtracking para
mostrar claramente a natureza exponencial do problema.
"""

from time import perf_counter
from typing import List, Optional, Tuple


def subset_sum(s: List[int], alvo: int) -> Tuple[bool, List[int], int]:
    """
    Procura um subconjunto com soma igual ao alvo.

    Retorna:
    - existe: True/False
    - subconjunto encontrado
    - chamadas recursivas executadas
    """
    chamadas = 0
    n = len(s)

    # Sufixo com soma dos positivos restantes ajuda a podar casos positivos.
    positivos_restantes = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        positivos_restantes[i] = positivos_restantes[i + 1] + max(0, s[i])

    def buscar(indice: int, soma_atual: int, escolhidos: List[int]) -> Optional[List[int]]:
        nonlocal chamadas
        chamadas += 1

        if soma_atual == alvo and escolhidos:
            return escolhidos.copy()

        if indice == n:
            return None

        # Poda segura quando todos os numeros restantes sao nao negativos.
        if all(valor >= 0 for valor in s[indice:]) and soma_atual > alvo:
            return None
        if all(valor >= 0 for valor in s[indice:]) and soma_atual + positivos_restantes[indice] < alvo:
            return None

        escolhidos.append(s[indice])
        incluindo = buscar(indice + 1, soma_atual + s[indice], escolhidos)
        if incluindo is not None:
            return incluindo
        escolhidos.pop()

        return buscar(indice + 1, soma_atual, escolhidos)

    resposta = buscar(0, 0, [])
    return resposta is not None, resposta or [], chamadas


def casos_de_teste() -> List[Tuple[str, List[int], int]]:
    """Monta os tres cenarios do enunciado."""
    pequeno = [2, 4, 6, 10]
    medio = [-5, -2, 1, 3, 7, 12, 15, 21]

    # Caso grande deterministico com 30 inteiros de cinco digitos.
    # Os cinco primeiros somam exatamente 500000.
    grande = [
        12345,
        87654,
        43210,
        23456,
        333335,
        54321,
        67890,
        11111,
        22222,
        34567,
        45678,
        56789,
        67891,
        78912,
        89123,
        91234,
        13579,
        24680,
        97531,
        86420,
        75310,
        64200,
        53100,
        42000,
        31999,
        20888,
        19777,
        18666,
        17555,
        16444,
    ]

    return [
        ("Pequeno", pequeno, 16),
        ("Medio", medio, 0),
        ("Grande", grande, 500000),
    ]


def explicar_complexidade() -> None:
    """Imprime classe do problema e complexidade."""
    print("\nAnalise de complexidade")
    print("-" * 26)
    print("Subset Sum em versao de decisao pertence a NP e e NP-completo.")
    print("A busca exata por inclusao/exclusao testa, no pior caso, 2^n subconjuntos.")
    print("Complexidade de tempo no pior caso: O(2^n).")
    print("Complexidade de memoria: O(n), por causa da profundidade da recursao.")
    print("As podas podem acelerar alguns casos, mas nao mudam o pior caso exponencial.")


def demonstracao() -> None:
    """Executa todos os cenarios do enunciado com tempo de execucao."""
    print("=== Dever 4 - Subset Sum ===")

    for nome, conjunto, alvo in casos_de_teste():
        inicio = perf_counter()
        existe, subconjunto, chamadas = subset_sum(conjunto, alvo)
        fim = perf_counter()

        print(f"\nCenario {nome}")
        print(f"n = {len(conjunto)} | alvo T = {alvo}")
        print("Existe subconjunto?", "sim" if existe else "nao")
        if existe:
            print(f"Subconjunto encontrado: {subconjunto}")
            print(f"Soma: {sum(subconjunto)}")
        print(f"Chamadas recursivas: {chamadas}")
        print(f"Tempo de execucao: {(fim - inicio) * 1000:.6f} ms")

    explicar_complexidade()


if __name__ == "__main__":
    demonstracao()
