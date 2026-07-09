from fastapi import APIRouter

from database import listar_vendas

router = APIRouter()


def tier_of(total):
    if total >= 300:
        return {"name": "Ouro", "emoji": "🥇", "badge": "gold"}
    if total >= 100:
        return {"name": "Prata", "emoji": "🥈", "badge": "silver"}
    return {"name": "Bronze", "emoji": "🥉", "badge": "bronze"}


@router.get("/")
def ranking_fidelidade():
    grupos = {}
    for venda in listar_vendas():
        cpf = venda["customerCpf"]
        if cpf not in grupos:
            grupos[cpf] = {
                "cpf": cpf,
                "name": venda["customerName"],
                "salesCount": 0,
                "totalSpent": 0,
                "lastPurchase": None,
            }
        grupo = grupos[cpf]
        grupo["salesCount"] += 1
        grupo["totalSpent"] += venda["total"]
        if not grupo["lastPurchase"] or venda["createdAt"] > grupo["lastPurchase"]:
            grupo["lastPurchase"] = venda["createdAt"]

    ranking = [
        {**grupo, "tier": tier_of(grupo["totalSpent"])}
        for grupo in grupos.values()
    ]
    return sorted(ranking, key=lambda item: item["totalSpent"], reverse=True)
