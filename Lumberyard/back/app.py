from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Madeira
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Lumberyard", version="1.0.1")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
madeira_tag = Tag(name="Madeira", description="Adição, visualização, edição e remoção de madeiras à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')


@app.post('/madeira', tags=[madeira_tag],
          responses={"200": MadeiraViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_madeira(form: MadeiraSchema):
    """Adiciona uma nova madeira à base de dados

    Retorna uma representação das madeiras e informações associadas.
    """
    madeira = Madeira(
        madeira=form.madeira,
        volume=form.volume,
        produto=form.produto,
        origem=form.origem)
    logger.debug(f"Adicionando madeira de nome: '{madeira.nome}'")
    try:
        # Criando conexão com a base
        session = Session()
        # Adicionando madeira
        session.add(madeira)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado madeira de nome: '{madeira.nome}'")
        return apresenta_madeira(madeira), 200

    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Madeira de mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar madeira '{madeira.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar madeira '{madeira.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/madeiras', tags=[madeira_tag],
         responses={"200": ListagemMadeirasSchema, "404": ErrorSchema})
def get_madeiras():
    """Faz a busca por todos os Madeiras cadastradas
    Retorna uma representação da listagem de madeiras.
    """
    logger.debug(f"Coletando madeiras")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    madeiras = session.query(Madeira).all()

    if not madeiras:
        # Se não há madeiras cadastradas
        return {"madeiras": []}, 200
    else:
        logger.debug(f"%d madeiras encontradas" % len(madeiras))
        # Retorna a representação de madeira
        return apresenta_madeiras(madeiras), 200


@app.get('/madeira', tags=[madeira_tag],
         responses={"200": MadeiraViewSchema, "404": ErrorSchema})
def get_madeira(query: MadeiraBuscaSchema):
    """Faz a busca por uma Madeira a partir do nome da madeira

    Retorna uma representação das madeiras e as informações
    """
    madeira_nome = unquote(unquote(query.nome))
    logger.debug(f"Coletando dados sobre a madeira '{madeira_nome}'")
    # Criando conexão com a base
    session = Session()
    # Fazendo a busca
    madeira = session.query(Madeira).filter(Madeira.nome == madeira_nome).first()

    if not madeira:
        # Se a madeira não foi encontrada
        error_msg = "Madeira não encontrada na base :/"
        logger.warning(f"Erro ao buscar a madeira '{madeira_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Madeira encontrada: '{madeira.nome}'")
        # Retorna a representação da madeira
        return apresenta_madeira(madeira), 200


@app.delete('/madeira', tags=[madeira_tag],
            responses={"200": MadeiraDelSchema, "404": ErrorSchema})
def del_madeira(query: MadeiraBuscaSchema):
    """Deleta uma madeira a partir de uma madeira informada

    Retorna uma mensagem de confirmação da remoção.
    """
    madeira_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre a madeira '{madeira_nome}'")
    # Criando conexão com a base
    session = Session()
    # Fazendo a remoção
    count = session.query(Madeira).filter(Madeira.nome == madeira_nome).delete()
    session.commit()

    if count:
        # Retorna a representação da mensagem de confirmação
        logger.debug(f"Madeira deletada da base '{madeira_nome}'")
        return {"message": "Madeira removida com sucesso", "nome": madeira_nome}, 200
    else:
        # Se a madeira não for encontrada
        error_msg = "Madeira não encontrada na base :/"
        logger.warning(f"Erro ao deletar a madeira '{madeira_nome}', {error_msg}")
        return {"message": error_msg}, 404
