from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Bem-vindo ao sistema de cadastro de usuários!"

# Rota para o formulário de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for("sucesso"))
        except sqlite3.IntegrityError:
            return "Erro: Email já cadastrado!"

    return render_template("cadastro.html")

# Rota de sucesso
@app.route("/sucesso")
def sucesso():
    return "Usuário cadastrado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)

