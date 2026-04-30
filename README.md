# 🍪 Brilho Cookies

Aplicação local para gestão de venda de cookies, sem frameworks ou build.

## Como rodar

Abra o arquivo `index.html` diretamente no navegador (duplo clique) ou sirva
a pasta com qualquer servidor estático:

```bash
# opção 1 — Python
python3 -m http.server 8080

# opção 2 — Node
npx serve .
```

Acesse `http://localhost:8080`.

## Estrutura

```
raffa/
├── index.html       # Dashboard
├── cookies.html     # Cadastro e estoque de cookies
├── clientes.html    # Cadastro de clientes (CPF, contato)
├── vendas.html      # Registrar vendas, marcar pagamentos
├── fidelidade.html  # Ranking de CPFs por total gasto
├── css/styles.css   # Design system (tons pastéis + marrom)
└── js/
    ├── storage.js   # Camada de persistência (localStorage)
    ├── ui.js        # Helpers: modal, toast, máscara CPF, formatos
    └── layout.js    # Sidebar compartilhada
```

## Funcionalidades

- ✅ Cadastro de cookies com ingredientes, preço e estoque
- ✅ Cadastro de clientes (CPF único, nome, contato)
- ✅ Registro de vendas — toda venda nasce **pendente**
- ✅ Baixa automática de estoque ao registrar venda
- ✅ Métodos de pagamento: Pix, Dinheiro, Cartão, Fiado
- ✅ Marcar venda como paga quando o dinheiro cair
- ✅ Filtros por status, método, cliente, CPF
- ✅ Ranking de fidelidade por CPF (Bronze / Prata / Ouro)
- ✅ Dashboard com receita paga, valor a receber e estoque baixo

Todos os dados ficam no `localStorage` do navegador — 100% local, sem servidor.
