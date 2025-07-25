from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
from functools import wraps

# Importação do core Usuario e UsuarioService
from core.usuario.usuario import Usuario
from core.usuario.usuario_service import UsuarioService

# Importação do core Login e LoginService
from core.login.login import Login
from core.login.login_service import LoginService

# Importação do core Categoria e CategoriaService
from core.categoria.categoria import Categoria
from core.categoria.categoria_service import CategoriaService

# Importação do core Contato e ContatoService
from core.contato.contato import Contato
from core.contato.contato_service import ContatoService

# Importação do core Receita e ReceitaService
from core.receita.receita import Receita
from core.receita.receita_service import ReceitaService

app = Flask(__name__)
app.secret_key = '1234567890abcdef'

# Decorator para validar a atuenticação do usuário
# Vc pode utilizar nas rotas que são obrigatórias de autenticação do usuário
def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash("Você precisa estar logado para acessar esta página.", "error")
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    return decorated_function

# lista de imagens 
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

# Rota da página login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        imagem_escolhida = random.choice(imagens)
        return render_template('login.html', imagem_fundo=imagem_escolhida)
    
    elif request.method == 'POST':
        # Injeção de Dependências
        service = LoginService()
        # pegar os dados do formulário
        email = request.form['email'] 
        senha = request.form['senha']
        # criar o objeto
        obj_login = Login(email, senha)

        try:
            service.autenticar(obj_login)
            session['usuario'] = email
            return redirect(url_for('home'))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for('login'))


# Rota da página home
@app.route('/home')
@login_requerido
def home():
    return render_template('home.html')



# Rota para sair do sistema, retorna para página login
@app.route('/sair')
def sair():
    session.pop('usuario', None)
    return redirect(url_for('login'))



# Rota para página usuario
@app.route('/usuario', methods=['GET', 'POST'])
@login_requerido
def usuario():
    if request.method == 'GET':
        return render_template('usuario.html')
    
    elif request.method == 'POST':
        # Injeção de Dependências
        service = UsuarioService()

        # Pegar os dados do formulário web
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        conf_senha = request.form['conf-senha']
        situacao = request.form['situacao']
        
        if senha == conf_senha:
            # Cadastrar o usuario
            try:
                service.cadastrar_usuario(nome, email, senha, situacao)
                flash("Usuário cadastrado com sucesso!", "success")
                return render_template('usuario.html')
            except ValueError as e:
                flash(str(e), "error")
                return render_template('usuario.html')
        else:
            # senha nao confere
            flash("Senha não confere!", "error")
            return render_template('usuario.html')



@app.route('/listusuario', methods=['GET'])
@login_requerido
def listusuario():
    # Injeção de Dependências
    service = UsuarioService()
    try:
        usuarios = service.listar_usuarios()
    except Exception as e:
        flash(f"Erro ao carregar usuários: {str(e)}", "error")
        usuarios = []
    return render_template('list_usuario.html', usuarios=usuarios)



@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar_usuario(id):
    # Injeção de Dependências
    service = UsuarioService()
    try:
        usuario = service.obter_usuario_por_id(id)
    except ValueError:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('listusuario'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        conf_senha = request.form.get('conf-senha')
        situacao = request.form.get('situacao')

        # Validação básica
        if not nome or not email:
            flash("Nome e email são obrigatórios.", "error")
            return render_template('usuario.html', usuario=usuario)

        if senha != conf_senha:
            flash("Senhas não conferem.", "error")
            return render_template('usuario.html', usuario=usuario)

        try:
            service.cadastrar_usuario(nome, email, senha, situacao)
            flash("Usuário atualizado com sucesso!", "success")
            return redirect(url_for('listusuario'))
        except Exception as e:
            flash(str(e), "error")
            return render_template('usuario.html', usuario=usuario)

    # GET: exibe o formulário com dados atuais do usuário
    return render_template('usuario.html', usuario=usuario)


@app.route('/excluir_usuario/<int:id>')
@login_requerido
def excluir_usuario(id):
    # Injeção de Dependências
    service = UsuarioService()
    try:
        service.excluir_usuario_por_id(id)
        flash("Usuário excluído com sucesso!", "success")
        return redirect(url_for('listusuario'))
    except ValueError:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for('listusuario'))



# Rota para a página de contato
@app.route('/contato', methods=['GET', 'POST'])
@login_requerido
def contato():
    service = ContatoService()

    if request.method == "POST":
        contato = Contato(
            id = 1,
            facebook = request.form.get("facebook"),
            rede_x = request.form.get("rede_x"),
            instagram = request.form.get("instagram"),
            linkedin = request.form.get("linkedin"),
            github = request.form.get("github")
        )
        service.atualizar_ou_inserir(contato)
        flash("Contatos atualizados com sucesso!", "success")
        return redirect(url_for("contato"))

    try:
        contato = service.obter_contato()
    except ValueError:
        contato = Contato(
            id = 1,
            facebook = "",
            rede_x = "",
            instagram = "",
            linkedin = "",
            github = ""
        )

    return render_template('contato.html', contato=contato)


