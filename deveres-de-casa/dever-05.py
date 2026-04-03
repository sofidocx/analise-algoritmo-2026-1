import sys
import time
import random

# Aumentei o limite de recursão por segurança, já que o Merge Sort usa recursão
sys.setrecursionlimit(2000)

# 1) ALGORITMO MERGE SORT
def merge_sort(arr):
    # Caso base: se o array tiver tamanho 1 ou 0, já tá ordenado
    if len(arr) <= 1:
        return arr
    
    # Divido o array bem no meio
    meio = len(arr) // 2
    
    # Faço a chamada recursiva pras duas metades
    esq = merge_sort(arr[:meio])
    dir = merge_sort(arr[meio:])
    
    # Função interna pra fazer o "merge" (juntar as metades já ordenadas)
    def juntar(esq, dir):
        resultado = []
        i = j = 0
        
        # Vou comparando e pegando o menor de cada lado
        while i < len(esq) and j < len(dir):
            if esq[i] < dir[j]:
                resultado.append(esq[i])
                i += 1
            else:
                resultado.append(dir[j])
                j += 1
                
        # Adiciono o que sobrar de qualquer um dos lados
        resultado.extend(esq[i:])
        resultado.extend(dir[j:])
        return resultado
        
    return juntar(esq, dir)

# 2) MULTIPLICAÇÃO DE MATRIZES
def multiplicar_matrizes(A, B):
    n = len(A)
    # Crio uma matriz de zeros do tamanho n x n pra guardar a resposta
    C = [[0] * n for _ in range(n)]
    
    # Faço o jeito clássico com 3 loops pra multiplicar linha por coluna
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

print("--- Testes de Desempenho: MERGE SORT ---")
for n in [10, 100, 500, 1000]:
    # Gero um array aleatório de tamanho n pra não testar com dados viciados
    array_teste = [random.randint(0, 1000) for _ in range(n)]
    
    start = time.perf_counter()
    res_merge = merge_sort(array_teste)
    end = time.perf_counter()
    print(f"n={n:<4} | Tempo Merge Sort: {end - start:.10f}s")

print("\n--- Testes de Desempenho: MATRIZES ---")
# Reduzi os valores de n aqui porque O(n^3) para n=1000 travaria o PC (bilhões de iterações)
for n in [10, 50, 100, 200]:
    # Gero duas matrizes aleatórias n x n
    matriz_a = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    matriz_b = [[random.randint(1, 10) for _ in range(n)] for _ in range(n)]
    
    start = time.perf_counter()
    res_matriz = multiplicar_matrizes(matriz_a, matriz_b)
    end = time.perf_counter()
    print(f"n={n:<4} | Tempo Matrizes:   {end - start:.10f}s")

"""
ANÁLISE DE COMPLEXIDADE DO DEVER DE CASA

1) ALGORITMO DE ORDENAÇÃO MERGE SORT:
Tempo: O(n log n). Eu considero isso porque o algoritmo divide o array 
na metade repetidas vezes (o que me dá uma altura de árvore log n) e, 
para cada nível dessa divisão, eu percorro todos os n elementos para 
juntar tudo. Fica n vezes log n.
Espaço: O(n). Na hora de fazer o "merge", eu preciso criar listas 
auxiliares para montar o array ordenado de novo, gastando memória extra 
proporcional ao tamanho da entrada.

2) MULTIPLICAÇÃO DE MATRIZES:
Tempo: O(n³). Como eu implementei a forma padrão, eu precisei usar três 
loops `for` aninhados (o i, o j e o k) indo de 0 até n. Então, se o 
n cresce, as operações crescem ao cubo.
Espaço: O(n²). Eu preciso criar uma matriz auxiliar C de dimensões 
n x n para conseguir armazenar o resultado da multiplicação.

3) CÁLCULO DAS RECORRÊNCIAS (Teorema Mestre):
Eu usei o formato clássico $T(n) = aT(n/b) + f(n)$ e comparei $f(n)$ com $n^{\log_b a}$.

a) $T(n) = 2T(n/4) + \sqrt{n}$
- Aqui eu tenho $a=2$, $b=4$ e $f(n) = n^{0.5}$ (raiz de n).
- Calculando o limite: $n^{\log_4 2} = n^{0.5}$.
- Como $f(n)$ é exatamente igual a $n^{\log_b a}$, eu caio direto no Caso 2 do Teorema Mestre.
- Resultado: $\Theta(\sqrt{n} \log n)$

b) $T(n) = 2T(n/4) + n$
- Aqui eu tenho $a=2$, $b=4$ e $f(n) = n^1$.
- Calculando o limite de novo: $n^{\log_4 2} = n^{0.5}$.
- Como o meu $f(n)$ cresce muito mais rápido que $n^{0.5}$, eu caio no Caso 3. (A condição de regularidade também bate porque $2(n/4) \le c \cdot n$ para $c=0.5$).
- Resultado: $\Theta(n)$

c) $T(n) = 16T(n/4) + n^2$
- Aqui eu tenho $a=16$, $b=4$ e $f(n) = n^2$.
- Calculando o limite: $n^{\log_4 16} = n^2$.
- Mais uma vez, $f(n)$ bate certinho com $n^{\log_b a}$. Cai no Caso 2 de novo.
- Resultado: $\Theta(n^2 \log n)$
"""
