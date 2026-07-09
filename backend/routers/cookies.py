from fastapi import APIRouter, HTTPException

from backend.database import (
    atualizar_cookie,
    criar_cookie,
    listar_cookies,
    obter_cookie,
    remover_cookie,
)

router = APIRouter()


@router.get("/")
def get_cookies():
    return listar_cookies()


@router.get("/{cookie_id}")
def get_cookie(cookie_id: str):
    cookie = obter_cookie(cookie_id)
    if not cookie:
        raise HTTPException(status_code=404, detail="Cookie nao encontrado")
    return cookie


@router.post("/")
def novo_cookie(cookie: dict):
    return criar_cookie(cookie)


@router.put("/{cookie_id}")
def editar_cookie(cookie_id: str, cookie: dict):
    atualizado = atualizar_cookie(cookie_id, cookie)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Cookie nao encontrado")
    return atualizado


@router.delete("/{cookie_id}")
def excluir_cookie(cookie_id: str):
    remover_cookie(cookie_id)
    return {"status": "ok"}
