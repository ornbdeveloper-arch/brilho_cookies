from fastapi import APIRouter, HTTPException

from backend.database import (
    atualizar_cliente,
    criar_cliente,
    listar_clientes,
    obter_cliente,
    remover_cliente,
)

router = APIRouter()


@router.get("/")
def get_clientes():
    return listar_clientes()


@router.get("/{cliente_id}")
def get_cliente(cliente_id: str):
    cliente = obter_cliente(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return cliente


@router.post("/")
def novo_cliente(cliente: dict):
    return criar_cliente(cliente)


@router.put("/{cliente_id}")
def editar_cliente(cliente_id: str, cliente: dict):
    atualizado = atualizar_cliente(cliente_id, cliente)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Cliente nao encontrado")
    return atualizado


@router.delete("/{cliente_id}")
def excluir_cliente(cliente_id: str):
    remover_cliente(cliente_id)
    return {"status": "ok"}
