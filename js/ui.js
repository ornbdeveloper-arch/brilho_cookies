/* 🍪 CookieJar — Helpers de UI: modal, toast, formatação, sidebar, máscara CPF */

const fmt = {
  brl: (n) => Number(n || 0).toLocaleString("pt-BR", { style: "currency", currency: "BRL" }),
  date: (iso) => {
    if (!iso) return "—";
    const d = new Date(iso);
    return d.toLocaleDateString("pt-BR") + " " + d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  },
  cpf: (cpf) => {
    const v = (cpf || "").replace(/\D/g, "").padStart(11, "0").slice(0, 11);
    return v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
  },
};

/** Aplica máscara de CPF em um input enquanto digita. */
function maskCpf(input) {
  input.addEventListener("input", () => {
    let v = input.value.replace(/\D/g, "").slice(0, 11);
    v = v.replace(/(\d{3})(\d)/, "$1.$2");
    v = v.replace(/(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
    v = v.replace(/(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
    input.value = v;
  });
}

/* ───── Toast ───── */
function ensureToastContainer() {
  let c = document.querySelector(".toast-container");
  if (!c) {
    c = document.createElement("div");
    c.className = "toast-container";
    document.body.appendChild(c);
  }
  return c;
}
function toast(msg, type = "info") {
  const c = ensureToastContainer();
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = msg;
  c.appendChild(el);
  setTimeout(() => { el.style.opacity = "0"; el.style.transform = "translateX(20px)"; }, 2400);
  setTimeout(() => el.remove(), 2800);
}

/* ───── Modal ───── */
function openModal({ title, subtitle, body, onConfirm, confirmText = "Salvar", cancelText = "Cancelar", danger = false }) {
  const backdrop = document.createElement("div");
  backdrop.className = "modal-backdrop open";
  backdrop.innerHTML = `
    <div class="modal" role="dialog" aria-modal="true">
      <h2>${title}</h2>
      ${subtitle ? `<p class="modal-sub">${subtitle}</p>` : ""}
      <div class="modal-body"></div>
      <div class="modal-actions">
        <button class="btn ghost" data-act="cancel">${cancelText}</button>
        <button class="btn ${danger ? "danger" : ""}" data-act="confirm">${confirmText}</button>
      </div>
    </div>`;
  document.body.appendChild(backdrop);
  const modalBody = backdrop.querySelector(".modal-body");
  if (typeof body === "string") modalBody.innerHTML = body;
  else if (body instanceof Node) modalBody.appendChild(body);

  const close = () => backdrop.remove();
  backdrop.querySelector('[data-act="cancel"]').onclick = close;
  backdrop.querySelector('[data-act="confirm"]').onclick = () => {
    const ok = onConfirm ? onConfirm(modalBody) : true;
    if (ok !== false) close();
  };
  backdrop.addEventListener("click", (e) => { if (e.target === backdrop) close(); });
  return { close, root: backdrop };
}

function confirmModal({ title, message, confirmText = "Confirmar", danger = true }) {
  return new Promise((resolve) => {
    openModal({
      title, subtitle: message, body: "",
      confirmText, cancelText: "Cancelar", danger,
      onConfirm: () => { resolve(true); return true; },
    });
    // se cancelar, resolve false na remoção
    setTimeout(() => {
      const bd = document.querySelectorAll(".modal-backdrop");
      const last = bd[bd.length - 1];
      if (!last) return;
      const obs = new MutationObserver(() => {
        if (!document.body.contains(last)) { resolve(false); obs.disconnect(); }
      });
      obs.observe(document.body, { childList: true });
    }, 0);
  });
}

/* ───── Sidebar ativa + toggle mobile ───── */
function setupSidebar() {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav a").forEach((a) => {
    if (a.getAttribute("href") === path) a.classList.add("active");
  });
  const toggle = document.querySelector(".menu-toggle");
  const sidebar = document.querySelector(".sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
  }
}

document.addEventListener("DOMContentLoaded", setupSidebar);
