import os
from datetime import datetime, timezone
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi import HTTPException
from supabase import Client, create_client


_client: Client | None = None
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def get_supabase() -> Client:
    global _client
    if _client is None:
        url = (os.getenv("SUPABASE_URL") or "").strip()
        key = (os.getenv("SUPABASE_KEY") or "").strip()
        if not url or not key:
            raise RuntimeError(
                "Configure as variaveis de ambiente SUPABASE_URL e SUPABASE_KEY."
            )
        parsed = urlparse(url)
        if parsed.path and parsed.path != "/":
            raise RuntimeError(
                "SUPABASE_URL deve ser apenas a URL base, sem caminho como /rest/v1."
            )
        _client = create_client(url, key)
    return _client


def criar_tabelas():
    # As tabelas ficam descritas em backend/schema.sql.
    # O Supabase nao permite criar schema pela API REST usada pela aplicacao.
    get_supabase()


def verificar_configuracao():
    url = (os.getenv("SUPABASE_URL") or "").strip()
    key = (os.getenv("SUPABASE_KEY") or "").strip()
    parsed = urlparse(url)
    status = {
        "api": "ok",
        "supabase_url_configurada": bool(url),
        "supabase_key_configurada": bool(key),
        "supabase_url_host": parsed.netloc,
        "supabase_url_path": parsed.path,
        "customers_acessivel": False,
    }
    if not url or not key:
        status["erro"] = "Configure SUPABASE_URL e SUPABASE_KEY no Render."
        return status
    try:
        get_supabase().table("customers").select("id").limit(1).execute()
        status["customers_acessivel"] = True
    except Exception as exc:
        status["erro"] = str(exc)
    return status


def _executar_supabase(operacao):
    try:
        return operacao()
    except Exception as exc:
        mensagem = str(exc)
        status = 400 if "duplicate key" in mensagem.lower() else 500
        raise HTTPException(status_code=status, detail=mensagem)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _cookie(row):
    return {
        "id": row["id"],
        "name": row.get("name") or "",
        "nome": row.get("name") or "",
        "flavor": row.get("flavor") or "",
        "price": float(row.get("price") or 0),
        "preco": float(row.get("price") or 0),
        "stock": int(row.get("stock") or 0),
        "quantidade": int(row.get("stock") or 0),
        "ingredients": row.get("ingredients") or [],
        "createdAt": row.get("created_at"),
    }


def _cliente(row):
    return {
        "id": row["id"],
        "name": row.get("name") or "",
        "nome": row.get("name") or "",
        "cpf": row.get("cpf") or "",
        "contact": row.get("contact") or "",
        "telefone": row.get("contact") or "",
        "createdAt": row.get("created_at"),
    }


def _venda(row):
    return {
        "id": row["id"],
        "customerId": row.get("customer_id"),
        "customerName": row.get("customer_name") or "",
        "cliente": row.get("customer_name") or "",
        "customerCpf": row.get("customer_cpf") or "",
        "items": row.get("items") or [],
        "total": float(row.get("total") or 0),
        "valor": float(row.get("total") or 0),
        "paymentMethod": row.get("payment_method") or "",
        "paymentStatus": row.get("payment_status") or "pending",
        "pago": row.get("payment_status") == "paid",
        "payLater": bool(row.get("pay_later")),
        "notes": row.get("notes") or "",
        "createdAt": row.get("created_at"),
        "paidAt": row.get("paid_at"),
    }


def criar_cookie(data):
    payload = {
        "name": (data.get("name") or data.get("nome") or "").strip(),
        "flavor": data.get("flavor", "").strip(),
        "price": float(data.get("price") or data.get("preco") or 0),
        "stock": int(data.get("stock") or data.get("quantidade") or 0),
        "ingredients": data.get("ingredients") or [],
    }
    result = _executar_supabase(
        lambda: get_supabase().table("cookies").insert(payload).execute()
    )
    return _cookie(result.data[0])


def listar_cookies():
    result = _executar_supabase(
        lambda: get_supabase()
        .table("cookies")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )
    return [_cookie(row) for row in result.data]


def obter_cookie(cookie_id):
    result = (
        get_supabase()
        .table("cookies")
        .select("*")
        .eq("id", cookie_id)
        .limit(1)
        .execute()
    )
    return _cookie(result.data[0]) if result.data else None


