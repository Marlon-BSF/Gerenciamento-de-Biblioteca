from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'chave-secreta'
app.config['PORT'] = 15243

# Caminhos para os arquivos
ARQ_LIVROS = "livros.txt"
ARQ_USUARIOS = "usuarios.txt"
ARQ_EMPRESTIMOS = "emprestimos.txt"
ARQ_HISTORICO = "historico.txt"

def salvar_usuario(nome, email, senha):
    with open(ARQ_USUARIOS, 'a', encoding='utf-8') as f:
        f.write(f"{nome};{email};{senha}\n")

def validar_login(email, senha):
    if not os.path.exists(ARQ_USUARIOS):
        return False
    with open(ARQ_USUARIOS, 'r', encoding='utf-8') as f:
        for linha in f:
            _, e, s = linha.strip().split(';')
            if e == email and s == senha:
                return True
    return False

def ler_arquivo(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, 'r', encoding='utf-8') as f:
        return [linha.strip().split(';') for linha in f.readlines()]

def adicionar_linha(caminho, linha):
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(';'.join(linha) + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    if validar_login(email, senha):
        session['usuario'] = email
        return redirect(url_for('biblioteca'))
    return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/salvar_cadastro', methods=['POST'])
def salvar_cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    salvar_usuario(nome, email, senha)
    return redirect(url_for('index'))

# Funções para gerenciar livros e empréstimos
@app.route('/biblioteca')
def biblioteca():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    livros = ler_arquivo(ARQ_LIVROS)
    emprestimos = ler_arquivo(ARQ_EMPRESTIMOS)
    return render_template('biblioteca.html', usuario=session['usuario'], livros=livros, emprestimos=emprestimos)

@app.route('/cadastrar_livro', methods=['POST'])
def cadastrar_livro():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    titulo = request.form['titulo']
    autor = request.form['autor']
    editora = request.form['editora']
    ano = request.form['ano']
    genero = request.form['genero']
    isbn = request.form['isbn']
    
    adicionar_linha(ARQ_LIVROS, [titulo, autor, editora, ano, genero, isbn])
    
    return redirect(url_for('biblioteca'))

@app.route('/emprestar_livro', methods=['POST'])
def emprestar_livro():
    if 'usuario' not in session:
        return redirect(url_for('index'))

    email_usuario = session['usuario']
    livro_idx = int(request.form['livro_idx'])
    prazo = request.form['prazo']
    
    livros = ler_arquivo(ARQ_LIVROS)
    livro = livros[livro_idx]
    titulo = livro[0]
    data_retirada = datetime.now().strftime('%Y-%m-%d')
    
    adicionar_linha(ARQ_EMPRESTIMOS, [email_usuario, titulo, data_retirada, prazo])
    
    return redirect(url_for('biblioteca'))

@app.route('/devolver_livro', methods=['POST'])
def devolver_livro():
    if 'usuario' not in session:
        return redirect(url_for('index'))

    email_usuario = session['usuario']
    emprestimos = ler_arquivo(ARQ_EMPRESTIMOS)
    livro_idx = int(request.form['livro_idx'])
    
    emprestimo = emprestimos[livro_idx]
    emprestimos.remove(emprestimo)
    
    adicionar_linha(ARQ_HISTORICO, emprestimo + [datetime.now().strftime('%Y-%m-%d')])
    
    with open(ARQ_EMPRESTIMOS, 'w', encoding='utf-8') as f:
        for e in emprestimos:
            f.write(';'.join(e) + '\n')
    
    return redirect(url_for('biblioteca'))

@app.route('/historico')
def historico_usuario():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    historico = ler_arquivo(ARQ_HISTORICO)
    usuario_historico = [h for h in historico if h[0] == session['usuario']]
    
    return render_template('historico.html', historico=usuario_historico)

if __name__ == '__main__':
    app.run(port=app.config['PORT'])
