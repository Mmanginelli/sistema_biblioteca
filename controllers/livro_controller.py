# controllers/livro_controller.py 
from flask import Blueprint, render_template, request, redirect, url_for, flash 
from models.biblioteca_model import Livro, LivroRepositorio, Autor, AutorRepositorio  

livro_bp    = Blueprint('livros', __name__, url_prefix='/livros') 
repo        = LivroRepositorio() 
autor_repo  = AutorRepositorio()   

@livro_bp.route('/') 
def index():     """Lista todos os livros com o nome do autor (join)."""     
livros = repo.listar_todos()     
return render_template('livros/lista.html', livros=livros)   

@livro_bp.route('/autor/<int:autor_id>') 
def por_autor(autor_id: int):     
    """Lista apenas os livros de um autor específico."""     
    autor  = autor_repo.buscar_por_id(autor_id)     
    if not autor:         
        flash('Autor não encontrado.', 'erro')         
        return redirect(url_for('livros.index'))     
        livros = repo.listar_por_autor(autor_id)     
    return render_template('livros/por_autor.html', autor=autor, livros=livros)   
    
@livro_bp.route('/novo', methods=['GET']) 
def novo_form():
    """Passa a lista de autores para o <select> do formulário."""     
    autores = autor_repo.listar_todos()     
    return render_template('livros/form.html', livro=None, modo='Novo', autores=autores)   
    
@livro_bp.route('/novo', methods=['POST']) 
def novo_salvar():     
    titulo   = request.form.get('titulo', '').strip()     
    ano_str  = request.form.get('ano', '').strip()     
    autor_id = request.form.get('autor_id', '')     
    autores  = autor_repo.listar_todos()      
    
    if not titulo or not autor_id:         
        flash('Título e autor são obrigatórios.', 'erro')         
        return render_template('livros/form.html', livro=None, modo='Novo', autores=autores)     
        try:         
            ano = int(ano_str) if ano_str else None
        except ValueError:         
            flash('Ano inválido.', 'erro')         
            return render_template('livros/form.html', livro=None, modo='Novo', autores=autores)     

        repo.adicionar(Livro(titulo=titulo, ano=ano, autor_id=int(autor_id)))     
        flash(f'"{titulo}" cadastrado com sucesso!', 'sucesso')     
        return redirect(url_for('livros.index'))   

@livro_bp.route('/remover/<int:livro_id>', methods=['POST']) 
def remover(livro_id: int):     
    if repo.remover(livro_id):         
        flash('Livro removido.', 'sucesso')     
    else:         
        flash('Livro não encontrado.', 'erro')     
    return redirect(url_for('livros.index')) 