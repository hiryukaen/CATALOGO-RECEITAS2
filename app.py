from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
DATABASE_URL = "postgresql://postgresql_usuario_user:sLsZ0dqBk1d7GAvsXzFTOyLIxnLbF2eN@dpg-cu9c183tq21c73ahm080-a/postgresql_usuario"

def connect_db():
    return psycopg2.connect(DATABASE_URL)

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

init_db()

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
            conn.commit()
            conn.close()
            return redirect(url_for("sucesso"))
        except psycopg2.IntegrityError:
            return "Erro: Email já cadastrado!"

    return render_template("cadastro.html")

@app.route("/sucesso")
def sucesso():
    return "Usuário cadastrado com sucesso!"

if __name__ == "__main__":
    app.run(debug=True)
