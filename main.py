from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/livros'
app.config['SECRET_KEY'] = 'clave_secreta'
db = SQLAlchemy(app)

class Livro(db.Model):
    id_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100))
    autor = db.Column(db.String(254))
    ano_publicacao = db.Column(db.Integer)

@app.route('/')
def index():
    livros = Livro.query.all()
    return render_template('cadastroLivro.html', outro=livros)


@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    livro = Livro.query.filter_by(titulo=titulo).first()
    if livro:
        flash('Livro já existente!')
        return redirect(url_for('novo'))

    novo_livro = Livro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao)
    db.session.add(novo_livro)
    db.session.commit()
    flash('Livro adicionado com sucesso.')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    livro = Livro.query.get(id)
    return render_template('editarLivro.html', titulo='Editando livro', livro=livro)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    livro = Livro.query.get(request.form['id'])
    livro.titulo = request.form['titulo']
    livro.autor = request.form['autor']
    livro.ano_publicacao = request.form['ano_publicacao']

    db.session.commit()
    flash('Livro atualizado com sucesso.')
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    Livro.query.filter_by(id_livro=id).delete()
    db.session.commit()
    flash('Livro excluído com sucesso.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
