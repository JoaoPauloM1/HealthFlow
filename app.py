from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Serve a página HTML principal

@app.route("/calcular_imc", methods=["POST"])
def calcular_imc():
    data = request.json
    peso = data.get("peso")
    altura = data.get("altura")

    if not peso or not altura:
        return jsonify({"erro": "Forneça peso e altura"}), 400

    imc = peso / (altura ** 2)
    return jsonify({"imc": round(imc, 2)})

if __name__ == "__main__":
    app.run(debug=True)