def atualizar_cookie(cookie_id, data):
    payload = {
        "name": (data.get("name") or data.get("nome") or "").strip(),
        "flavor": data.get("flavor", "").strip(),
        "price": float(data.get("price") or data.get("preco") or 0),
        "stock": int(data.get("stock") or data.get("quantidade") or 0),
        "ingredients": data.get("ingredients") or [],
    }
    result = (
        get_supabase()
        .table("cookies")
        .update(payload)
        .eq("id", cookie_id)
        .execute()
    )
    return _cookie(result.data[0]) if result.data else None


def ajustar_estoque(cookie_id, delta):
    cookie = obter_cookie(cookie_id)
    if not cookie:
        return None
    novo_estoque = max(0, int(cookie["stock"]) + int(delta))
    result = (
        get_supabase()
        .table("cookies")
        .update({"stock": novo_estoque})
        .eq("id", cookie_id)
        .execute()
    )
    return _cookie(result.data[0]) if result.data else None


def remover_cookie(cookie_id):
    get_supabase().table("cookies").delete().eq("id", cookie_id).execute()


def criar_cliente(data):
    cpf = (data.get("cpf") or "").strip() or None
    payload = {
        "name": (data.get("name") or data.get("nome") or "").strip(),
        "cpf": cpf,
        "contact": (data.get("contact") or data.get("telefone") or "").strip(),
    }
    result = _executar_supabase(
        lambda: get_supabase().table("customers").insert(payload).execute()
    )
    return _cliente(result.data[0])


def listar_clientes():
    result = _executar_supabase(
        lambda: get_supabase()
        .table("customers")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )
    return [_cliente(row) for row in result.data]


def obter_cliente(cliente_id):
    result = (
        get_supabase()
        .table("customers")
        .select("*")
        .eq("id", cliente_id)
        .limit(1)
        .execute()
    )
    return _cliente(result.data[0]) if result.data else None


def atualizar_cliente(cliente_id, data):
    cpf = (data.get("cpf") or "").strip() or None
    payload = {
        "name": (data.get("name") or data.get("nome") or "").strip(),
        "cpf": cpf,
        "contact": (data.get("contact") or data.get("telefone") or "").strip(),
    }
    result = (
        get_supabase()
        .table("customers")
        .update(payload)
        .eq("id", cliente_id)
        .execute()
    )
    return _cliente(result.data[0]) if result.data else None


def remover_cliente(cliente_id):
    get_supabase().table("customers").delete().eq("id", cliente_id).execute()


def criar_venda(data):
    items = data.get("items") or []
    total = (
        sum(float(item["unitPrice"]) * int(item["quantity"]) for item in items)
        if items
        else float(data.get("valor") or 0)
    )
    status = data.get("paymentStatus") or data.get("payment_status") or "pending"
    if "pago" in data:
        status = "paid" if data.get("pago") else "pending"
    payload = {
        "customer_id": data.get("customerId"),
        "customer_name": (data.get("customerName") or data.get("cliente") or "").strip(),
        "customer_cpf": (data.get("customerCpf") or "").strip() or None,
        "items": items,
        "total": total,
        "payment_method": data.get("paymentMethod", "pix"),
        "payment_status": status,
        "pay_later": bool(data.get("payLater")),
        "notes": data.get("notes", "").strip(),
        "paid_at": _now() if status == "paid" else None,
    }
    created_at = data.get("createdAt") or data.get("created_at")
    if created_at:
        payload["created_at"] = created_at
    result = _executar_supabase(
        lambda: get_supabase().table("sales").insert(payload).execute()
    )
    for item in items:
        ajustar_estoque(item["cookieId"], -int(item["quantity"]))
    return _venda(result.data[0])


def listar_vendas():
    result = _executar_supabase(
        lambda: get_supabase()
        .table("sales")
        .select("*")
        .order("created_at", desc=False)
        .execute()
    )
    return [_venda(row) for row in result.data]


def obter_venda(venda_id):
    result = (
        get_supabase()
        .table("sales")
        .select("*")
        .eq("id", venda_id)
        .limit(1)
        .execute()
    )
    return _venda(result.data[0]) if result.data else None


def marcar_venda(venda_id, status):
    payload = {
        "payment_status": status,
        "paid_at": _now() if status == "paid" else None,
    }
    result = (
        get_supabase()
        .table("sales")
        .update(payload)
        .eq("id", venda_id)
        .execute()
    )
    return _venda(result.data[0]) if result.data else None


def remover_venda(venda_id):
    venda = obter_venda(venda_id)
    if venda:
        for item in venda["items"]:
            ajustar_estoque(item["cookieId"], int(item["quantity"]))
    get_supabase().table("sales").delete().eq("id", venda_id).execute()
