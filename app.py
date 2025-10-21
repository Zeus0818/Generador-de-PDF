from flask import Flask, render_template_string, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

# ---------------- Plantilla con Bootstrap ---------------- #
form_template = """
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Generar PDF</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container mt-5">
      <div class="card shadow-lg p-4">
        <h2 class="mb-4 text-center">Formulario de Registro</h2>
        <form method="POST" action="/submit">
          <div class="mb-3">
            <label class="form-label">Nombre</label>
            <input type="text" class="form-control" name="nombre" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Apellido</label>
            <input type="text" class="form-control" name="apellido" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Edad</label>
            <input type="number" class="form-control" name="edad" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Número de Celular</label>
            <input type="text" class="form-control" name="celular" required>
          </div>
          <button type="submit" class="btn btn-primary w-100">Generar PDF</button>
        </form>
      </div>
    </div>
  </body>
</html>
"""

# ---------------- Ruta principal ---------------- #
@app.route("/")
def index():
    return render_template_string(form_template)

# ---------------- Procesar y generar PDF ---------------- #
@app.route("/submit", methods=["POST"])
def submit():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    edad = request.form["edad"]
    celular = request.form["celular"]

    # Crear PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(200, 10, "Información Personal", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Nombre: {nombre}", ln=True)
    pdf.cell(200, 10, f"Apellido: {apellido}", ln=True)
    pdf.cell(200, 10, f"Edad: {edad}", ln=True)
    pdf.cell(200, 10, f"Número de Celular: {celular}", ln=True)

    # Guardar en memoria y enviar
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    return send_file(pdf_output, as_attachment=True, download_name="informacion.pdf")

if __name__ == "__main__":
    app.run(debug=True)
