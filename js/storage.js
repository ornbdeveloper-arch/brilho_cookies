/* Brilho Cookies - camada de persistencia via API/Supabase.
   As telas continuam usando cookieStore, customerStore e saleStore. */

const API_BASE = window.BRILHO_API_URL || "https://brilho-cookies-1.onrender.com";

const state = {
  cookies: [],
  customers: [],
  sales: [],
};

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    let message = text;
    try {
      const body = JSON.parse(text);
      message = body.detail || body.erro || text;
    } catch (_) {
      message = text;
    }
    throw new Error(message || `Erro na API: ${response.status}`);
  }
  if (response.status === 204) return null;
  return response.json();
}

async function loadAllData() {
  const [cookies, customers, sales] = await Promise.all([
    request("/cookies/"),
    request("/clientes/"),
    request("/vendas/"),
  ]);
  state.cookies = cookies;
  state.customers = customers;
  state.sales = sales;
}

function replaceById(list, item) {
  const index = list.findIndex((entry) => entry.id === item.id);
  if (index === -1) list.push(item);
  else list[index] = item;
  return item;
}

const brilhoStore = {
  ready: loadAllData(),
  reload: loadAllData,
};

const cookieStore = {
  list: () => state.cookies,
  get: (id) => state.cookies.find((c) => c.id === id),
  create: async (data) => {
    const cookie = await request("/cookies/", {
      method: "POST",
      body: JSON.stringify(data),
    });
    state.cookies.push(cookie);
    return cookie;
  },
  update: async (id, data) => {
    const cookie = await request(`/cookies/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
    return replaceById(state.cookies, cookie);
  },
  remove: async (id) => {
    await request(`/cookies/${id}`, { method: "DELETE" });
    state.cookies = state.cookies.filter((c) => c.id !== id);
  },
};

const customerStore = {
  list: () => state.customers,
  get: (id) => state.customers.find((c) => c.id === id),
  getByCpf: (cpf) => state.customers.find((c) => c.cpf === cpf),
  create: async (data) => {
    const customer = await request("/clientes/", {
      method: "POST",
      body: JSON.stringify(data),
    });
    state.customers.push(customer);
    return customer;
  },
  update: async (id, data) => {
    const customer = await request(`/clientes/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
    return replaceById(state.customers, customer);
  },
  remove: async (id) => {
    await request(`/clientes/${id}`, { method: "DELETE" });
    state.customers = state.customers.filter((c) => c.id !== id);
  },
};

const saleStore = {
  list: () => state.sales,
  get: (id) => state.sales.find((s) => s.id === id),
  create: async (data) => {
    const sale = await request("/vendas/", {
      method: "POST",
      body: JSON.stringify(data),
    });
    state.sales.push(sale);
    await loadAllData();
    return sale;
  },
  markPaid: async (id) => {
    const sale = await request(`/vendas/${id}/pagar`, { method: "PATCH" });
    return replaceById(state.sales, sale);
  },
  markPending: async (id) => {
    const sale = await request(`/vendas/${id}/pendente`, { method: "PATCH" });
    return replaceById(state.sales, sale);
  },
  remove: async (id) => {
    await request(`/vendas/${id}`, { method: "DELETE" });
    await loadAllData();
  },
};
