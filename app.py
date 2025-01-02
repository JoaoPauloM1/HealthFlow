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
            calorias_perder = round(calorias_diarias - 500)
            calorias_ganhar = round(calorias_diarias + 500)

        except ValueError:
            erro = "Insira valores válidos para peso, altura e idade."

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
                erro = "Todos os campos são obrigatórios."
                return render_template("calculadora_agua.html", erro=erro)

            if atividade == "não":
                quantidade_agua = peso * 35
            elif atividade == "sim":
                horas_treino = float(request.form.get("horas_treino", 0))
                quantidade_agua = (peso * 35) + (horas_treino * 500)
            else:
                erro = "Opção de atividade inválida. Escolha 'Sim' ou 'Não'."
        except ValueError:
            erro = "Insira valores válidos para peso e horas de treino."

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
                erro = "A idade deve ser maior que zero."
            else:
                frequencia_maxima = 220 - idade

                zona_leve = (frequencia_maxima * 0.5, frequencia_maxima * 0.6)
                zona_moderada = (frequencia_maxima * 0.7, frequencia_maxima * 0.8)
                zona_intensa = (frequencia_maxima * 0.85, frequencia_maxima * 0.9)
        except ValueError:
            erro = "Insira uma idade válida."

    return render_template(
        "calculadora_cardiaca.html",
        frequencia_maxima=frequencia_maxima,
        zona_leve=zona_leve,
        zona_moderada=zona_moderada,
        zona_intensa=zona_intensa,
        erro=erro,
    )

@app.route("/dicas")
def dicas():
    exercicios = [
        "Caminhada ou corrida (cardio leve a moderado).",
        "Treinamento de força (levantamento de peso).",
        "Yoga para flexibilidade e relaxamento.",
        "HIIT (treino intervalado de alta intensidade).",
        "Natação ou ciclismo para impacto reduzido nas articulações."
    ]

    alimentos_proteinas = [
        "Peito de frango.",
        "Ovos.",
        "Iogurte grego.",
        "Tofu.",
        "Peixes (salmão, atum, sardinha).",
        "Feijão e lentilha."
    ]

    alimentos_carboidratos = [
        "Batata-doce.",
        "Arroz integral.",
        "Quinoa.",
        "Aveia.",
        "Frutas (banana, maçã, frutas vermelhas).",
        "Legumes (cenoura, abóbora, beterraba)."
    ]

    alimentos_gorduras = [
        "Abacate.",
        "Azeite de oliva.",
        "Nozes e castanhas.",
        "Sementes de chia e linhaça.",
        "Peixes ricos em ômega-3 (salmão, cavala).",
        "Manteiga de amendoim natural."
    ]

    return render_template(
        "dicas.html",
        exercicios=exercicios,
        alimentos_proteinas=alimentos_proteinas,
        alimentos_carboidratos=alimentos_carboidratos,
        alimentos_gorduras=alimentos_gorduras
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
                erro = "Forneça as calorias diárias e escolha um objetivo."
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
                erro = "Objetivo inválido."
                return render_template("calculadora_macronutrientes.html", erro=erro)

        except ValueError:
            erro = "Por favor, insira valores válidos."

    return render_template(
        "calculadora_macronutrientes.html",
        carboidratos=round(carboidratos, 2) if carboidratos else None,
        gorduras=round(gorduras, 2) if gorduras else None,
        proteinas=round(proteinas, 2) if proteinas else None,
        erro=erro
    )

if __name__ == "__main__":
    app.run(debug=True)