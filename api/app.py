from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Pinguin, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Penguin Classifier", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Documentação: Swagger")
pinguin_tag = Tag(name="Pinguin", description="Adição, visualização, remoção e predição de pinguins")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação
    """
    return redirect('/openapi')


# Rota de listagem de pacientes
@app.get('/pinguins', tags=[pinguin_tag],
         responses={"200": PinguinViewSchema, "404": ErrorSchema})
def get_pinguins():
    """Lista todos os pinguins cadastrados na base
    Retorna uma lista de pinguins cadastrados na base.
    """
    session = Session()
    
    # Buscando todos os pacientes
    pinguins = session.query(Pinguin).all()
    
    if not pinguins:
        logger.warning("Não existem pinguins cadastrados na base :/")
        return {"message": "Não existem pinguins cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d pinguins econtrados" % len(pinguins))
        return apresenta_pinguins(pinguins), 200


# Rota de adição de paciente
@app.post('/pinguin', tags=[pinguin_tag],
          responses={"200": PinguinViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: PinguinSchema):
    """Adiciona um novo pinguin à base de dados
    Retorna uma representação dos pinguins e características associadas.

    """
    
    # Carregando modelo
    ml_path = 'ml_model/classificador.pkl'
    modelo = Model.carrega_modelo(ml_path)
    
    pinguin = Pinguin(
        name=form.name.strip(),
        lenght=form.lenght,
        depth=form.depth,
        flipper=form.flipper,
        mass=form.mass,
        outcome=Model.preditor(modelo, form)
    )
    logger.debug(f"Adicionando pinguin com o nome: '{pinguin.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se paciente já existe na base
        if session.query(Pinguin).filter(Pinguin.name == form.name).first():
            error_msg = "Pinguin com id já cadastrado :/"
            logger.warning(f"Erro ao adicionar pinguin '{pinguin.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando paciente
        session.add(pinguin)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado pinguin com nome: '{pinguin.name}'")
        return apresenta_pinguin(pinguin), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pinguin '{pinguin.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get('/pinguin', tags=[pinguin_tag],
         responses={"200": PinguinViewSchema, "404": ErrorSchema})
def get_pinguin(query: PinguinBuscaSchema):    
    """Faz a busca por um pinguin cadastrado na base a partir do id

    """
    
    pinguin_nome = query.name
    logger.debug(f"Coletando dados sobre espécie #{pinguin_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pinguin = session.query(Pinguin).filter(Pinguin.name == pinguin_nome).first()
    
    if not pinguin:
        # se o pinguin não foi encontrado
        error_msg = f"Pinguin {pinguin_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar espécie '{pinguin_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pinguin econtrado: '{pinguin.name}'")
        # retorna a representação do pinguin
        return apresenta_pinguin(pinguin), 200
   
    
# Rota de remoção de pinguin por id
@app.delete('/pinguin', tags=[pinguin_tag],
            responses={"200": PinguinViewSchema, "404": ErrorSchema})
def delete_pinguin(query: PinguinBuscaSchema):
    """Remove um pinguin cadastrado na base a partir do id
    """
    
    pinguin_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre pinguin #{pinguin_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando paciente
    pinguin = session.query(Pinguin).filter(Pinguin.name == pinguin_nome).first()
    
    if not pinguin:
        error_msg = "Pinguin não encontrado na base :/"
        logger.warning(f"Erro ao deletar pinguin '{pinguin_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(pinguin)
        session.commit()
        logger.debug(f"Deletado pinguin #{pinguin_nome}")
        return {"message": f"Pinguin {pinguin_nome} removido com sucesso!"}, 200