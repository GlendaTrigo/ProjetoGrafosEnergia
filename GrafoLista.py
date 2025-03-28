# INTEGRANTES: Arthur C. e Glenda M.
# Projeto 1 Grafos - Versão 12 (28/03/2025 - Arrumando função 9 menu)
# ANÁLISE DO CONSUMO DE ENERGIA ELÉTRICA NO BRASIL

import networkx as nx
import numpy as np
import re

class Grafo:
    def __init__(self):
        self.grafo = nx.DiGraph()
        self.nomes_vertices = {}
        self.arquivo = ""

    def carregar_grafo(self, arquivo):
        self.arquivo = arquivo
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                linhas = [linha.strip() for linha in f.readlines()]

            tipo_grafo = int(linhas[0])
            num_vertices = int(linhas[1])
            num_arestas = int(linhas[2 + num_vertices])

            for i in range(2, 2 + num_vertices):
                match = re.match(r'^\d+\s+"(.+)"\s+"([\d\.]+)"$', linhas[i])
                if match:
                    nome_cidade = match.group(1)
                    peso = float(match.group(2))
                    self.grafo.add_node(i - 2, cidade=nome_cidade, peso=peso)
                    self.nomes_vertices[i - 2] = nome_cidade
                else:
                    raise ValueError(f"Erro ao processar linha de vértice: {linhas[i]}")

            for i in range(3 + num_vertices, 3 + num_vertices + num_arestas):
                dados = linhas[i].split()
                if len(dados) != 3:
                    raise ValueError(f"Erro ao processar linha de aresta: {linhas[i]}")
                origem, destino, peso = int(dados[0]), int(dados[1]), float(dados[2])
                self.grafo.add_edge(origem, destino, peso=peso)

            print("\n✅ Grafo carregado com sucesso!\n")
        except Exception as e:
            print(f"\n❌ Erro ao carregar o grafo: {e}\n")
    
    def salvar_grafo(self):
        try:
            with open(self.arquivo, "w", encoding="utf-8") as f:
                f.write("7\n")
                f.write(f"{self.grafo.number_of_nodes()}\n")
                for node in sorted(self.grafo.nodes()):
                    cidade = self.grafo.nodes[node]['cidade']
                    peso = self.grafo.nodes[node]['peso']
                    f.write(f'{node} "{cidade}" "{peso}"\n')
                f.write(f"{self.grafo.number_of_edges()}\n")
                for origem, destino, data in self.grafo.edges(data=True):
                    f.write(f"{origem} {destino} {data['peso']}\n")
            print("\n💾 Grafo salvo com sucesso!\n")
        except Exception as e:
            print(f"\n❌ Erro ao salvar o grafo: {e}\n")
    
    def mostrar_conteudo_arquivo(self):
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                print("\n📂 Conteúdo do Arquivo:\n")
                print(f.read())
        except Exception as e:
            print(f"\n❌ Erro ao ler o arquivo: {e}\n")
    
    def mostrar_grafo(self):
        print("\n📊 Representação do Grafo:")
        print("\nLista de Adjacência:")
        for node in sorted(self.grafo.nodes()):
            vizinhos = sorted(self.grafo.successors(node))
            print(f"{node}: {vizinhos}")
        
        print("\nMatriz de Adjacência:")
        nodes_sorted = sorted(self.grafo.nodes())
        index_map = {node: i for i, node in enumerate(nodes_sorted)}
        n = len(nodes_sorted)
        matriz = np.zeros((n, n), dtype=int)
        
        for origem, destino in self.grafo.edges():
            matriz[index_map[origem]][index_map[destino]] = 1
        
        print("   " + " ".join(f"{nodes_sorted[i]:2}" for i in range(n)))
        for i in range(n):
            print(f"{nodes_sorted[i]:2} " + " ".join(f"{matriz[i][j]:2}" for j in range(n)))
    
    def inserir_vertice(self, vertice, nome, peso):
        self.grafo.add_node(vertice, cidade=nome, peso=peso)
        self.nomes_vertices[vertice] = nome
        print(f"\n✅ Vértice {vertice} ({nome}) inserido com sucesso!\n")
    
    def inserir_aresta(self, origem, destino, peso):
        self.grafo.add_edge(origem, destino, peso=peso)
        print(f"\n✅ Aresta de {origem} para {destino} inserida com sucesso!\n")
    
    def remover_vertice(self, vertice):
        if self.grafo.has_node(vertice):
            self.grafo.remove_node(vertice)
            del self.nomes_vertices[vertice]
            print(f"\n✅ Vértice {vertice} removido com sucesso!\n")
        else:
            print("\n❌ Vértice não encontrado.\n")
    
    def remover_aresta(self, origem, destino):
        if self.grafo.has_edge(origem, destino):
            self.grafo.remove_edge(origem, destino)
            print(f"\n✅ Aresta de {origem} para {destino} removida com sucesso!\n")
        else:
            print("\n❌ Aresta não encontrada.\n")
    
    def conexidade_grafo(self):
        if nx.is_strongly_connected(self.grafo):
            print("\n🌐 O grafo é **fortemente conexo (C3)**.")
        elif nx.is_weakly_connected(self.grafo):
            print("\n🔗 O grafo é **simplesmente conexo (C2)**.")
        elif any(len(c) > 1 for c in nx.strongly_connected_components(self.grafo)):
            print("\n🌀 O grafo é **semi fortemente conexo (C1)**.")
        else:
            print("\n🚧 O grafo é **desconexo (C0)**.")

def menu():
    grafo = Grafo()
    arquivo = "grafo.txt"
    grafo.carregar_grafo(arquivo)
    
    while True:
        opcao = input("\n📌 MENU\n1. Mostrar Arquivo\n2. Mostrar Grafo\n3. Inserir Vértice\n4. Inserir Aresta\n5. Remover Vértice\n6. Remover Aresta\n7. Conexidade\n8. Salvar e Sair\n9. Sair\nEscolha: ")
        if opcao == "1": grafo.mostrar_conteudo_arquivo()
        elif opcao == "2": grafo.mostrar_grafo()
        elif opcao == "3": grafo.inserir_vertice(int(input("Vértice: ")), input("Nome: "), float(input("Peso: ")))
        elif opcao == "4": grafo.inserir_aresta(int(input("Origem: ")), int(input("Destino: ")), float(input("Peso: ")))
        elif opcao == "5": grafo.remover_vertice(int(input("Vértice: ")))
        elif opcao == "6": grafo.remover_aresta(int(input("Origem: ")), int(input("Destino: ")))
        elif opcao == "7": grafo.conexidade_grafo()
        elif opcao == "8": grafo.salvar_grafo(); break
        elif opcao == "9": break

if __name__ == "__main__":
    menu()
