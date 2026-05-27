#!/usr/bin/env python3
"""
Sistema de triagem hospitalar usando Max-Heap.

Ideia principal:
- O paciente com maior dor deve ser atendido primeiro.
- Como a fila muda o tempo todo, usamos um Max-Heap para manter o maior valor
  sempre no topo com custo eficiente.
- Tambem implementamos Increase/Decrease Key para mudar a prioridade de um
  paciente que ja esta na fila, que e exatamente a meta do trabalho.
"""

from dataclasses import dataclass
from itertools import count
from typing import Dict, List, Optional, Tuple


@dataclass
class Paciente:
    """Representa um paciente dentro da fila de prioridade."""

    id: int
    nome: str
    dor: int
    chegada: int


class MaxHeapTriagem:
    """
    Max-Heap especializado para triagem.

    A heap fica em uma lista. Para cada indice i:
    - filho esquerdo = 2*i + 1
    - filho direito = 2*i + 2
    - pai = (i - 1) // 2

    Tambem mantemos um dicionario posicoes[id] = indice na heap. Esse detalhe
    torna possivel localizar um paciente em O(1) antes de ajustar sua dor.
    Sem esse dicionario, teriamos que procurar o paciente na lista em O(N).
    """

    def __init__(self) -> None:
        self.heap: List[Paciente] = []
        self.posicoes: Dict[int, int] = {}
        self._proximo_id = count(1)
        self._ordem_chegada = count(1)

    def inserir(self, nome: str, dor: int) -> Paciente:
        """Adiciona paciente na fila. Complexidade: O(log N)."""
        self._validar_dor(dor)

        paciente = Paciente(
            id=next(self._proximo_id),
            nome=nome.strip() or "Paciente sem nome",
            dor=dor,
            chegada=next(self._ordem_chegada),
        )

        # Inserimos no final e subimos enquanto a prioridade for maior que a do pai.
        self.heap.append(paciente)
        self.posicoes[paciente.id] = len(self.heap) - 1
        self._subir(len(self.heap) - 1)
        return paciente

    def atender_proximo(self) -> Optional[Paciente]:
        """Remove e retorna o paciente mais prioritario. Complexidade: O(log N)."""
        if not self.heap:
            return None

        paciente_atendido = self.heap[0]
        ultimo = self.heap.pop()
        del self.posicoes[paciente_atendido.id]

        # Se ainda existe alguem na fila, colocamos o ultimo na raiz e descemos.
        if self.heap:
            self.heap[0] = ultimo
            self.posicoes[ultimo.id] = 0
            self._descer(0)

        return paciente_atendido

    def alterar_dor(self, paciente_id: int, nova_dor: int) -> Paciente:
        """
        Altera a dor de um paciente que ja esta na fila.

        Se a dor aumenta, aplicamos Increase Key e o paciente pode subir.
        Se a dor diminui, aplicamos Decrease Key e o paciente pode descer.

        Complexidade:
        - localizar pelo dicionario: O(1)
        - reajustar a heap: O(log N)
        - total: O(log N)
        """
        self._validar_dor(nova_dor)

        if paciente_id not in self.posicoes:
            raise KeyError(f"Nao existe paciente com ID {paciente_id} na fila.")

        indice = self.posicoes[paciente_id]
        paciente = self.heap[indice]
        dor_antiga = paciente.dor
        paciente.dor = nova_dor

        # A direcao do ajuste depende de como a prioridade mudou.
        if nova_dor > dor_antiga:
            self._subir(indice)
        elif nova_dor < dor_antiga:
            self._descer(indice)

        return paciente

    def listar(self) -> List[Paciente]:
        """Retorna uma copia da heap no estado interno atual."""
        return list(self.heap)

    def esta_vazia(self) -> bool:
        return not self.heap

    def _prioridade(self, paciente: Paciente) -> Tuple[int, int]:
        """
        Maior dor ganha. Em empate, quem chegou antes ganha.

        Como queremos que menor chegada tenha prioridade maior, usamos -chegada.
        Exemplo: chegada 1 vira -1, que e maior que -2.
        """
        return (paciente.dor, -paciente.chegada)

    def _tem_prioridade(self, esquerda: Paciente, direita: Paciente) -> bool:
        """Compara dois pacientes seguindo a regra da triagem."""
        return self._prioridade(esquerda) > self._prioridade(direita)

    def _trocar(self, i: int, j: int) -> None:
        """Troca dois elementos e atualiza o mapa de posicoes."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.posicoes[self.heap[i].id] = i
        self.posicoes[self.heap[j].id] = j

    def _subir(self, indice: int) -> None:
        """Move um paciente para cima enquanto ele for mais prioritario que o pai."""
        while indice > 0:
            pai = (indice - 1) // 2
            if not self._tem_prioridade(self.heap[indice], self.heap[pai]):
                break
            self._trocar(indice, pai)
            indice = pai

    def _descer(self, indice: int) -> None:
        """Move um paciente para baixo ate restaurar a propriedade de Max-Heap."""
        tamanho = len(self.heap)

        while True:
            esquerda = 2 * indice + 1
            direita = 2 * indice + 2
            maior = indice

            if esquerda < tamanho and self._tem_prioridade(self.heap[esquerda], self.heap[maior]):
                maior = esquerda
            if direita < tamanho and self._tem_prioridade(self.heap[direita], self.heap[maior]):
                maior = direita

            if maior == indice:
                break

            self._trocar(indice, maior)
            indice = maior

    @staticmethod
    def _validar_dor(dor: int) -> None:
        """Garante que o nivel de dor esteja dentro da faixa pedida no enunciado."""
        if dor < 1 or dor > 10:
            raise ValueError("O nivel de dor deve estar entre 1 e 10.")


def pedir_inteiro(mensagem: str, minimo: Optional[int] = None, maximo: Optional[int] = None) -> int:
    """Le um inteiro do terminal, repetindo ate o usuario digitar um valor valido."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um numero maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um numero menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


