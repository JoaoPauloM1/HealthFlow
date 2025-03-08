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
            return render_template("calculadora_imc.html", erro="Provide weight and height")

        imc = round(peso / (altura ** 2), 2)
    
    return render_template("calculadora_imc.html", imc=imc)

@app.route("/calcular_calorias", methods=["GET", "POST"])
def calcular_calorias():
    calorias_diarias = None
    calorias_ganhar = None
    calorias_perder = None
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
                erro = "All fields are required."
                return render_template("calculadora_calorias.html", erro=erro)

            if sexo == "homem":
                taxa_basal = round(88.36 + (13.4 * peso) + (4.8 * altura * 100) - (5.7 * idade))
            elif sexo == "mulher":
                taxa_basal = round(447.6 + (9.2 * peso) + (3.1 * altura * 100) - (4.3 * idade))
            else:
                erro = "Invalid gender. Please choose 'Male' or 'Female'."
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
                erro = "Invalid activity level."
                return render_template("calculadora_calorias.html", erro=erro)

            calorias_diarias = round(taxa_basal * fator)
            calorias_perder = round(calorias_diarias - 500)
            calorias_ganhar = round(calorias_diarias + 500)

        except ValueError:
            erro = "Please enter valid values for weight, height, and age."

    return render_template(
        "calculadora_calorias.html",
        taxa_basal=taxa_basal,
        calorias_diarias=calorias_diarias,
        calorias_ganhar=calorias_ganhar,
        calorias_perder=calorias_perder,
        erro=erro
    )

@app.route("/calcular_agua", methods=["GET", "POST"])
def calcular_agua():
    quantidade_agua = None
    erro = None

    if request.method == "POST":
        try:
            peso = float(request.form.get("peso"))
            atividade = request.form.get("atividade").lower()

            if not peso or not atividade:
                erro = "All fields are required."
                return render_template("calculadora_agua.html", erro=erro)

            if atividade == "não":
                quantidade_agua = peso * 35
            elif atividade == "sim":
                horas_treino = float(request.form.get("horas_treino", 0))
                quantidade_agua = (peso * 35) + (horas_treino * 500)
            else:
                erro = "Invalid activity option. Please choose 'Yes' or 'No'."
        except ValueError:
            erro = "Enter valid values for weight and training hours."

    return render_template("calculadora_agua.html", quantidade_agua=quantidade_agua, erro=erro)

@app.route("/calcular_frequencia_cardiaca", methods=["GET", "POST"])
def calcular_frequencia():
    frequencia_maxima = None
    zona_leve = None
    zona_moderada = None
    zona_intensa = None
    erro = None

    if request.method == "POST":
        try:
            idade = int(request.form.get("idade"))

            if idade <= 0:
                erro = "The age must be greater than zero."
            else:
                frequencia_maxima = 220 - idade

                zona_leve = (frequencia_maxima * 0.5, frequencia_maxima * 0.6)
                zona_moderada = (frequencia_maxima * 0.7, frequencia_maxima * 0.8)
                zona_intensa = (frequencia_maxima * 0.85, frequencia_maxima * 0.9)
        except ValueError:
            erro = "Please enter a valid age."

    return render_template(
        "calculadora_cardiaca.html",
        frequencia_maxima=frequencia_maxima,
        zona_leve=zona_leve,
        zona_moderada=zona_moderada,
        zona_intensa=zona_intensa,
        erro=erro,
    )

@app.route("/calcular_macronutrientes", methods=["GET", "POST"])
def calcular_macronutrientes():
    carboidratos = gorduras = proteinas = None
    erro = None

    if request.method == "POST":
        try:
            calorias = float(request.form.get("calorias"))
            objetivo = request.form.get("objetivo")

            if not calorias or not objetivo:
                erro = "Provide your daily calories and choose a goal."
                return render_template("calculadora_macronutrientes.html", erro=erro)

            if objetivo == "equilibrada":
                carboidratos = (calorias * 0.50) / 4
                gorduras = (calorias * 0.30) / 9
                proteinas = (calorias * 0.20) / 4
            elif objetivo == "ganho_massa":
                carboidratos = (calorias * 0.40) / 4
                gorduras = (calorias * 0.30) / 9
                proteinas = (calorias * 0.30) / 4
            else:
                erro = "Invalid object."
                return render_template("calculadora_macronutrientes.html", erro=erro)

        except ValueError:
            erro = "Please, enter valid values."

    return render_template(
        "calculadora_macronutrientes.html",
        carboidratos=round(carboidratos, 2) if carboidratos else None,
        gorduras=round(gorduras, 2) if gorduras else None,
        proteinas=round(proteinas, 2) if proteinas else None,
        erro=erro
    )

if __name__ == "__main__":
    app.run(debug=True)