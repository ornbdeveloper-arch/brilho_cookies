/* Layout compartilhado: injeta sidebar em todas as páginas para evitar duplicação. */
function renderLayout(activePage) {
  const root = document.getElementById("app");
  const main = document.getElementById("main-content");
  const mainHTML = main ? main.innerHTML : "";


  /* 
  Estrutura da Sidebar e seus itens editáveis
  */
  root.innerHTML = `
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-logo">🍪</div>
        <div class="brand-text">
          <div class="brand-name">Brilho Cookies</div>
          <div class="brand-sub">Sua renda extra docinha</div>
        </div>
      </div>
      <div class="nav-label">Menu</div>
      <nav class="nav">
        <a href="index.html"><span class="nav-icon">🏠</span> Dashboard</a>
        <a href="cookies.html"><span class="nav-icon">🍪</span> Cookies</a>
        <a href="clientes.html"><span class="nav-icon">👥</span> Clientes</a>
        <a href="vendas.html"><span class="nav-icon">🛍️</span> Vendas</a>
        <a href="fidelidade.html"><span class="nav-icon">💖</span> Fidelidade</a>
      </nav>
    </aside>
    <main class="main">
      <button class="btn ghost sm menu-toggle">☰ Menu</button>
      <div id="page">${mainHTML}</div>
    </main>`;
  setupSidebar();
}
