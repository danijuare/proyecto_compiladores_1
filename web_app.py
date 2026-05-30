"""
Servidor web para la interfaz HTML del compilador.
Ejecutar: python web_app.py
Abrir:   http://127.0.0.1:5000
"""
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from main import compilar_codigo

DIRECTORIO = Path(__file__).resolve().parent
WEB_DIR = DIRECTORIO / "web"
EJEMPLOS = sorted(DIRECTORIO.glob("prueba*.txt"))

app = Flask(__name__, static_folder=str(WEB_DIR), static_url_path="")


@app.route("/")
def inicio():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/api/compilar", methods=["POST"])
def api_compilar():
    datos = request.get_json(silent=True) or {}
    codigo = datos.get("codigo", "")
    if not isinstance(codigo, str):
        return jsonify({"exito": False, "errores": ["Código inválido"]}), 400
    return jsonify(compilar_codigo(codigo))


@app.route("/api/ejemplos")
def api_ejemplos():
    return jsonify([f.name for f in EJEMPLOS])


@app.route("/api/ejemplo/<nombre>")
def api_ejemplo(nombre):
    ruta = DIRECTORIO / nombre
    if not ruta.is_file() or not nombre.startswith("prueba") or ruta.suffix != ".txt":
        return jsonify({"error": "Archivo no permitido"}), 404
    return jsonify({"nombre": nombre, "codigo": ruta.read_text(encoding="utf-8")})


if __name__ == "__main__":
    print("Compilador web en http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)
