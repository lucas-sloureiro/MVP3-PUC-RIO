from pydantic import BaseModel
from typing import Optional, List
from model.pinguin import Pinguin
import json
import numpy as np

class PinguinSchema(BaseModel):
    """ Define como um novo Pinguin a ser inserido deve ser representado
    """
    name: str = "Kowalski"
    lenght: float = 45.2
    depth: float = 14.1
    flipper: float = 223.2
    mass: float = 482.3
    
class PinguinViewSchema(BaseModel):
    """Define como um Pinguin será retornado
    """
    id: int = 1
    name: str = "Kowalski"
    lenght: float = 45.2
    depth: float = 14.1
    flipper: float = 223.2
    mass: float = 482.3
    outcome: str = "Adelie"
    
class PinguinBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """
    name: str = "Kowalski"

class ListaPinguinSchema(BaseModel):
    """Define como uma lista de pinguins será representada
    """
    pinguins: List[PinguinSchema]

    
class PinguinDelSchema(BaseModel):
    """Define como um paciente para deleção será representado
    """
    name: str = "Kowalski"
    
# Apresenta apenas os dados de um pinguin    
def apresenta_pinguin(pinguin: Pinguin):
    """ Retorna uma representação do pinguin seguindo o schema definido em
        PinguinViewSchema.
    """
    return {
        "id": pinguin.id,
        "name": pinguin.name,
        "lenght": pinguin.lenght,
        "depth": pinguin.depth,
        "flipper": pinguin.flipper,
        "mass": pinguin.mass,
        "outcome": pinguin.outcome,
    }
    
# Apresenta uma lista de pinguins
def apresenta_pinguins(pinguins: List[Pinguin]):
    """ Retorna uma representação do pinguin seguindo o schema definido em
        PinguinViewSchema.
    """
    result = []
    for pinguin in pinguins:
        result.append({
            "id": pinguin.id,
            "name": pinguin.name,
            "lenght": pinguin.lenght,
            "depth": pinguin.depth,
            "flipper": pinguin.flipper,    
            "mass": pinguin.mass,
            "outcome": pinguin.outcome
        })

    return {"pinguins": result}

