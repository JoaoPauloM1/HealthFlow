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
    calorias_diarias = None
    taxa_basal = None
    erro = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            altura = float(request.form.get("altura"))
            idade = float(request.form.get("idade"))
            sexo = request.form.get("sexo").lower()
            atividade = request.form.get("atividade").lower()

            if not peso or not altura or not idade or not sexo or not atividade:
                erro = "Todos os campos são obrigatórios."
                return render_template("calculadora_calorias.html", erro=erro)

            if sexo == "homem":
                taxa_basal = round(88.36 + (13.4 * peso) + (4.8 * altura * 100) - (5.7 * idade))
            elif sexo == "mulher":
                taxa_basal = round(447.6 + (9.2 * peso) + (3.1 * altura * 100) - (4.3 * idade))
            else:
                erro = "Sexo inválido. Escolha 'Homem' ou 'Mulher'."
                return render_template("calculadora_calorias.html", erro=erro)

            fatores_atividade = {
                "sedentario": 1.2,
                "leve": 1.375,
                "moderado": 1.55,
                "intenso": 1.725,
                "muito_intenso": 1.9
            }

            fator = fatores_atividade.get(atividade)
            if not fator:
                erro = "Nível de atividade inválido."
                return render_template("calculadora_calorias.html", erro=erro)

            calorias_diarias = round(taxa_basal * fator)

        except ValueError:
            erro = "Insira valores válidos para peso, altura e idade."

    return render_template(
        "calculadora_calorias.html",
        taxa_basal=taxa_basal,
        calorias_diarias=calorias_diarias,
        erro=erro
    )

if __name__ == "__main__":
    app.run(debug=True)