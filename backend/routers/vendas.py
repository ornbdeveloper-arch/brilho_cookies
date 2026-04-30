from fastapi import APIRouter
from database import criar_venda, listar_vendas

router = APIRouter()


@router.post("/")
def nova_venda(venda: dict):
    criar_venda(
        venda["cliente"],
        venda["valor"],
        venda.get("pago", True)
    )
    return {"status": "ok"}


@router.get("/")
def get_vendas():
    return listar_vendas()