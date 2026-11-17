"""Sistema de cadastro: controller Flask, model SQLite, views Jinja."""
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get('SECRET_KEY', 'trocar-para-producao'), DATABASE=os.path.join(app.instance_path, 'cadastros.db'))
    if test_config:
        app.config.update(test_config)
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

    def connection():
        db = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
        return db

    with connection() as db:
        db.execute('CREATE TABLE IF NOT EXISTS pessoas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE, telefone TEXT)')
        db.commit()

    def validar(form):
        nome = form.get('nome', '').strip()
        email = form.get('email', '').strip().lower()
        telefone = form.get('telefone', '').strip()
        if len(nome) < 2 or len(nome) > 100:
            return None, 'Informe um nome de 2 a 100 caracteres.'
        if len(email) > 150 or '@' not in email or '.' not in email.split('@')[-1] or email.count('@') != 1:
            return None, 'Informe um e-mail válido.'
        if len(telefone) > 25:
            return None, 'Telefone muito longo.'
        return (nome, email, telefone), None

    @app.get('/')
    def index():
        with connection() as db:
            pessoas = db.execute('SELECT * FROM pessoas ORDER BY id DESC').fetchall()
        return render_template('index.html', pessoas=pessoas)

    @app.post('/criar')
    def criar():
        dados, erro = validar(request.form)
        if erro:
            flash(erro, 'erro')
        else:
            try:
                with connection() as db:
                    db.execute('INSERT INTO pessoas (nome,email,telefone) VALUES (?,?,?)', dados)
                    db.commit()
                flash('Cadastro realizado.', 'sucesso')
            except sqlite3.IntegrityError:
                flash('Este e-mail já está cadastrado.', 'erro')
        return redirect(url_for('index'))

    @app.route('/editar/<int:pessoa_id>', methods=['GET', 'POST'])
    def editar(pessoa_id):
        with connection() as db:
            pessoa = db.execute('SELECT * FROM pessoas WHERE id=?', (pessoa_id,)).fetchone()
        if pessoa is None:
            return 'Registro não encontrado', 404
        if request.method == 'POST':
            dados, erro = validar(request.form)
            if erro:
                flash(erro, 'erro')
            else:
                try:
                    with connection() as db:
                        db.execute('UPDATE pessoas SET nome=?, email=?, telefone=? WHERE id=?', (*dados, pessoa_id))
                        db.commit()
                    flash('Cadastro atualizado.', 'sucesso')
                    return redirect(url_for('index'))
                except sqlite3.IntegrityError:
                    flash('Este e-mail já está cadastrado.', 'erro')
        return render_template('editar.html', pessoa=pessoa)

    @app.post('/excluir/<int:pessoa_id>')
    def excluir(pessoa_id):
        with connection() as db:
            result = db.execute('DELETE FROM pessoas WHERE id=?', (pessoa_id,))
            db.commit()
        flash('Registro excluído.' if result.rowcount else 'Registro não encontrado.', 'sucesso' if result.rowcount else 'erro')
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run(debug=False)
