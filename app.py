from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Funcionario, Fornecedor, Produto, Categoria, Movimentacao, User
from datetime import datetime
from flask_login import login_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funcionarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'techstock123'

# Inicializar o banco de dados com o app
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

# Página de gerenciamento
@app.route('/gerenciamento')
def gerenciamento():
    return render_template('gerenciamento.html')

# Gerenciar funcionários
@app.route('/gerenciar_funcionarios')
def gerenciar_funcionarios():
    # Buscar todos os funcionários
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/gerenciar_funcionarios.html', funcionarios=funcionarios)


# Criar funcionário
@app.route('/criar_funcionario', methods=['GET', 'POST'])
def criar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        cargo = request.form['cargo']

        # Verifica se o CPF ou o e-mail já existem
        if Funcionario.query.filter_by(cpf_funcionario=cpf).first():
            flash('CPF já existente.', 'error')
            return redirect(url_for('criar_funcionario'))

        if Funcionario.query.filter_by(email_funcionario=email).first():
            flash('E-mail já existente.', 'error')
            return redirect(url_for('criar_funcionario'))

        if Funcionario.query.filter_by(telefone_funcionario=telefone).first():
            return render_template(
                'funcionarios/criar_funcionario.html',
                nome=nome,
                cpf=cpf,
                email=email,
                telefone=telefone,
                telefone_erro='O telefone inserido já está registrado. Use outro número.',
                cargo=cargo
            )

        # Cria um novo funcionário
        novo_funcionario = Funcionario(
            nome_funcionario=nome,
            cpf_funcionario=cpf,
            email_funcionario=email,
            telefone_funcionario=telefone,
            cargo_funcionario=cargo
        )
        db.session.add(novo_funcionario)
        db.session.commit()
        flash('Funcionário criado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    return render_template('funcionarios/criar_funcionario.html')

# Listar funcionários
@app.route('/listar_funcionarios')
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('funcionarios/listar_funcionarios.html', funcionarios=funcionarios)



@app.route('/editar_funcionario/<int:id>', methods=['GET', 'POST'])
def editar_funcionario(id):
    # Buscar o funcionário no banco de dados usando o ID
    funcionario = Funcionario.query.get(id)

    # Caso o funcionário não seja encontrado, exibe uma mensagem de erro e redireciona
    if not funcionario:
        flash('Funcionário não encontrado.', 'error')
        return redirect(url_for('listar_funcionarios'))

    if request.method == 'POST':
        # Atualiza os dados do funcionário com os dados do formulário
        funcionario.nome_funcionario = request.form['nome']
        funcionario.cpf_funcionario = request.form['cpf']
        funcionario.email_funcionario = request.form['email']
        funcionario.telefone_funcionario = request.form['telefone']
        funcionario.cargo_funcionario = request.form['cargo']

        # Salva as alterações no banco de dados
        db.session.commit()

        # Exibe uma mensagem de sucesso e redireciona para a lista de funcionários
        flash('Funcionário atualizado com sucesso!', 'success')
        return redirect(url_for('listar_funcionarios'))

    return render_template('funcionarios/editar_funcionario.html', funcionario=funcionario)

@app.route('/deletar_funcionario/<int:id>', methods=['GET', 'POST'])
def deletar_funcionario(id):
    funcionario = Funcionario.query.get(id)
    if funcionario:
        db.session.delete(funcionario)
        db.session.commit()
    return redirect(url_for('gerenciar_funcionarios'))




# Gerenciar fornecedores
@app.route('/gerenciar_fornecedores')
def gerenciar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores/gerenciar_fornecedores.html', fornecedores=fornecedores)

# Criar fornecedor
@app.route('/criar_fornecedor', methods=['GET', 'POST'])
def criar_fornecedor():
    if request.method == 'POST':
        nome_fornecedor = request.form['nome_fornecedor']
        telefone_fornecedor = request.form['telefone_fornecedor']
        email_fornecedor = request.form['email_fornecedor']

        # Verifica se o telefone já existe
        fornecedor_existente = Fornecedor.query.filter_by(telefone_fornecedor=telefone_fornecedor).first()
        if fornecedor_existente:
            flash('Este telefone já está cadastrado!', 'danger')
            return redirect(url_for('criar_fornecedor'))

        # Caso o telefone não exista, cria o novo fornecedor
        fornecedor = Fornecedor(
            nome_fornecedor=nome_fornecedor,
            telefone_fornecedor=telefone_fornecedor,
            email_fornecedor=email_fornecedor
        )

        db.session.add(fornecedor)
        db.session.commit()
        flash('Fornecedor criado com sucesso!', 'success')
        return redirect(url_for('listar_fornecedores'))

    return render_template('fornecedores/criar_fornecedor.html')

# Listar fornecedores
@app.route('/listar_fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('fornecedores/listar_fornecedores.html', fornecedores=fornecedores)

# Editar fornecedor
@app.route('/editar_fornecedor/<int:id>', methods=['GET', 'POST'])
def editar_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)

    if not fornecedor:
        flash('Fornecedor não encontrado.', 'error')
        return redirect(url_for('listar_fornecedores'))

    if request.method == 'POST':
        fornecedor.nome_fornecedor = request.form['nome']
        fornecedor.telefone_fornecedor = request.form['telefone']
        fornecedor.email_fornecedor = request.form['email']

        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('listar_fornecedores'))

    return render_template('fornecedores/editar_fornecedor.html', fornecedor=fornecedor)

