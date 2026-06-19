#!/usr/bin/env python3
"""
Dever 5 - Simulated Annealing nas 12-Rainhas.

O script compara a convergencia de Simulated Annealing (SA) com um Algoritmo
Genetico (AG) simples. A curva de convergencia usa o menor numero de conflitos
encontrado ao longo das iteracoes: quanto mais perto de 0, melhor.
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path
from time import perf_counter
from typing import List, Tuple


N = 12
MAX_CONFLITOS = N * (N - 1) // 2
SEMENTE = 42


Tabuleiro = List[int]


def criar_tabuleiro(n: int = N) -> Tabuleiro:
    """
    Representa uma solucao como lista: indice=coluna, valor=linha da rainha.

    Usamos uma permutacao de 0..n-1. Assim, nunca existem duas rainhas na mesma
    linha e a busca precisa se preocupar apenas com diagonais.
    """
    tabuleiro = list(range(n))
    random.shuffle(tabuleiro)
    return tabuleiro


def conflitos(tabuleiro: Tabuleiro) -> int:
    """Conta pares de rainhas em conflito na mesma linha ou diagonal."""
    total = 0
    n = len(tabuleiro)

    for col_a in range(n):
        for col_b in range(col_a + 1, n):
            mesma_diagonal = abs(tabuleiro[col_a] - tabuleiro[col_b]) == abs(col_a - col_b)
            if mesma_diagonal:
                total += 1

    return total


def vizinho(tabuleiro: Tabuleiro) -> Tabuleiro:
    """Gera um vizinho trocando duas rainhas de linha."""
    n = len(tabuleiro)
    novo = tabuleiro.copy()
    col_a, col_b = random.sample(range(n), 2)
    novo[col_a], novo[col_b] = novo[col_b], novo[col_a]
    return novo


def simulated_annealing(
    n: int = N,
    iteracoes: int = 3000,
    temperatura_inicial: float = 12.0,
    resfriamento: float = 0.997,
) -> Tuple[Tabuleiro, int, List[int]]:
    """Executa o loop principal do Simulated Annealing."""
    atual = criar_tabuleiro(n)
    custo_atual = conflitos(atual)
    melhor = atual.copy()
    melhor_custo = custo_atual
    temperatura = temperatura_inicial
    curva = []

    for _ in range(iteracoes):
        candidato = vizinho(atual)
        custo_candidato = conflitos(candidato)
        delta = custo_candidato - custo_atual

        if delta <= 0 or random.random() < math.exp(-delta / max(temperatura, 1e-9)):
            atual = candidato
            custo_atual = custo_candidato

        if custo_atual < melhor_custo:
            melhor = atual.copy()
            melhor_custo = custo_atual

        curva.append(melhor_custo)

        if melhor_custo == 0:
            curva.extend([0] * (iteracoes - len(curva)))
            break

        temperatura *= resfriamento

    return melhor, melhor_custo, curva


def fitness(tabuleiro: Tabuleiro) -> int:
    """Fitness maior e melhor: total de pares sem conflito."""
    return MAX_CONFLITOS - conflitos(tabuleiro)


def torneio(populacao: List[Tabuleiro], tamanho: int = 3) -> Tabuleiro:
    """Seleciona o melhor individuo entre alguns sorteados."""
    candidatos = random.sample(populacao, tamanho)
    return max(candidatos, key=fitness).copy()


def cruzamento(pai: Tabuleiro, mae: Tabuleiro) -> Tabuleiro:
    """Crossover ordenado para manter a permutacao valida."""
    n = len(pai)
    inicio, fim = sorted(random.sample(range(n), 2))
    filho = [None] * n
    filho[inicio:fim] = pai[inicio:fim]

    posicao = fim
    for valor in mae[fim:] + mae[:fim]:
        if valor not in filho:
            if posicao == n:
                posicao = 0
            filho[posicao] = valor
            posicao += 1

    return [int(valor) for valor in filho]


def mutar(tabuleiro: Tabuleiro, taxa: float = 0.08) -> None:
    """Troca duas colunas com pequena probabilidade."""
    n = len(tabuleiro)
    if random.random() < taxa:
        col_a, col_b = random.sample(range(n), 2)
        tabuleiro[col_a], tabuleiro[col_b] = tabuleiro[col_b], tabuleiro[col_a]


def algoritmo_genetico(
    n: int = N,
    geracoes: int = 3000,
    tamanho_populacao: int = 60,
    elitismo: int = 4,
) -> Tuple[Tabuleiro, int, List[int]]:
    """AG simples para comparar com SA."""
    populacao = [criar_tabuleiro(n) for _ in range(tamanho_populacao)]
    melhor = min(populacao, key=conflitos).copy()
    melhor_custo = conflitos(melhor)
    curva = []

    for _ in range(geracoes):
        populacao.sort(key=conflitos)
        if conflitos(populacao[0]) < melhor_custo:
            melhor = populacao[0].copy()
            melhor_custo = conflitos(melhor)

        curva.append(melhor_custo)
        if melhor_custo == 0:
            curva.extend([0] * (geracoes - len(curva)))
            break

        nova_populacao = [individuo.copy() for individuo in populacao[:elitismo]]
        while len(nova_populacao) < tamanho_populacao:
            pai = torneio(populacao)
            mae = torneio(populacao)
            filho = cruzamento(pai, mae)
            mutar(filho)
            nova_populacao.append(filho)

        populacao = nova_populacao

    return melhor, melhor_custo, curva


def salvar_curvas(curva_sa: List[int], curva_ag: List[int], pasta: Path) -> None:
    """Salva CSV, SVG e tenta salvar PNG com as curvas de convergencia."""
    csv_path = pasta / "dever05-curvas-convergencia.csv"
    svg_path = pasta / "dever05-curvas-convergencia.svg"
    png_path = pasta / "dever05-curvas-convergencia.png"

    limite = min(len(curva_sa), len(curva_ag))
    with csv_path.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["iteracao", "simulated_annealing", "algoritmo_genetico"])
        for i in range(limite):
            escritor.writerow([i + 1, curva_sa[i], curva_ag[i]])

    largura, altura = 900, 520
    margem = 60
    max_y = max(max(curva_sa[:limite]), max(curva_ag[:limite]), 1)

    def pontos(curva: List[int]) -> str:
        coords = []
        for i, valor in enumerate(curva[:limite]):
            x = margem + (i / max(1, limite - 1)) * (largura - 2 * margem)
            y = altura - margem - (valor / max_y) * (altura - 2 * margem)
            coords.append(f"{x:.1f},{y:.1f}")
        return " ".join(coords)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{largura}" height="{altura}" viewBox="0 0 {largura} {altura}">
  <rect width="100%" height="100%" fill="white"/>
  <text x="{largura / 2}" y="32" text-anchor="middle" font-family="Arial" font-size="22">Convergencia nas 12-Rainhas</text>
  <line x1="{margem}" y1="{altura - margem}" x2="{largura - margem}" y2="{altura - margem}" stroke="#333"/>
  <line x1="{margem}" y1="{margem}" x2="{margem}" y2="{altura - margem}" stroke="#333"/>
  <text x="{largura / 2}" y="{altura - 15}" text-anchor="middle" font-family="Arial" font-size="14">Iteracao/Geracao</text>
  <text x="18" y="{altura / 2}" transform="rotate(-90 18 {altura / 2})" text-anchor="middle" font-family="Arial" font-size="14">Melhor numero de conflitos</text>
  <polyline points="{pontos(curva_sa)}" fill="none" stroke="#2563eb" stroke-width="3"/>
  <polyline points="{pontos(curva_ag)}" fill="none" stroke="#dc2626" stroke-width="3"/>
  <rect x="{largura - 230}" y="58" width="170" height="58" fill="white" stroke="#ccc"/>
  <line x1="{largura - 215}" y1="78" x2="{largura - 175}" y2="78" stroke="#2563eb" stroke-width="3"/>
  <text x="{largura - 165}" y="83" font-family="Arial" font-size="14">SA</text>
  <line x1="{largura - 215}" y1="102" x2="{largura - 175}" y2="102" stroke="#dc2626" stroke-width="3"/>
  <text x="{largura - 165}" y="107" font-family="Arial" font-size="14">AG</text>
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(9, 5))
        plt.plot(range(1, limite + 1), curva_sa[:limite], label="SA")
        plt.plot(range(1, limite + 1), curva_ag[:limite], label="AG")
        plt.xlabel("Iteracao/Geracao")
        plt.ylabel("Melhor numero de conflitos")
        plt.title("Convergencia nas 12-Rainhas")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(png_path, dpi=150)
        plt.close()
        print(f"Grafico salvo em: {png_path}")
    except Exception as erro:
        print("Matplotlib nao disponivel; use o CSV para montar o grafico.")
        print(f"Motivo: {erro}")

    print(f"SVG salvo em: {svg_path}")
    print(f"CSV salvo em: {csv_path}")


def explicar_complexidade(iteracoes: int, populacao: int) -> None:
    """Imprime a analise de complexidade pedida."""
    print("\nAnalise de complexidade")
    print("-" * 26)
    print("Para n rainhas, avaliar conflitos custa O(n^2), pois compara pares de rainhas.")
    print(f"SA executa {iteracoes} iteracoes, entao o tempo e O(iteracoes * n^2).")
    print("A memoria do SA e O(n), alem da curva guardada para o grafico.")
    print(f"AG avalia uma populacao P={populacao} por geracao.")
    print("Tempo do AG: O(geracoes * P * n^2), ignorando constantes de selecao e mutacao.")
    print("Na pratica, SA tende a ser mais barato por iteracao porque trabalha com um unico estado,")
    print("enquanto o AG pode precisar de menos geracoes, mas avalia muitos individuos por geracao.")


def demonstracao() -> None:
    """Roda SA e AG, imprime resultados, tempos e salva as curvas."""
    random.seed(SEMENTE)
    iteracoes = 3000
    tamanho_populacao = 60

    print("=== Dever 5 - Simulated Annealing nas 12-Rainhas ===")

    inicio_sa = perf_counter()
    solucao_sa, custo_sa, curva_sa = simulated_annealing(iteracoes=iteracoes)
    fim_sa = perf_counter()

    inicio_ag = perf_counter()
    solucao_ag, custo_ag, curva_ag = algoritmo_genetico(
        geracoes=iteracoes,
        tamanho_populacao=tamanho_populacao,
    )
    fim_ag = perf_counter()

    print("\nResultado SA")
    print(f"Melhor tabuleiro: {solucao_sa}")
    print(f"Conflitos: {custo_sa}")
    print(f"Tempo de execucao: {(fim_sa - inicio_sa) * 1000:.3f} ms")
    print(f"Iteracao em que zerou conflitos: {curva_sa.index(0) + 1 if 0 in curva_sa else 'nao zerou'}")

    print("\nResultado AG")
    print(f"Melhor tabuleiro: {solucao_ag}")
    print(f"Conflitos: {custo_ag}")
    print(f"Tempo de execucao: {(fim_ag - inicio_ag) * 1000:.3f} ms")
    print(f"Geracao em que zerou conflitos: {curva_ag.index(0) + 1 if 0 in curva_ag else 'nao zerou'}")

    salvar_curvas(curva_sa, curva_ag, Path(__file__).resolve().parent)

    print("\nParagrafo curto para a entrega")
    print("-" * 33)
    print("No teste, comparei as curvas pelo numero de conflitos ao longo do tempo.")
    if 0 in curva_sa and (0 not in curva_ag or curva_sa.index(0) <= curva_ag.index(0)):
        print("O SA convergiu mais rapido, chegando a uma solucao sem conflitos antes do AG.")
    elif 0 in curva_ag:
        print("O AG convergiu mais rapido neste experimento, chegando primeiro a 0 conflitos.")
    else:
        print("Nenhum dos dois zerou conflitos no limite escolhido, entao comparei o menor custo final.")
    print("A diferenca ocorre porque SA explora vizinhos com temperatura decrescente, enquanto")
    print("o AG depende da qualidade da populacao, cruzamentos e mutacoes ao longo das geracoes.")

    explicar_complexidade(iteracoes=iteracoes, populacao=tamanho_populacao)


if __name__ == "__main__":
    demonstracao()
