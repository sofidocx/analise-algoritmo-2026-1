import sys
import time

# Aumentei o limite porque o Python trava em 1000 por padrão
# e eu preciso testar arrays grandes sem dar erro de recursão.
sys.setrecursionlimit(2000)

def verificar_palindromo(arr):
    # Valido se a entrada é uma lista (array) pra não quebrar o código
    if not isinstance(arr, list):
        return "Erro: Insira uma lista/array válido."

    # Fiz uma função interna pra recursão passando os índices (esquerda e direita).
    # Faço isso para evitar fatiar a lista (arr[1:-1]), o que gastaria muita memória à toa.
    def recursao(esq, dir):
        # Caso base: se os ponteiros se cruzaram ou são iguais, tudo validou
        if esq >= dir:
            return True
        # Se os extremos forem diferentes, já não é palíndromo
        if arr[esq] != arr[dir]:
            return False
        # Chamada recursiva encurtando as pontas
        return recursao(esq + 1, dir - 1)

    return recursao(0, len(arr) - 1)

# Testes
print("Testes: ")
exemplos = [
    [0, 1, 2, 3, 2, 1, 0],
    ["a", "b", "b", "a"],
    ["a", "b", "c", "b", "a"],
    ["a", "b", "c", "f", "b", "a"]
]

for i, ex in enumerate(exemplos, 1):
    status = "É palíndromo" if verificar_palindromo(ex) else "Não é palíndromo"
    print(f"array{i} = {ex} -> {status}")

print("\n testes de desempenho:")
# Testes e medição de tempo (usando arrays preenchidos com zeros só para forçar o pior caso)
for n in [10, 100, 500, 1000]:
    array_teste = [0] * n # Cria um palíndromo de tamanho n
    
    start = time.perf_counter()
    res = verificar_palindromo(array_teste)
    end = time.perf_counter()
    print(f"n={n} | Tempo: {end - start:.10f}s")

"""
ANÁLISE DE COMPLEXIDADE 

Tempo: O(n). Eu considero linear porque eu faço uma chamada recursiva 
para cada par de elementos. No pior caso (quando o array é realmente 
um palíndromo), eu faço n/2 chamadas. Se n aumenta, o número de 
operações aumenta na mesma proporção.

Espaço: O(n). Como eu usei recursão, cada chamada ocupa um espaço na 
pilha (stack) até chegar no caso base (o meio do array). Então, n=1000 
gasta muito mais memória que n=10 porque eu mantenho até 500 estados 
abertos ao mesmo tempo.

RESULTADOS DA MINHA EXECUÇÃO:
n=10 | Tempo: 0.0000031000s
n=100 | Tempo: 0.0000213000s
n=500 | Tempo: 0.0001050000s
n=1000 | Tempo: 0.0002150000s
"""
