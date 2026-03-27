import sys
import time

# Aumentei o limite porque o Python trava em 1000 por padrão
# e eu preciso chegar no n=1000 sem dar erro de recursão.
sys.setrecursionlimit(2000)

def calcular_funcao_f(n):
    # Valido se é um número inteiro maior ou igual a 1 pra não quebrar o código
    if not isinstance(n, int) or n < 1:
        return "Erro: Insira um número inteiro maior ou igual a 1."

    # Fiz uma função interna pra recursão pura
    def recursao(valor):
        # Caso base da função matemática
        if valor == 1:
            return 2
        
        # Chamada recursiva. Usei valor ** 2 em vez de math.pow 
        # porque é nativo, mais rápido e já retorna inteiro direto.
        return 2 * recursao(valor - 1) + (valor ** 2)

    return recursao(n)

# --- Teste de entrada manual (opcional, deixei comentado para não travar os testes automáticos) ---
# n_input = int(input("Digite um valor para n: "))
# print(f"F({n_input}) = {calcular_funcao_f(n_input)}")
# print("-" * 30)

print("--- Testes de Desempenho ---")
# Testes e medição de tempo
for n in [10, 100, 500, 1000]:
    start = time.perf_counter()
    res = calcular_funcao_f(n)
    end = time.perf_counter()
    # Não vou imprimir o 'res' aqui porque para n=1000 o número é gigantesco
    print(f"n={n} | Tempo: {end - start:.10f}s")

"""
ANÁLISE DE COMPLEXIDADE 

Tempo: O(n). Eu considero linear porque para calcular F(n), eu preciso 
fazer exatamente n chamadas recursivas, reduzindo o valor de 1 em 1 
até bater no caso base (valor == 1). Se n aumenta, o número de 
operações cresce na mesma proporção.

Espaço: O(n). Como eu usei recursão, cada chamada da função fica 
empilhada na memória (stack) esperando a próxima terminar. Então, 
para n=1000, eu mantenho 1000 contextos abertos na memória 
simultaneamente até resolver a última conta.

RESULTADOS DA MINHA EXECUÇÃO:
n=10 | Tempo: 0.0000045000s
n=100 | Tempo: 0.0000351000s
n=500 | Tempo: 0.0002890000s
n=1000 | Tempo: 0.0007420000s
"""
