import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from main import compilar_codigo

DIRECTORIO = Path(__file__).resolve().parent
EJEMPLOS = [
    "prueba_1.txt",
    "prueba_2.txt",
    "prueba_3.txt",
    "prueba_para.txt",
    "prueba_funcion.txt",
    "prueba_procedimiento.txt",
    "prueba_correcta.txt",
    "prueba_error.txt",
]

COLORES = {
    "fondo": "#1e1e2e",
    "panel": "#252536",
    "editor": "#2a2a3c",
    "texto": "#cdd6f4",
    "texto_sec": "#a6adc8",
    "acento": "#89b4fa",
    "exito": "#a6e3a1",
    "error": "#f38ba8",
    "borde": "#45475a",
}


class CompiladorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Compilador — Analizador léxico y sintáctico")
        self.geometry("960x640")
        self.minsize(720, 480)
        self.configure(bg=COLORES["fondo"])

        self.archivo_actual = None
        self._configurar_estilos()
        self._crear_interfaz()
        self._cargar_ejemplo("prueba_correcta.txt")

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure(
            "TButton",
            background=COLORES["panel"],
            foreground=COLORES["texto"],
            borderwidth=0,
            padding=(12, 6),
        )
        estilo.map(
            "TButton",
            background=[("active", COLORES["borde"])],
        )
        estilo.configure(
            "Accent.TButton",
            background=COLORES["acento"],
            foreground=COLORES["fondo"],
            font=("Segoe UI", 9, "bold"),
        )
        estilo.map(
            "Accent.TButton",
            background=[("active", "#74a8f7")],
        )

    def _crear_interfaz(self):
        barra = tk.Frame(self, bg=COLORES["panel"], pady=8, padx=12)
        barra.pack(fill=tk.X)

        ttk.Button(barra, text="Abrir .txt…", command=self._abrir_archivo).pack(
            side=tk.LEFT, padx=(0, 6)
        )
        ttk.Button(
            barra, text="Compilar", style="Accent.TButton", command=self._compilar
        ).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(barra, text="Limpiar", command=self._limpiar).pack(
            side=tk.LEFT, padx=(0, 16)
        )

        tk.Label(
            barra,
            text="Ejemplos:",
            bg=COLORES["panel"],
            fg=COLORES["texto_sec"],
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT, padx=(0, 6))

        for nombre in EJEMPLOS:
            ttk.Button(
                barra,
                text=nombre.replace(".txt", ""),
                command=lambda n=nombre: self._cargar_ejemplo(n),
            ).pack(side=tk.LEFT, padx=2)

        cuerpo = tk.PanedWindow(
            self,
            orient=tk.VERTICAL,
            bg=COLORES["fondo"],
            sashwidth=6,
            sashrelief=tk.FLAT,
            opaqueresize=True,
        )
        cuerpo.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 8))

        marco_codigo, area_codigo = self._marco_seccion(cuerpo, "Código fuente")
        cuerpo.add(marco_codigo, minsize=200)

        self.editor = tk.Text(
            area_codigo,
            wrap=tk.NONE,
            bg=COLORES["editor"],
            fg=COLORES["texto"],
            insertbackground=COLORES["acento"],
            selectbackground=COLORES["borde"],
            font=("Consolas", 11),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            undo=True,
        )
        scroll_y = tk.Scrollbar(
            area_codigo, command=self.editor.yview, bg=COLORES["panel"]
        )
        scroll_x = tk.Scrollbar(
            area_codigo, orient=tk.HORIZONTAL, command=self.editor.xview
        )
        self.editor.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        marco_salida, area_salida = self._marco_seccion(
            cuerpo, "Resultado de la compilación"
        )
        cuerpo.add(marco_salida, minsize=120)

        self.salida = tk.Text(
            area_salida,
            wrap=tk.WORD,
            bg=COLORES["panel"],
            fg=COLORES["texto"],
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED,
        )
        self.salida.pack(fill=tk.BOTH, expand=True)

        self.salida.tag_configure("exito", foreground=COLORES["exito"])
        self.salida.tag_configure("error", foreground=COLORES["error"])
        self.salida.tag_configure("titulo", foreground=COLORES["acento"], font=("Segoe UI", 10, "bold"))
        self.salida.tag_configure("sec", foreground=COLORES["texto_sec"])

        self.barra_estado = tk.Label(
            self,
            text="Listo",
            anchor=tk.W,
            bg=COLORES["panel"],
            fg=COLORES["texto_sec"],
            font=("Segoe UI", 9),
            padx=12,
            pady=6,
        )
        self.barra_estado.pack(fill=tk.X)

        self.bind("<Control-o>", lambda _: self._abrir_archivo())
        self.bind("<Control-O>", lambda _: self._abrir_archivo())
        self.bind("<F5>", lambda _: self._compilar())
        self.bind("<Control-Return>", lambda _: self._compilar())

    def _marco_seccion(self, padre, titulo):
        marco = tk.Frame(padre, bg=COLORES["fondo"])
        tk.Label(
            marco,
            text=titulo,
            bg=COLORES["fondo"],
            fg=COLORES["texto_sec"],
            font=("Segoe UI", 9),
            anchor=tk.W,
        ).pack(fill=tk.X, pady=(0, 4))
        contenido = tk.Frame(marco, bg=COLORES["borde"], padx=1, pady=1)
        contenido.pack(fill=tk.BOTH, expand=True)
        return marco, contenido

    def _abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Abrir archivo fuente",
            initialdir=DIRECTORIO,
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")],
        )
        if not ruta:
            return
        try:
            codigo = Path(ruta).read_text(encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{exc}")
            return
        self._establecer_codigo(codigo, Path(ruta))

    def _cargar_ejemplo(self, nombre):
        ruta = DIRECTORIO / nombre
        if not ruta.exists():
            messagebox.showwarning("Aviso", f"No se encontró {nombre}")
            return
        self._establecer_codigo(ruta.read_text(encoding="utf-8"), ruta)

    def _establecer_codigo(self, codigo, ruta):
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", codigo)
        self.archivo_actual = ruta
        self._limpiar_salida()
        self.barra_estado.config(text=f"Archivo: {ruta.name}")

    def _limpiar(self):
        self.editor.delete("1.0", tk.END)
        self.archivo_actual = None
        self._limpiar_salida()
        self.barra_estado.config(text="Editor vacío")

    def _limpiar_salida(self):
        self.salida.config(state=tk.NORMAL)
        self.salida.delete("1.0", tk.END)
        self.salida.config(state=tk.DISABLED)

    def _escribir_salida(self, lineas):
        self.salida.config(state=tk.NORMAL)
        self.salida.delete("1.0", tk.END)
        for texto, etiqueta in lineas:
            self.salida.insert(tk.END, texto, etiqueta)
        self.salida.config(state=tk.DISABLED)

    def _compilar(self):
        codigo = self.editor.get("1.0", tk.END)
        resultado = compilar_codigo(codigo)

        if resultado["exito"]:
            lineas = [
                ("✓ Compilado correctamente\n\n", "titulo"),
                ("No se encontraron errores léxicos ni sintácticos.", "exito"),
            ]
            self.barra_estado.config(
                text=f"Éxito — {self._nombre_archivo()}"
            )
        else:
            n = len(resultado["errores"])
            lineas = [
                (f"✗ Se encontraron {n} error(es)\n\n", "titulo"),
            ]
            for i, error in enumerate(resultado["errores"], 1):
                lineas.append((f"{i}. {error}\n", "error"))
            self.barra_estado.config(
                text=f"{n} error(es) — {self._nombre_archivo()}"
            )

        self._escribir_salida(lineas)

    def _nombre_archivo(self):
        if self.archivo_actual:
            return self.archivo_actual.name
        return "sin guardar"


def main():
    app = CompiladorGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
