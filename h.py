import financial as f
from flask import Flask, request,jsonify


# finance = f.Extraccion()
# simbolos=finance.get_simbol_sp500()
# # print(finance.get_ShortInfo(simbolos))
# info=finance.get_ShortInfo(simbolos[0:5]) 

def d():
    finance = f.Extraccion()
    simbolos=finance.get_simbol_sp500()
    # print(finance.get_ShortInfo(simbolos))
    info=finance.get_ShortInfo(simbolos[0:5]) 
    return jsonify(info),200

