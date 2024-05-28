import financial as f
from flask import Flask, request,jsonify

app = Flask(__name__)

@app.route("/")



def financialData():
    finance = f.Extraccion()
    simbolos=finance.get_simbol_sp500()
    # print(finance.get_ShortInfo(simbolos))
    info=finance.get_ShortInfo(simbolos[0:]) 
    return jsonify(info),200



if __name__ == "__main__":
    app.run(debug=True)