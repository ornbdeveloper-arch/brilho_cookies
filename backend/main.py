from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import clientes, cookies, fidelidade, index, vendas
from database import criar_tabelas

app = FastAPI()


criar_tabelas()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(index.router)  
app.include_router(clientes.router, prefix="/clientes")
app.include_router(cookies.router, prefix="/cookies")
app.include_router(fidelidade.router, prefix="/fidelidade")
app.include_router(vendas.router, prefix="/vendas")

@app.get("/")
def root():
    return {"msg": "API Brilho Cookies Rodando 🍪"}