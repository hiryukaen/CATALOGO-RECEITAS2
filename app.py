from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import random

from core.utils.postgresql_crud import PostgreSQLCRUD

# importamos a classe Usuario
from core.usuario.usuario import Usuario

app = Flask(__name__)
app.secret_key = '1234567890abcdef'

# Configuração do banco de dados PostgreSQL
#DATABASE_URL = "postgresql://postgresql_usuario_user:sLsZ0dqBk1d7GAvsXzFTOyLIxnLbF2eN@dpg-cu9c183tq21c73ahm080-a/postgresql_usuario"

#def connect_db():
#    return psycopg2.connect(DATABASE_URL)

# Inicializar o banco de dados
# def init_db():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS usuario (
#             id SERIAL PRIMARY KEY,
#             nome TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             senha TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

###init_db()

imagens = [
    'image/fundoazul.png',
    'image/fundoazulclaro.png',
    'image/fundocaderno.png',
    'image/fundofarinha.png',
    'image/fundoblack.jpeg',
    'image/fundoroxo.jpeg',
    'image/fundopardo.jpeg',
    'image/fundopardoitens.jpeg',
    'image/fundomadeira.jpeg',
    'image/fundobraco.jpeg',
    'image/fundoverde.png',
    'image/fundoitens.png'
]

bd_usuario = {
    "email": "anderson@gmail.com",
    "senha": "123"
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        imagem_escolhida = random.choice(imagens)
        return render_template('login.html', imagem_fundo=imagem_escolhida)
    elif request.method == 'POST':
        email = request.form['email'] 
        senha = request.form['senha']
        if email == bd_usuario['email'] and senha == bd_usuario['senha']:
            session['usuario'] = email
            return redirect(url_for('home'))


@app.route('/home')
def home():
    if 'usuario' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/sair')
def sair():
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route('/usuario', methods=['GET', 'POST'])
def usuario():
    if 'usuario' in session:
        if request.method == 'GET':
            return render_template('usuario.html')
        elif request.method == 'POST':
            nome = request.form['nome']
            email = request.form['email']
            senha = request.form['senha']
            conf_senha = request.form['conf-senha']
            situacao = request.form['situacao']
            
            if senha == conf_senha:
                obj_usuario = Usuario(nome, email, senha, situacao)
    else:
        return redirect(url_for('login'))

@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/receita')
def receita():
    return render_template('receita.html')


@app.route('/categoria')
def categoria():
    return render_template('categoria.html')


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            db = PostgreSQLCRUD()
            db.create("usuario", nome = nome, email = email, senha = senha)

            # conn = connect_db()
            # cursor = conn.cursor()
            # cursor.execute("INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            # conn.commit()
            # conn.close()
            return redirect(url_for("sucesso"))
        except psycopg2.IntegrityError:
            return "Erro: Email já cadastrado!"

    return render_template("cadastro.html")



if __name__ == "__main__":
    app.run(debug=True)
