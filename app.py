from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcular_imc", methods=["GET", "POST"])
def calcular_imc():
    imc = None
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))

        if not peso or not altura:
            return render_template("calculadora_imc.html", erro="Forneça peso e altura")

        imc = round(peso / (altura ** 2), 2)
    
    return render_template("calculadora_imc.html", imc=imc)

@app.route("/calcular_calorias", methods=["GET", "POST"])
def calcular_calorias():
    calorias = None
    taxa_basal = None
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        idade = float(request.form.get("idade"))

        if not peso or not altura or not idade:
            return render_template("calculadora_calorias.html", erro="Forneça peso, altura e idade")

        taxa_basal = round(88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade))
    
    return render_template("calculadora_calorias.html", taxa_basal=taxa_basal)


if __name__ == "__main__":
    app.run(debug=True)