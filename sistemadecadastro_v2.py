import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Definindo a paleta de cores
cor_fundo = "#000000"  # Preto
cor_texto = "#00FF00"  # Verde
cor_botao = "#006400"  # Verde escuro

# Função para carregar o arquivo JSON
def carregarArquivo(nomeArquivo):
    if os.path.exists(nomeArquivo):
        with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:
            dataGeral = json.load(arquivo)
        return dataGeral
    else:
        return {}

# Função para salvar o arquivo JSON
def salvarArquivo(nome_arquivo, dados):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=2, ensure_ascii=False)

# Função para adicionar um novo usuário ao arquivo JSON
def addUsuario(nomeArquivo, **usuario):
    # Garante que o telefone e o endereço tenham valores padrão se não forem fornecidos
    if "Telefone" not in usuario:
        usuario["Telefone"] = "Não Informado"
    if "Endereço" not in usuario:
        usuario["Endereço"] = "Não Informado"

    # Carrega os dados atuais do arquivo
    dados = carregarArquivo(nomeArquivo)
    # Adiciona um novo usuário ao dicionário de dados
    dados[len(dados) + 1] = usuario
    # Salva os dados atualizados no arquivo
    salvarArquivo(nomeArquivo, dados)

# Função para excluir um ou mais usuários do arquivo JSON
def excluirUsuario(nomeArquivo, *ids):
    dados = carregarArquivo(nomeArquivo)
    for id in ids:
        if str(id) in dados:
            dados[str(id)]["Status"] = False
        else:
            messagebox.showinfo("Erro", f"Usuário com ID {id} não encontrado")

    salvarArquivo(nomeArquivo, dados)

# Função para editar as informações de um usuário no arquivo JSON
def editUsuario(nomeArquivo, *ids):
    dados = carregarArquivo(nomeArquivo)
    for id in ids:
        if str(id) in dados and dados[str(id)]["Status"] == True:
            # Solicita ao usuário a opção de edição
            opcao = int(input("Qual informação deseja alterar: 1-Nome 2-Telefone 3-Endereço: "))
            if opcao == 1:
                nome = input("Insira o nome: ")
                dados[str(id)]["Nome"] = nome
            elif opcao == 2:
                telefone = input("Insira o telefone: ")
                dados[str(id)]["Telefone"] = telefone
            elif opcao == 3:
                endereco = input("Insira o endereço: ")
                dados[str(id)]["Endereço"] = endereco
            else:
                messagebox.showinfo("Erro", "Opção inválida")
        else:
            messagebox.showinfo("Erro", f"Usuário com ID {id} não encontrado")

    salvarArquivo(nomeArquivo, dados)

# Função para exibir as informações de um ou mais usuários
def exibirUsuarios(nomeArquivo, *ids):
    dados = carregarArquivo(nomeArquivo)
    for id in ids:
        if str(id) in dados and dados[str(id)]["Status"] == True:
            messagebox.showinfo(
                'Nome: {}'.format(dados[str(id)]["Nome"]),
                'Telefone: {}'.format(dados[str(id)]["Telefone"]),
                'Endereço: {}\n'.format(dados[str(id)]["Endereço"])
            )
        else:
            messagebox.showinfo("Erro", f"Usuário com ID {id} não encontrado")

# Função para exibir as informações de todos os usuários
def exibirTodosUsuarios(nomeArquivo):
    dados = carregarArquivo(nomeArquivo)
    message = ""
    for key, values in dados.items():
        if dados[key]["Status"] == True:
            message += (
                'ID: {}\n'
                'Nome: {}\n'
                'Telefone: {}\n'
                'Endereço: {}\n\n'.format(
                    key, dados[key]["Nome"], dados[key]["Telefone"], dados[key]["Endereço"]
                )
            )

    if message:
        messagebox.showinfo("Informações de Todos os Usuários", message)
    else:
        messagebox.showinfo("Informações de Todos os Usuários", "Nenhum usuário encontrado.")

