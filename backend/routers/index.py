from fastapi import APIRouter
from database import listar_vendas, listar_clientes, listar_cookies

router = APIRouter()

@router.get("/")
def dashboard():
    vendas = listar_vendas()
    clientes = listar_clientes()
    cookies = listar_cookies()

    receita_total = sum(v["valor"] for v in vendas) if vendas else 0
    a_receber = sum(v["valor"] for v in vendas if not v.get("pago", True)) if vendas else 0

    return {
        "tipos_cookie": len(cookies),
        "clientes": len(clientes),
        "receita_total": receita_total,
        "a_receber": a_receber,
        "total_vendas": len(vendas),
        "ultimas_vendas": vendas[-5:],
        "estoque_baixo": [c for c in cookies if c["quantidade"] < 10]
    }