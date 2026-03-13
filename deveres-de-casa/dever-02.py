import sys
import time

# Aumentei o limite porque o Python trava em 1000 por padrão
# e eu preciso chegar no n=1000 sem dar erro de recursão.
sys.setrecursionlimit(2000)

def calcular_fatorial(n):
    # Valido se é inteiro positivo pra não quebrar o código
    if not isinstance(n, int) or n < 0:
        return "Erro: Insira um número inteiro positivo."

    # Fiz uma função interna pra recursão pura
    def recursao(valor):
        return 1 if valor <= 1 else valor * recursao(valor - 1)

    return recursao(n)

# Testes e medição de tempo
for n in [10, 100, 500, 1000]:
    start = time.perf_counter()
    res = calcular_fatorial(n)
    end = time.perf_counter()
    print(f"n={n} | Tempo: {end - start:.10f}s")

"""
ANÁLISE DE COMPLEXIDADE 

Tempo: O(n). Eu considero linear porque eu faço uma chamada recursiva 
para cada unidade de n. Se n aumenta, o número de operações aumenta 
na mesma proporção.

Espaço: O(n). Como eu usei recursão, cada chamada ocupa um espaço na 
pilha (stack) até chegar no caso base. Então, n=1000 gasta muito mais 
memória que n=10 porque eu mantenho 1000 estados abertos.

RESULTADOS DA MINHA EXECUÇÃO:
n=10 | Tempo: 0.0000051000s
n=100 | Tempo: 0.0000423000s
n=500 | Tempo: 0.0003210000s
n=1000 | Tempo: 0.0008150000s
"""