# Classe que define a interface gráfica do sistema de usuários
class SistemaUsuariosApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Usuários")

        self.tabControl = ttk.Notebook(master)
        self.tabControl.pack(expand=1, fill="both")

        # Criação das abas
        self.tab_inserir = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_inserir, text="Inserir Usuário")
        self.create_inserir_tab()

        self.tab_excluir = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_excluir, text="Excluir Usuário")
        self.create_excluir_tab()

        self.tab_atualizar = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_atualizar, text="Atualizar Usuário")
        self.create_atualizar_tab()

        self.tab_info_individual = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_info_individual, text="Info Usuário Individual")
        self.create_info_individual_tab()

        self.tab_info_todos = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_info_todos, text="Info Todos os Usuários")
        self.create_info_todos_tab()

    # Métodos para criar as abas
    def create_inserir_tab(self):
        frame = ttk.Frame(self.tab_inserir)
        frame.grid(column=0, row=0, padx=10, pady=10)

        tk.Label(frame, text="Nome:").grid(column=0, row=0, sticky=tk.W)
        self.nome_entry = tk.Entry(frame, width=30)
        self.nome_entry.grid(column=1, row=0, padx=10, pady=5)

        tk.Label(frame, text="Telefone:").grid(column=0, row=1, sticky=tk.W)
        self.telefone_entry = tk.Entry(frame, width=30)
        self.telefone_entry.grid(column=1, row=1, padx=10, pady=5)

        tk.Label(frame, text="Endereço:").grid(column=0, row=2, sticky=tk.W)
        self.endereco_entry = tk.Entry(frame, width=30)
        self.endereco_entry.grid(column=1, row=2, padx=10, pady=5)

        tk.Button(frame, text="Inserir Usuário", command=self.inserir_usuario).grid(column=0, row=3, columnspan=2, pady=10)

    def create_excluir_tab(self):
        frame = ttk.Frame(self.tab_excluir)
        frame.grid(column=0, row=0, padx=10, pady=10)

        tk.Label(frame, text="IDs dos Usuários (separados por vírgula):").grid(column=0, row=0, sticky=tk.W)
        self.ids_excluir_entry = tk.Entry(frame, width=30)
        self.ids_excluir_entry.grid(column=1, row=0, padx=10, pady=5)

        tk.Button(frame, text="Excluir Usuário(s)", command=self.excluir_usuario).grid(column=0, row=1, columnspan=2, pady=10)

    def create_atualizar_tab(self):
        frame = ttk.Frame(self.tab_atualizar)
        frame.grid(column=0, row=0, padx=10, pady=10)

        tk.Label(frame, text="IDs dos Usuários (separados por vírgula):").grid(column=0, row=0, sticky=tk.W)
        self.ids_atualizar_entry = tk.Entry(frame, width=30)
        self.ids_atualizar_entry.grid(column=1, row=0, padx=10, pady=5)

        tk.Label(frame, text="Novo Nome:").grid(column=0, row=1, sticky=tk.W)
        self.novo_nome_entry = tk.Entry(frame, width=30)
        self.novo_nome_entry.grid(column=1, row=1, padx=10, pady=5)

        tk.Label(frame, text="Novo Telefone:").grid(column=0, row=2, sticky=tk.W)
        self.novo_telefone_entry = tk.Entry(frame, width=30)
        self.novo_telefone_entry.grid(column=1, row=2, padx=10, pady=5)

        tk.Label(frame, text="Novo Endereço:").grid(column=0, row=3, sticky=tk.W)
        self.novo_endereco_entry = tk.Entry(frame, width=30)
        self.novo_endereco_entry.grid(column=1, row=3, padx=10, pady=5)

        tk.Button(frame, text="Atualizar Usuário(s)", command=self.atualizar_usuario).grid(column=0, row=4, columnspan=2, pady=10)

    def create_info_individual_tab(self):
        frame = ttk.Frame(self.tab_info_individual)
        frame.grid(column=0, row=0, padx=10, pady=10)

        tk.Label(frame, text="IDs dos Usuários (separados por vírgula):").grid(column=0, row=0, sticky=tk.W)
        self.ids_info_individual_entry = tk.Entry(frame, width=30)
        self.ids_info_individual_entry.grid(column=1, row=0, padx=10, pady=5)

        tk.Button(frame, text="Obter Informações", command=self.info_individual).grid(column=0, row=1, columnspan=2, pady=10)

    def create_info_todos_tab(self):
        frame = ttk.Frame(self.tab_info_todos)
        frame.grid(column=0, row=0, padx=10, pady=10)

        tk.Button(frame, text="Obter Informações de Todos", command=self.info_todos).grid(column=0, row=0, pady=10)

    # Métodos para ações nos botões
    def inserir_usuario(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        endereco = self.endereco_entry.get()

        usuario = {"Status": True, "Nome": nome, "Telefone": telefone, "Endereço": endereco}
        addUsuario(nomeArquivo, **usuario)

        messagebox.showinfo("Sucesso", "Usuário inserido com sucesso!")

    def excluir_usuario(self):
        ids_str = self.ids_excluir_entry.get().split(",")
        ids = [int(id.strip()) for id in ids_str if id.strip()]
        excluirUsuario(nomeArquivo, *ids)
        messagebox.showinfo("Sucesso", "Usuário(s) excluído(s) com sucesso!")

    def atualizar_usuario(self):
        ids_str = self.ids_atualizar_entry.get().split(",")
        ids = [int(id.strip()) for id in ids_str if id.strip()]

        novo_nome = self.novo_nome_entry.get()
        novo_telefone = self.novo_telefone_entry.get()
        novo_endereco = self.novo_endereco_entry.get()

        if not any([novo_nome, novo_telefone, novo_endereco]):
            messagebox.showinfo("Erro", "Pelo menos um campo de atualização deve ser preenchido.")
            return

        dados = carregarArquivo(nomeArquivo)

        for id in ids:
            if str(id) in dados and dados[str(id)]["Status"] == True:
                if novo_nome:
                    dados[str(id)]["Nome"] = novo_nome
                if novo_telefone:
                    dados[str(id)]["Telefone"] = novo_telefone
                if novo_endereco:
                    dados[str(id)]["Endereço"] = novo_endereco
            
            else:
                messagebox.showinfo("Erro", f"Usuário com ID {id} não encontrado")
                return

        salvarArquivo(nomeArquivo, dados)
        messagebox.showinfo("Sucesso", "Informações do(s) usuário(s) atualizadas com sucesso!")

    def info_individual(self):
        ids_str = self.ids_info_individual_entry.get().split(",")
        ids = [int(id.strip()) for id in ids_str if id.strip()]

        if ids:
            message = ""
            for id in ids:
                usuario = carregarArquivo(nomeArquivo).get(str(id))
                if usuario and usuario["Status"]:
                    message += (
                        f'ID: {id}\n'
                        f'Nome: {usuario["Nome"]}\n'
                        f'Telefone: {usuario["Telefone"]}\n'
                        f'Endereço: {usuario["Endereço"]}\n\n'
                    )
                else:
                    messagebox.showinfo("Erro", f"Usuário com ID {id} não encontrado")

            if message:
                messagebox.showinfo("Informações do(s) Usuário(s)", message)
        else:
            messagebox.showinfo("Erro", "Nenhum ID válido fornecido")

    def info_todos(self):
        exibirTodosUsuarios(nomeArquivo)

# Nome do arquivo JSON
nomeArquivo = "projetoModuloII.json"

# Verifica se o script está sendo executado como principal
if __name__ == "__main__":
    # Criação da janela principal
    root = tk.Tk()
    # Inicialização da aplicação
    app = SistemaUsuariosApp(root)
    # Início do loop principal da interface gráfica
    root.mainloop()
