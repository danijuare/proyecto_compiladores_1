const editor = document.getElementById("editor");
const lineNumbers = document.getElementById("line-numbers");
const resultado = document.getElementById("resultado");
const estadoBadge = document.getElementById("estado-badge");
const archivoNombre = document.getElementById("archivo-nombre");
const footerStats = document.getElementById("footer-stats");
const btnCompilar = document.getElementById("btn-compilar");
const fileInput = document.getElementById("file-input");
const ejemplosSelect = document.getElementById("ejemplos-select");

let archivoActual = null;

function actualizarLineas() {
  const lineas = editor.value.split("\n").length;
  lineNumbers.textContent = Array.from({ length: lineas }, (_, i) => i + 1).join("\n");
  const chars = editor.value.length;
  footerStats.textContent = `${lineas} línea${lineas !== 1 ? "s" : ""} · ${chars} caracter${chars !== 1 ? "es" : ""}`;
}

function escaparHtml(texto) {
  return String(texto)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderizarError(detalle, indice) {
  if (typeof detalle === "string") {
    return `
      <li class="error-item" style="animation-delay:${indice * 0.05}s">
        <span class="num">${indice + 1}</span>
        <span class="msg">${escaparHtml(detalle)}</span>
      </li>`;
  }

  const tipo = detalle.tipo || "error";
  const tipoClase = tipo === "semántico" ? "error-type error-type-semantico" : "error-type";
  const linea = detalle.linea || "?";
  const col = detalle.columna || "?";
  const bloqueCodigo =
    detalle.linea_codigo
      ? `<pre class="error-code"><span class="error-ln">${linea}</span> ${escaparHtml(detalle.linea_codigo)}
<span class="error-ln"></span> ${escaparHtml(detalle.puntero || "")}</pre>`
      : "";

  return `
    <li class="error-item" style="animation-delay:${indice * 0.05}s">
      <span class="num">${indice + 1}</span>
      <div class="error-body">
        <div class="error-meta">
          <span class="${tipoClase}">${escaparHtml(tipo)}</span>
          <span class="error-pos">Línea ${linea}, columna ${col}</span>
        </div>
        <p class="error-msg">${escaparHtml(detalle.mensaje)}</p>
        <p class="error-hint">${escaparHtml(detalle.sugerencia)}</p>
        ${bloqueCodigo}
      </div>
    </li>`;
}

function mostrarExito() {
  estadoBadge.textContent = "Compilado";
  estadoBadge.className = "badge badge-ok";
  resultado.className = "resultado resultado-success";
  resultado.innerHTML = `
    <div class="success-card">
      <div class="icon-wrap" aria-hidden="true">
        <svg class="icon-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
          <polyline points="22 4 12 14.01 9 11.01"/>
        </svg>
      </div>
      <h2>Compilado correctamente</h2>
      <p>No se encontraron errores léxicos ni sintácticos en el programa.</p>
    </div>
  `;
}

function mostrarErrores(errores, detalles) {
  const lista = detalles?.length ? detalles : errores;
  const n = lista.length;
  estadoBadge.textContent = `${n} error${n !== 1 ? "es" : ""}`;
  estadoBadge.className = "badge badge-error";
  resultado.className = "resultado resultado-errors";
  const items = lista.map((d, i) => renderizarError(d, i)).join("");
  resultado.innerHTML = `
    <h2>
      Errores detectados
      <span class="count">${n}</span>
    </h2>
    <ul class="error-list">${items}</ul>
  `;
}

function mostrarIdle() {
  estadoBadge.textContent = "En espera";
  estadoBadge.className = "badge badge-idle";
  resultado.className = "resultado resultado-idle";
  resultado.innerHTML = `
    <div class="resultado-placeholder">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 16v-4M12 8h.01"/>
      </svg>
      <p>Pulsa <strong>Compilar</strong> o <kbd>F5</kbd> para analizar el programa.</p>
    </div>
  `;
}

async function compilar() {
  btnCompilar.classList.add("loading");
  estadoBadge.textContent = "Analizando…";
  estadoBadge.className = "badge badge-loading";

  try {
    const res = await fetch("/api/compilar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ codigo: editor.value }),
    });
    const data = await res.json();
    if (data.exito) {
      mostrarExito();
    } else {
      mostrarErrores(data.errores || ["Error desconocido"], data.detalles);
    }
  } catch {
    mostrarErrores(["No se pudo conectar con el servidor. Ejecuta: python web_app.py"]);
  } finally {
    btnCompilar.classList.remove("loading");
  }
}

async function cargarEjemplos() {
  try {
    const res = await fetch("/api/ejemplos");
    const lista = await res.json();
    lista.forEach((nombre) => {
      const opt = document.createElement("option");
      opt.value = nombre;
      opt.textContent = nombre.replace(".txt", "");
      ejemplosSelect.appendChild(opt);
    });
  } catch {
    /* servidor no iniciado */
  }
}

async function cargarEjemplo(nombre) {
  const res = await fetch(`/api/ejemplo/${encodeURIComponent(nombre)}`);
  if (!res.ok) return;
  const data = await res.json();
  editor.value = data.codigo;
  archivoActual = data.nombre;
  archivoNombre.textContent = data.nombre;
  actualizarLineas();
  mostrarIdle();
}

fileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    editor.value = reader.result;
    archivoActual = file.name;
    archivoNombre.textContent = file.name;
    actualizarLineas();
    mostrarIdle();
  };
  reader.readAsText(file, "UTF-8");
  e.target.value = "";
});

ejemplosSelect.addEventListener("change", () => {
  const nombre = ejemplosSelect.value;
  if (nombre) cargarEjemplo(nombre);
  ejemplosSelect.value = "";
});

btnCompilar.addEventListener("click", compilar);

editor.addEventListener("input", actualizarLineas);
editor.addEventListener("scroll", () => {
  lineNumbers.scrollTop = editor.scrollTop;
});

document.addEventListener("keydown", (e) => {
  if (e.key === "F5") {
    e.preventDefault();
    compilar();
  }
  if (e.key === "Tab") {
    e.preventDefault();
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    editor.value = editor.value.slice(0, start) + "    " + editor.value.slice(end);
    editor.selectionStart = editor.selectionEnd = start + 4;
    actualizarLineas();
  }
});

cargarEjemplos().then(() => cargarEjemplo("prueba_correcta.txt"));
actualizarLineas();
