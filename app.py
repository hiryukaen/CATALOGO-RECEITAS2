from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import random

from core.utils.postgresql_crud import PostgreSQLCRUD

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
#DATABASE_URL = "postgresql://postgresql_usuario_user:sLsZ0dqBk1d7GAvsXzFTOyLIxnLbF2eN@dpg-cu9c183tq21c73ahm080-a/postgresql_usuario"

#def connect_db():
#    return psycopg2.connect(DATABASE_URL)

# Inicializar o banco de dados
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

###init_db()

@app.route('/')
def login():
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
    imagem_escolhida = random.choice(imagens)
    return render_template('login.html', imagem_fundo=imagem_escolhida)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/usuario')
def usuario():
    return render_template('usuario.html')


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
            db.create("users", nome = nome, email = email, senha = senha)

            # conn = connect_db()
            # cursor = conn.cursor()
            # cursor.execute("INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            # conn.commit()
            # conn.close()
            return redirect(url_for("sucesso"))
        except psycopg2.IntegrityError:
            return "Erro: Email já cadastrado!"

    return render_template("cadastro.html")

@app.route("/sucesso")
def sucesso():
    return "Usuário cadastrado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)
