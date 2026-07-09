from fastapi import APIRouter, HTTPException

from backend.database import (
    criar_venda,
    listar_vendas,
    marcar_venda,
    obter_venda,
    registrar_pagamento,
    remover_venda,
)

router = APIRouter()


@router.post("/")
def nova_venda(venda: dict):
    return criar_venda(venda)


@router.get("/")
def get_vendas():
    return listar_vendas()


@router.get("/{venda_id}")
def get_venda(venda_id: str):
    venda = obter_venda(venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda nao encontrada")
    return venda


@router.patch("/{venda_id}/pagar")
def pagar_venda(venda_id: str):
    venda = marcar_venda(venda_id, "paid")
    if not venda:
        raise HTTPException(status_code=404, detail="Venda nao encontrada")
    return venda


@router.patch("/{venda_id}/pagamento")
def pagamento_parcial(venda_id: str, pagamento: dict):
    valor = pagamento.get("valor") or pagamento.get("amount")
    if not valor or float(valor) <= 0:
        raise HTTPException(status_code=400, detail="Informe um valor de pagamento maior que zero")
    venda = registrar_pagamento(venda_id, valor)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda nao encontrada")
    return venda


@router.patch("/{venda_id}/pendente")
def pendente_venda(venda_id: str):
    venda = marcar_venda(venda_id, "pending")
    if not venda:
        raise HTTPException(status_code=404, detail="Venda nao encontrada")
    return venda


@router.delete("/{venda_id}")
def excluir_venda(venda_id: str):
    remover_venda(venda_id)
    return {"status": "ok"}
