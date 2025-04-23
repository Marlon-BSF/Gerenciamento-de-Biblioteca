import os
from datetime import datetime

# Caminhos dos arquivos
ARQ_LIVROS = "livros.txt"
ARQ_USUARIOS = "usuarios.txt"
ARQ_EMPRESTIMOS = "emprestimos.txt"
ARQ_HISTORICO = "historico.txt"

# Utilitários
def ler_arquivo(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, 'r', encoding='utf-8') as f:
        return [linha.strip().split(';') for linha in f.readlines()]

def escrever_arquivo(caminho, linhas):
    with open(caminho, 'w', encoding='utf-8') as f:
        for linha in linhas:
            f.write(';'.join(linha) + '\n')

def adicionar_linha(caminho, linha):
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(';'.join(linha) + '\n')

# Cadastro de livros (R1)
def cadastrar_livro():
    titulo = input("Título: ")
    autor = input("Autor: ")
    editora = input("Editora: ")
    ano = input("Ano de publicação: ")
    genero = input("Gênero: ")
    isbn = input("ISBN: ")
    adicionar_linha(ARQ_LIVROS, [titulo, autor, editora, ano, genero, isbn])
    print("Livro cadastrado com sucesso!")

# Edição de livros (R2)
def editar_livro():
    livros = ler_arquivo(ARQ_LIVROS)
    listar_livros()
    idx = int(input("Digite o índice do livro a editar: "))
    if 0 <= idx < len(livros):
        print("Deixe em branco para manter o valor atual.")
        for i, campo in enumerate(["Título", "Autor", "Editora", "Ano", "Gênero", "ISBN"]):
            novo = input(f"{campo} ({livros[idx][i]}): ")
            if novo:
                livros[idx][i] = novo
        escrever_arquivo(ARQ_LIVROS, livros)
        print("Livro editado com sucesso.")
    else:
        print("Índice inválido.")

# Exclusão de livros (R3)
def excluir_livro():
    livros = ler_arquivo(ARQ_LIVROS)
    listar_livros()
    idx = int(input("Digite o índice do livro a excluir: "))
    if 0 <= idx < len(livros):
        livros.pop(idx)
        escrever_arquivo(ARQ_LIVROS, livros)
        print("Livro excluído.")
    else:
        print("Índice inválido.")

def listar_livros():
    livros = ler_arquivo(ARQ_LIVROS)
    for i, livro in enumerate(livros):
        print(f"[{i}] - {livro}")

# Cadastro de usuário (R7)
def cadastrar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    senha = input("Senha: ")
    adicionar_linha(ARQ_USUARIOS, [nome, email, senha])
    print("Usuário cadastrado.")

# Login (R8)
def login():
    email = input("Email: ")
    senha = input("Senha: ")
    usuarios = ler_arquivo(ARQ_USUARIOS)
    for usuario in usuarios:
        if usuario[1] == email and usuario[2] == senha:
            print("Login bem-sucedido!")
            return email
    print("Credenciais inválidas.")
    return None

# Registro de empréstimo (R4)
def emprestar_livro(email_usuario):
    listar_livros()
    livros = ler_arquivo(ARQ_LIVROS)
    idx = int(input("Digite o índice do livro a emprestar: "))
    if 0 <= idx < len(livros):
        titulo = livros[idx][0]
        data_retirada = datetime.now().strftime('%Y-%m-%d')
        prazo = input("Prazo para devolução (ex: 7 dias): ")
        adicionar_linha(ARQ_EMPRESTIMOS, [email_usuario, titulo, data_retirada, prazo])
        print("Empréstimo registrado.")

# Registro de devolução (R5)
def devolver_livro(email_usuario):
    emprestimos = ler_arquivo(ARQ_EMPRESTIMOS)
    ativos = [e for e in emprestimos if e[0] == email_usuario]
    for i, e in enumerate(ativos):
        print(f"[{i}] - Livro: {e[1]}, Data: {e[2]}, Prazo: {e[3]}")
    idx = int(input("Digite o índice do empréstimo a devolver: "))
    if 0 <= idx < len(ativos):
        devolvido = ativos[idx]
        emprestimos.remove(devolvido)
        escrever_arquivo(ARQ_EMPRESTIMOS, emprestimos)
        adicionar_linha(ARQ_HISTORICO, devolvido + [datetime.now().strftime('%Y-%m-%d')])
        print("Livro devolvido.")
    else:
        print("Índice inválido.")

# Histórico por usuário (R6)
def historico_usuario(email_usuario):
    historico = ler_arquivo(ARQ_HISTORICO)
    print(f"Histórico de {email_usuario}:")
    for h in historico:
        if h[0] == email_usuario:
            print(f"Livro: {h[1]} | Retirada: {h[2]} | Prazo: {h[3]} | Devolução: {h[4]}")

# Menu principal
def menu():
    while True:
        print("\n1. Login\n2. Cadastrar Usuário\n0. Sair")
        op = input("Escolha: ")
        if op == '1':
            email = login()
            if email:
                menu_usuario(email)
        elif op == '2':
            cadastrar_usuario()
        elif op == '0':
            break

# Menu após login
def menu_usuario(email):
    while True:
        print("\n1. Cadastrar Livro\n2. Editar Livro\n3. Excluir Livro\n4. Emprestar Livro\n5. Devolver Livro\n6. Ver Histórico\n0. Logout")
        op = input("Escolha: ")
        if op == '1':
            cadastrar_livro()
        elif op == '2':
            editar_livro()
        elif op == '3':
            excluir_livro()
        elif op == '4':
            emprestar_livro(email)
        elif op == '5':
            devolver_livro(email)
        elif op == '6':
            historico_usuario(email)
        elif op == '0':
            break

if __name__ == "__main__":
    menu()