def mostrar_fila(triagem: MaxHeapTriagem) -> None:
    """Mostra o estado interno da heap e a explicacao do topo."""
    pacientes = triagem.listar()
    if not pacientes:
        print("\nFila vazia.")
        return

    print("\nFila interna em formato de Max-Heap:")
    print("indice | id | dor | chegada | nome")
    print("-" * 45)
    for indice, paciente in enumerate(pacientes):
        print(
            f"{indice:>6} | {paciente.id:>2} | {paciente.dor:>3} | "
            f"{paciente.chegada:>7} | {paciente.nome}"
        )

    topo = pacientes[0]
    print(
        f"\nTopo da heap: ID {topo.id} - {topo.nome}, dor {topo.dor}. "
        "Esse sera o proximo atendimento."
    )


def explicar_complexidade() -> None:
    """Imprime a analise de complexidade pedida no trabalho."""
    print("\nAnalise de complexidade")
    print("-" * 26)
    print("Inserir paciente: O(log N), pois o paciente pode subir pela altura da heap.")
    print("Atender proximo: O(log N), pois a raiz e removida e o ultimo elemento desce.")
    print("Consultar proximo: O(1), pois o maior elemento fica sempre na raiz.")
    print("Alterar dor com Increase/Decrease Key: O(log N).")
    print("Motivo: o dicionario encontra o paciente em O(1), e a heap reajusta em O(log N).")
    print("Se nao existisse o dicionario de posicoes, localizar o paciente custaria O(N).")


def demonstracao() -> None:
    """Roteiro automatico para apresentar em sala sem depender de digitacao manual."""
    triagem = MaxHeapTriagem()

    print("\n=== Demonstracao automatica da triagem ===")
    dados = [
        ("Ana", 4),
        ("Bruno", 9),
        ("Carla", 6),
        ("Diego", 8),
        ("Elisa", 3),
    ]

    print("\n1) Inserindo pacientes:")
    ids = {}
    for nome, dor in dados:
        paciente = triagem.inserir(nome, dor)
        ids[nome] = paciente.id
        print(f"   Inserido ID {paciente.id}: {paciente.nome} com dor {paciente.dor}")
    mostrar_fila(triagem)

    print("\n2) Decrease Key: Bruno recebeu medicacao e caiu de dor 9 para 2.")
    triagem.alterar_dor(ids["Bruno"], 2)
    mostrar_fila(triagem)

    print("\n3) Increase Key: Carla piorou de dor 6 para 10.")
    triagem.alterar_dor(ids["Carla"], 10)
    mostrar_fila(triagem)

    print("\n4) Atendendo pacientes na ordem de prioridade:")
    while not triagem.esta_vazia():
        paciente = triagem.atender_proximo()
        print(f"   Atendimento: ID {paciente.id} - {paciente.nome}, dor {paciente.dor}")

    explicar_complexidade()


def menu_interativo() -> None:
    """Menu principal para o usuario testar livremente pelo terminal."""
    triagem = MaxHeapTriagem()

    while True:
        print("\n=== Sistema de Triagem do Pronto-Socorro ===")
        print("1 - Cadastrar paciente")
        print("2 - Atender proximo paciente")
        print("3 - Alterar dor de paciente (Increase/Decrease Key)")
        print("4 - Mostrar fila")
        print("5 - Explicar complexidade")
        print("6 - Rodar demonstracao automatica")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            nome = input("Nome do paciente: ")
            dor = pedir_inteiro("Nivel de dor (1-10): ", 1, 10)
            paciente = triagem.inserir(nome, dor)
            print(f"Paciente cadastrado com ID {paciente.id}.")

        elif opcao == "2":
            paciente = triagem.atender_proximo()
            if paciente is None:
                print("Nao ha pacientes na fila.")
            else:
                print(f"Atendendo ID {paciente.id}: {paciente.nome}, dor {paciente.dor}.")

        elif opcao == "3":
            paciente_id = pedir_inteiro("ID do paciente: ", 1)
            nova_dor = pedir_inteiro("Novo nivel de dor (1-10): ", 1, 10)
            try:
                paciente = triagem.alterar_dor(paciente_id, nova_dor)
                print(f"Prioridade atualizada: ID {paciente.id}, {paciente.nome}, dor {paciente.dor}.")
            except KeyError as erro:
                print(erro)

        elif opcao == "4":
            mostrar_fila(triagem)

        elif opcao == "5":
            explicar_complexidade()

        elif opcao == "6":
            demonstracao()

        elif opcao == "0":
            print("Encerrando o sistema de triagem.")
            break

        else:
            print("Opcao invalida. Tente novamente.")


def main() -> None:
    """Permite escolher entre demonstracao automatica e menu interativo."""
    print("Triagem hospitalar com Max-Heap")
    print("Digite 'demo' para apresentacao automatica ou pressione Enter para menu.")
    modo = input("Modo: ").strip().lower()

    if modo == "demo":
        demonstracao()
    else:
        menu_interativo()


if __name__ == "__main__":
    main()