# Deletar fornecedor
@app.route('/deletar_fornecedor/<int:id>', methods=['GET', 'POST'])
def deletar_fornecedor(id):
    fornecedor = Fornecedor.query.get(id)
    if fornecedor:
        db.session.delete(fornecedor)
        db.session.commit()
        flash('Fornecedor deletado com sucesso!', 'success')

    return redirect(url_for('gerenciar_fornecedores'))




# Gerenciar produtos
@app.route('/gerenciar_produtos')
def gerenciar_produtos():
    produtos = Produto.query.all()
    return render_template('produtos/gerenciar_produtos.html', produtos=produtos)

@app.route('/criar_produto', methods=['GET', 'POST'])
def criar_produto():
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        validade_str = request.form['validade']
        validade = datetime.strptime(validade_str, '%Y-%m-%d').date()  # Converter para objeto date
        id_fornecedor = request.form.get('id_fornecedor')
        id_categoria = request.form.get('id_categoria')

        # Criação do produto no banco de dados
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade=quantidade,
            validade=validade,  # Usando objeto date
            id_fornecedor=id_fornecedor,
            id_categoria=id_categoria
        )
        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('listar_produtos'))

    # Envia fornecedores para o template
    fornecedores = Fornecedor.query.all()
    return render_template('produtos/criar_produto.html', fornecedores=fornecedores)
# Listar produtos
@app.route('/listar_produtos')
def listar_produtos():
    produtos = Produto.query.all()  # Recupera todos os produtos do banco de dados
    return render_template('produtos/listar_produtos.html', produtos=produtos)

# Editar produto
@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)  # Obtém o produto a ser editado

    if request.method == 'POST':
        # Captura os dados do formulário de edição
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.preco = float(request.form['preco'])  # Certifique-se de que o preço seja convertido para float
        produto.quantidade = int(request.form['quantidade'])
        validade_str = request.form['validade']
        produto.validade = datetime.strptime(validade_str, '%Y-%m-%d').date()  # Converter para objeto date
        produto.id_categoria = request.form['id_categoria']  # Apenas a categoria permanece

        try:
            db.session.commit()  # Atualiza o banco de dados
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('listar_produtos'))  # Redireciona para a lista de produtos
        except Exception as e:
            db.session.rollback()  # Rollback em caso de erro
            flash('Erro ao atualizar o produto. Tente novamente.', 'danger')

    return render_template('produtos/editar_produto.html', produto=produto)


