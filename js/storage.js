/* 🍪 CookieJar — Camada de persistência em localStorage
   Mantém cookies, clientes e vendas. Tudo síncrono e local. */

const KEYS = {
  cookies: "cookiejar:cookies",
  customers: "cookiejar:customers",
  sales: "cookiejar:sales",
};

/* ───── Helpers ───── */
function read(key) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error("Erro lendo", key, e);
    return [];
  }
}
function write(key, data) {
  localStorage.setItem(key, JSON.stringify(data));
}
function uid() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

/* ───── Cookies ───── */
const cookieStore = {
  list: () => read(KEYS.cookies),
  get: (id) => read(KEYS.cookies).find((c) => c.id === id),
  create: (data) => {
    const list = read(KEYS.cookies);
    const cookie = {
      id: uid(),
      name: data.name,
      flavor: data.flavor || "",
      price: Number(data.price) || 0,
      stock: Number(data.stock) || 0,
      ingredients: data.ingredients || [],
      createdAt: new Date().toISOString(),
    };
    list.push(cookie);
    write(KEYS.cookies, list);
    return cookie;
  },
  update: (id, data) => {
    const list = read(KEYS.cookies);
    const idx = list.findIndex((c) => c.id === id);
    if (idx === -1) return null;
    list[idx] = { ...list[idx], ...data, price: Number(data.price), stock: Number(data.stock) };
    write(KEYS.cookies, list);
    return list[idx];
  },
  remove: (id) => {
    write(KEYS.cookies, read(KEYS.cookies).filter((c) => c.id !== id));
  },
  /** Ajusta o estoque (delta pode ser negativo). */
  adjustStock: (id, delta) => {
    const list = read(KEYS.cookies);
    const idx = list.findIndex((c) => c.id === id);
    if (idx === -1) return;
    list[idx].stock = Math.max(0, list[idx].stock + delta);
    write(KEYS.cookies, list);
  },
};

/* ───── Clientes ───── */
const customerStore = {
  list: () => read(KEYS.customers),
  get: (id) => read(KEYS.customers).find((c) => c.id === id),
  getByCpf: (cpf) => read(KEYS.customers).find((c) => c.cpf === cpf),
  create: (data) => {
    const list = read(KEYS.customers);
    const customer = {
      id: uid(),
      name: data.name,
      cpf: data.cpf,
      contact: data.contact || "",
      createdAt: new Date().toISOString(),
    };
    list.push(customer);
    write(KEYS.customers, list);
    return customer;
  },
  update: (id, data) => {
    const list = read(KEYS.customers);
    const idx = list.findIndex((c) => c.id === id);
    if (idx === -1) return null;
    list[idx] = { ...list[idx], ...data };
    write(KEYS.customers, list);
    return list[idx];
  },
  remove: (id) => {
    write(KEYS.customers, read(KEYS.customers).filter((c) => c.id !== id));
  },
};

/* ───── Vendas ───── */
const saleStore = {
  list: () => read(KEYS.sales),
  get: (id) => read(KEYS.sales).find((s) => s.id === id),
  /** Ao criar, baixa estoque automaticamente e marca pendente. */
  create: (data) => {
    const list = read(KEYS.sales);
    const items = data.items.map((it) => ({
      cookieId: it.cookieId,
      cookieName: it.cookieName,
      quantity: Number(it.quantity),
      unitPrice: Number(it.unitPrice),
    }));
    const total = items.reduce((s, it) => s + it.quantity * it.unitPrice, 0);
    const sale = {
      id: uid(),
      customerId: data.customerId,
      customerName: data.customerName,
      customerCpf: data.customerCpf,
      items,
      total,
      paymentMethod: data.paymentMethod, // "pix" | "dinheiro" | "cartao" | "fiado"
      paymentStatus: "pending",          // sempre nasce pendente
      payLater: data.payLater || data.paymentMethod === "fiado",
      notes: data.notes || "",
      createdAt: new Date().toISOString(),
      paidAt: null,
    };
    items.forEach((it) => cookieStore.adjustStock(it.cookieId, -it.quantity));
    list.push(sale);
    write(KEYS.sales, list);
    return sale;
  },
  markPaid: (id) => {
    const list = read(KEYS.sales);
    const idx = list.findIndex((s) => s.id === id);
    if (idx === -1) return;
    list[idx].paymentStatus = "paid";
    list[idx].paidAt = new Date().toISOString();
    write(KEYS.sales, list);
  },
  markPending: (id) => {
    const list = read(KEYS.sales);
    const idx = list.findIndex((s) => s.id === id);
    if (idx === -1) return;
    list[idx].paymentStatus = "pending";
    list[idx].paidAt = null;
    write(KEYS.sales, list);
  },
  remove: (id) => {
    // devolve estoque
    const sale = saleStore.get(id);
    if (sale) sale.items.forEach((it) => cookieStore.adjustStock(it.cookieId, it.quantity));
    write(KEYS.sales, read(KEYS.sales).filter((s) => s.id !== id));
  },
};
