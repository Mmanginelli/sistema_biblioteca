# models/biblioteca_model.py
 
from typing import List, Optional
from extensions import db   

class Autor(db.Model):     
    """Lado 1 do relacionamento — um Autor tem vários Livros."""      
    
    __tablename__ = 'autor'      
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome          = db.Column(db.String(120), nullable=False)     
    nacionalidade = db.Column(db.String(80),  nullable=True)      
    
    # db.relationship() cria o atalho autor.livros → lista de Livro     
    livros = db.relationship('Livro', backref='autor', lazy='select')      
    
    def __repr__(self) -> str:         
        return f"<Autor {self.id}: {self.nome}>"   
        
class Livro(db.Model):     
    """Lado N do relacionamento — cada Livro pertence a um Autor."""      
    __tablename__ = 'livro'      
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)     
    titulo   = db.Column(db.String(200), nullable=False)     
    ano      = db.Column(db.Integer,     nullable=True)      

    # ForeignKey: coluna que armazena o id do autor no banco     
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    
    def __repr__(self) -> str:         
        return f"<Livro {self.id}: {self.titulo}>" 

class AutorRepositorio:     
    """Camada de acesso a dados de Autor."""      
    def adicionar(self, autor: Autor) -> Autor:         
        db.session.add(autor)         
        db.session.commit()         
        return autor      
        
    def listar_todos(self) -> List[Autor]:         
        return Autor.query.order_by(Autor.nome).all()      
        
    def buscar_por_id(self, autor_id: int) -> Optional[Autor]:         
        return Autor.query.get(autor_id)      
        
    def remover(self, autor_id: int) -> bool:         
        autor = self.buscar_por_id(autor_id)         
        if autor:             
            db.session.delete(autor)             
            db.session.commit()            
            return True         
        return False      
        
    def contar(self) -> int:         
        return Autor.query.count()

class LivroRepositorio:     
    """Camada de acesso a dados de Livro."""      
    def adicionar(self, livro: Livro) -> Livro:         
        db.session.add(livro)         
        db.session.commit()         
        return livro      
        
    def listar_todos(self) -> List[Livro]:         
        # join() carrega os dados do Autor junto com cada Livro        
        # evita N+1 queries (uma query por livro para buscar o autor)         
        return Livro.query.join(Autor).order_by(Autor.nome, Livro.titulo).all()      
    
    def listar_por_autor(self, autor_id: int) -> List[Livro]:         
        """Retorna todos os livros de um autor específico."""         
        return Livro.query.filter_by(autor_id=autor_id).order_by(Livro.titulo).all()      
        
    def buscar_por_id(self, livro_id: int) -> Optional[Livro]:         
        return Livro.query.get(livro_id)      
    
    def remover(self, livro_id: int) -> bool:         
        livro = self.buscar_por_id(livro_id)         
        if livro:             
            db.session.delete(livro)             
            db.session.commit()             
            return True         
        return False
        