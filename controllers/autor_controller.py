# controllers/autor_controller.py 
from flask import Blueprint, render_template, request, redirect, url_for, flash 
from models.biblioteca_model import Autor, AutorRepositorio  

autor_bp = Blueprint('autores', __name__, url_prefix='/autores') 
repo     = AutorRepositorio()   

@autor_bp.route('/') 
def index():     
    autores = repo.listar_todos()     
    return render_template('autores/lista.html', autores=autores)   
    
@autor_bp.route('/novo', methods=['GET']) 
def novo_form():     
    return render_template('autores/form.html', autor=None, modo='Novo') 

@autor_bp.route('/novo', methods=['POST']) 
def novo_salvar():     
    nome          = request.form.get('nome', '').strip()     
    nacionalidade = request.form.get('nacionalidade', '').strip()     
    if not nome:         
        flash('O nome é obrigatório.', 'erro')         
        return render_template('autores/form.html', autor=None, modo='Novo')     
    repo.adicionar(Autor(nome=nome, nacionalidade=nacionalidade))     
    flash(f'Autor "{nome}" cadastrado!', 'sucesso')     
    return redirect(url_for('autores.index'))   
    
    @autor_bp.route('/remover/<int:autor_id>', methods=['POST']) 
    def remover(autor_id: int):     
        if repo.remover(autor_id):         
            flash('Autor removido.', 'sucesso')     
        else:         
            flash('Autor não encontrado.', 'erro')     
        return redirect(url_for('autores.index')) 