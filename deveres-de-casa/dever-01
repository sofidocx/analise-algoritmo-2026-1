import random
import time

def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista


tamanhos = [1000, 5000, 10000, 20000] 

print(f"{'Tamanho':<10} | {'Insertion (s)':<15} | {'Sorted (s)':<15}")
print("-" * 45)

for n in tamanhos:
    lista_original = [random.randint(0, 100000) for _ in range(n)]
    
    # Teste Insertion Sort
    lista1 = lista_original.copy()
    inicio = time.perf_counter()
    insertion_sort(lista1)
    fim = time.perf_counter()
    tempo_insertion = fim - inicio

    # Teste Timsort (Built-in)
    lista2 = lista_original.copy()
    inicio = time.perf_counter()
    sorted(lista2)
    fim = time.perf_counter()
    tempo_sorted = fim - inicio

    print(f"{n:<10} | {tempo_insertion:<15.6f} | {tempo_sorted:<15.6f}")