# Deletar produto
@app.route('/deletar_produto/<int:id>', methods=['GET', 'POST'])
def deletar_produto(id):
    produto = Produto.query.get(id)
    if produto:
        db.session.delete(produto)
        db.session.commit()
        flash('Produto deletado com sucesso!', 'success')

    return redirect(url_for('gerenciar_produtos'))




@app.route('/movimentacao', methods=['GET', 'POST'])
def movimentacao_produto():
    produtos = Produto.query.all()
    funcionarios = Funcionario.query.all()
    if request.method == 'POST':
        # Captura os dados do formulário
        tipo = request.form['tipo']
        quantidade = int(request.form['quantidade'])
        id_produto = int(request.form['id_produto'])
        id_funcionario = int(request.form['id_funcionario'])
        data_movimentacao = datetime.strptime(request.form['data'], '%Y-%m-%d')

        # Busca o produto e valida a movimentação
        produto = Produto.query.get_or_404(id_produto)
        if tipo == 'saida' and produto.quantidade < quantidade:
            flash('Estoque insuficiente para a saída', 'danger')
            return redirect(url_for('movimentacao_produto'))

        # Atualiza o estoque e registra a movimentação
        try:
            movimentacao = Movimentacao(
                tipo=tipo,
                quantidade=quantidade,
                id_produto=id_produto,
                data=data_movimentacao
            )
            produto.quantidade += quantidade if tipo == 'entrada' else -quantidade
            db.session.add(movimentacao)
            db.session.commit()
            flash('Movimentação registrada com sucesso!', 'success')
            return redirect(url_for('movimentacao_produto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao registrar movimentação: {str(e)}', 'danger')

    return render_template('movimentacao/movimentacao.html', produtos=produtos, funcionarios=funcionarios)


@app.route('/grafico_movimentacoes')
def grafico_movimentacoes():
    # Consulta para obter movimentações agrupadas por produto
    movimentacoes = db.session.query(
        Produto.nome.label('produto'),
        Movimentacao.tipo,
        db.func.sum(Movimentacao.quantidade).label('total'),
        Funcionario.nome_funcionario.label('funcionario'),
        Fornecedor.nome_fornecedor.label('fornecedor')
    ).join(Produto, Movimentacao.id_produto == Produto.id) \
     .join(Funcionario, Movimentacao.id_produto == Produto.id) \
     .join(Fornecedor, Produto.id_fornecedor == Fornecedor.id) \
     .group_by(Produto.nome, Movimentacao.tipo, Funcionario.nome_funcionario, Fornecedor.nome_fornecedor) \
     .all()

    # Preparar os dados para o gráfico
    data = {}
    for mov in movimentacoes:
        produto = mov.produto
        if produto not in data:
            data[produto] = {
                'entrada': 0,
                'saida': 0,
                'funcionario': mov.funcionario,
                'fornecedor': mov.fornecedor
            }
        data[produto][mov.tipo] = mov.total

    return render_template('movimentacao/grafico_movimentacoes.html', data=data)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Verifica se o nome de usuário já existe
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe. Escolha outro.', 'danger')
        elif password != confirm_password:  # Verifica se as senhas não coincidem
            flash('As senhas não coincidem. Tente novamente.', 'danger')
        else:
            # Cria o usuário e usa o método set_password para definir a senha
            user = User(username=username)
            user.set_password(password)  # Configura a senha usando o método set_password
            db.session.add(user)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))

    return render_template('usuario/cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário existe e se a senha está correta
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)  # Faz o login do usuário
            flash('Login realizado com sucesso!', 'success')  # Mensagem de sucesso
            return redirect(url_for('dashboard'))  # Redireciona para o dashboard
        else:
            flash('Usuário ou senha inválidos. Tente novamente.', 'danger')  # Mensagem de erro

    return render_template('usuario/login.html')




@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))






if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