# Rota para a página receita
@app.route('/receita', methods=['GET', 'POST'])
@login_requerido
def receita():

    receita_service = ReceitaService()
    categoria_service = CategoriaService()

    categorias = categoria_service.listar_categorias()

    if request.method == "POST":
        nome = request.form.get("nome-receita", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        modo_preparo = request.form.get("modo_preparo", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if not nome or not ingredientes or not modo_preparo or not categoria:
            flash("Todos os campos são obrigatórios", "error")
        else:
            receita = Receita(0, nome, ingredientes, modo_preparo, categoria)
            receita_service.cadastrar_ou_atualizar(receita)
            flash("Receita cadastrada com sucesso!", "success")

    return render_template('receita.html', categorias = categorias)


# Rota para a página listreceita
@app.route('/listreceita', methods=['GET', 'POST'])
@login_requerido
def listreceita():

    service = ReceitaService()
    try:
        receitas = service.listar_receitas()
    except:
        receitas = []

    return render_template('list_receita.html', receitas = receitas)

#Rota para editar receita
@app.route('/editar_receita/<int:id>', methods=['GET', 'POST'])
@login_requerido
def editar_receita(id):
    receita_service = ReceitaService()
    categoria_service = CategoriaService()

    try:
        receita = receita_service.obter_receita_por_id(id)
        categorias = categoria_service.listar_categorias()
    except:
        flash("Receita não encontrada", "error")
        return redirect(url_for("listreceita"))

    if request.method == "POST":
        nome = request.form.get("nome-receita", "").strip()
        ingredientes = request.form.get("ingredientes", "").strip()
        modo_preparo = request.form.get("modo_preparo", "").strip()
        categoria = request.form.get("categoria", "").strip()

        if not nome or not ingredientes or not modo_preparo or not categoria:
            flash("Todos os campos são obrigatórios", "error")
        else:
            receita = Receita(id, nome, ingredientes, modo_preparo, categoria)
            receita_service.cadastrar_ou_atualizar(receita)
            flash("Receita atualizada com sucesso!", "success")
            return redirect(url_for("listreceita"))


    return render_template("receita.html", receita=receita, categorias=categorias)

@app.route("/excluir_receita/<int:id>")
@login_requerido
def excluir_receita(id):
    service = ReceitaService()
    try:
        service.excluir_receita(id)
        flash("Receita excluida com sucesso!", "success")
    except:
        flash("Receita não excluida/encontrada", "error")
    return redirect(url_for("listreceita"))



# Rota para a página categoria
@app.route('/categoria', methods=['GET', 'POST'])
@login_requerido
def categoria():

    service = CategoriaService()

    if request.method == "GET":
        return render_template('categoria.html')
    elif request.method == "POST":
        try:
            nome_categoria = request.form["categoria-receita"]
            service.cadastrar_categoria(nome_categoria)
            flash("Categoria cadastrada com sucesso!", "success")
        except ValueError as e:
            flash(str(e), "error")
        return render_template('categoria.html')


# Rota para a página listcategoria
@app.route('/listcategoria', methods=['GET', 'POST'])
@login_requerido
def listcategoria():
    service = CategoriaService()
    try:
        categorias = service.listar_categorias()
    except Exception as e:
        flash(str(e),"error")
        categorias = []

    return render_template('list_categoria.html',categorias=categorias)


# Rota para editar categoria
@app.route('/editar_categoria/<nome_categoria>', methods=['GET', 'POST'])
@login_requerido
def editar_categoria(nome_categoria):

    service =  CategoriaService()
    try:
        categoria = service.buscar_por_nome(nome_categoria)
    except ValueError:
        flash("Categoria não encontrada", "error")
        return redirect(url_for("listcategoria"))

    if request.method == "POST":
        nova_categoria = request.form["categoria-receita"]
        try:
            service.atualizar_categoria(nome_categoria, nova_categoria)
            flash("Categoria atualizada com sucesso!", "success")
            return redirect(url_for("listcategoria"))
        except Exception as e:
            flash(str(e), "error")

    return render_template('categoria.html', categoria = categoria)


# Rota para excluir categoria
@app.route('/excluir_categoria/<nome_categoria>')
@login_requerido
def excluir_categoria(nome_categoria):
    service = CategoriaService()
    try:
        service.excluir_categoria(nome_categoria)
        flash("Categoria excluída com sucesso!", "success")
    except ValueError:
        flash("Categoria não excluída", "error")
    return redirect(url_for('listcategoria'))

@app.context_processor
def inject_social_links():
    social_links = {}

    service = ContatoService()
    contato = service.obter_contato()
    if contato:
        social_links = {
            "facebook" : contato.facebook or "",
            "rede_x" : contato.rede_x or "",
            "instagram" : contato.instagram or "",
            "linkedin" : contato.linkedin or "",
            "github" : contato.github or ""
        }
    
    return {"social_links": social_links}

if __name__ == "__main__":
    app.run(debug=True)
