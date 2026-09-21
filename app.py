# app.py 
import os 
from dotenv import load_dotenv 
from flask import Flask, render_template 
from extensions import db 
from controllers.autor_controller import autor_bp 
from controllers.livro_controller import livro_bp  

load_dotenv()   

def create_app() -> Flask:     
    app = Flask(__name__)     
    app.secret_key = os.environ.get('SECRET_KEY')     
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')     
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False     

    db.init_app(app)     
    app.register_blueprint(autor_bp)     
    app.register_blueprint(livro_bp)    

    from models.biblioteca_model import AutorRepositorio, LivroRepositorio     
    autor_repo = AutorRepositorio()     
    livro_repo = LivroRepositorio()  

    @app.route('/')     
    def home():         
        """Dashboard inicial com contadores e atalhos de navegação.""" 
        return render_template(             
            'home.html',             
            total_autores=autor_repo.contar(),             
            total_livros=livro_repo.contar(),             
            autores=autor_repo.listar_todos(),         
        )      
        
    with app.app_context():         
        db.create_all()      
    
    return app   
        
if __name__ == "__main__":     
    app = create_app()     
    app.run(debug=True) 