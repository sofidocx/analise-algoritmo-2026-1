#!/usr/bin/env python3
"""
Dever 3 - KNN para classificar perfil de investimento.

Problema:
- Classificar o cliente Arthur usando k = 3 e distancia Euclidiana.
- Caracteristicas: salario anual em milhares de reais e pontuacao de credito.
"""

from math import sqrt
from time import perf_counter
from typing import Dict, List, Tuple


Cliente = Tuple[str, float, float, str]


BASE_TREINO: List[Cliente] = [
    ("Ana", 40, 20, "Conservador"),
    ("Bruno", 50, 35, "Conservador"),
    ("Carlos", 90, 80, "Agressivo"),
    ("Diana", 80, 65, "Agressivo"),
]

ARTHUR = ("Arthur", 60, 45)
K = 3


def distancia_euclidiana(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calcula a distancia Euclidiana entre dois pontos 2D."""
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def classificar_knn(base: List[Cliente], salario: float, credito: float, k: int) -> Tuple[str, List[Tuple[str, float, str]]]:
    """
    Classifica um novo cliente pelo algoritmo KNN.

    Passos:
    1. Calcula a distancia do novo cliente para todos os clientes de treino.
    2. Ordena pela menor distancia.
    3. Pega os k vizinhos mais proximos.
    4. Decide pela classe mais frequente entre esses vizinhos.
    """
    distancias = []

    for nome, salario_treino, credito_treino, perfil in base:
        distancia = distancia_euclidiana(salario, credito, salario_treino, credito_treino)
        distancias.append((nome, distancia, perfil))

    distancias.sort(key=lambda item: item[1])
    vizinhos = distancias[:k]

    votos: Dict[str, int] = {}
    soma_distancias: Dict[str, float] = {}
    for _, distancia, perfil in vizinhos:
        votos[perfil] = votos.get(perfil, 0) + 1
        soma_distancias[perfil] = soma_distancias.get(perfil, 0.0) + distancia

    # Desempate: maior numero de votos; depois menor soma de distancias.
    perfil_final = min(votos, key=lambda perfil: (-votos[perfil], soma_distancias[perfil]))
    return perfil_final, vizinhos


def explicar_complexidade(n: int, d: int, k: int) -> None:
    """Imprime a analise de complexidade do KNN usado no script."""
    print("\nAnalise de complexidade")
    print("-" * 26)
    print(f"n = {n} clientes de treino, d = {d} caracteristicas, k = {k}.")
    print("Calcular todas as distancias custa O(n * d).")
    print("Ordenar as distancias custa O(n log n).")
    print("Votar entre os k vizinhos custa O(k).")
    print("Complexidade total desta implementacao: O(n * d + n log n + k).")
    print("Como d=2 e k=3 sao constantes neste dever, domina O(n log n).")


def demonstracao() -> None:
    """Executa o exemplo do enunciado e mostra o tempo de execucao."""
    print("=== Dever 3 - KNN: Banco de Dados de Clientes ===")
    print(f"Novo cliente: {ARTHUR[0]} | salario anual: {ARTHUR[1]} | credito: {ARTHUR[2]}")
    print(f"k escolhido: {K}")

    inicio = perf_counter()
    perfil, vizinhos = classificar_knn(BASE_TREINO, ARTHUR[1], ARTHUR[2], K)
    fim = perf_counter()

    print("\nDistancias ate Arthur, ordenadas:")
    for nome, distancia, perfil_vizinho in vizinhos:
        print(f"{nome:<7} distancia = {distancia:>7.3f} | perfil = {perfil_vizinho}")

    print(f"\nClassificacao final de Arthur: {perfil}")
    print(f"Tempo de execucao: {(fim - inicio) * 1000:.6f} ms")

    explicar_complexidade(n=len(BASE_TREINO), d=2, k=K)


if __name__ == "__main__":
    demonstracao()
