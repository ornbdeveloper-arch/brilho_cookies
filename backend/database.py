import sqlite3

# 🔗 Conexão única
conn = sqlite3.connect("banco.db", check_same_thread=False)
cursor = conn.cursor()


# 🚀 Criar tabelas
def criar_tabelas():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cookies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        quantidade INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        valor REAL,
        pago BOOLEAN
    )
    """)

    conn.commit()


# =========================
# 👤 CLIENTES
# =========================

def criar_cliente(nome, telefone):
    cursor.execute(
        "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
        (nome, telefone)
    )
    conn.commit()


def listar_clientes():
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()

    return [
        {"id": c[0], "nome": c[1], "telefone": c[2]}
        for c in dados
    ]


# =========================
# 🍪 COOKIES
# =========================

def criar_cookie(nome, preco, quantidade):
    cursor.execute(
        "INSERT INTO cookies (nome, preco, quantidade) VALUES (?, ?, ?)",
        (nome, preco, quantidade)
    )
    conn.commit()


def listar_cookies():
    cursor.execute("SELECT * FROM cookies")
    dados = cursor.fetchall()

    return [
        {"id": c[0], "nome": c[1], "preco": c[2], "quantidade": c[3]}
        for c in dados
    ]


# =========================
# 💰 VENDAS
# =========================

def criar_venda(cliente, valor, pago=True):
    cursor.execute(
        "INSERT INTO vendas (cliente, valor, pago) VALUES (?, ?, ?)",
        (cliente, valor, pago)
    )
    conn.commit()


def listar_vendas():
    cursor.execute("SELECT * FROM vendas")
    dados = cursor.fetchall()

    return [
        {"id": v[0], "cliente": v[1], "valor": v[2], "pago": bool(v[3])}
        for v in dados
    ]