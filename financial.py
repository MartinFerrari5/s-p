import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
class Extraccion:
    def __init__(self) -> None:
        pass
    
    def get_simbol_sp500(slef):
        """
        Obtiene una lista de los símbolos bursátiles de las empresas listadas en el Nasdaq 100.
        
        Extrae la lista de empresas del sp 500 desde la página de Wikipedia 'NASDAQ-100'
        y retorna los símbolos de las empresas como una lista de strings.
        
        Returns:
            list: Una lista de strings, cada uno representando el símbolo bursátil de una empresa.
        """
        # URL de la página de Wikipedia que lista las empresas del S&P 500
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        # Realizar una solicitud HTTP a la URL para obtener el contenido de la página
        respuesta = requests.get(url)
        # Parsear el contenido HTML de la respuesta usando BeautifulSoup
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        # Encontrar la tabla con ID 'constituents', que contiene la lista de empresas
        tabla = soup.find('table', {'id': 'constituents'})
        # Convertir la tabla HTML en un DataFrame de pandas
        df = pd.read_html(str(tabla))[0]
        # Extraer la columna 'Symbol' del DataFrame y convertirla en una lista
        return df['Symbol'].tolist()

    def get_simbol_nasdaq100(self):
        """
        Obtiene una lista de los símbolos bursátiles de las empresas listadas en el Nasdaq 100.
        
        Extrae la lista de empresas del Nasdaq 100 desde la página de Wikipedia 'NASDAQ-100'
        y retorna los símbolos de las empresas como una lista de strings.
        
        Returns:
            list: Una lista de strings, cada uno representando el símbolo bursátil de una empresa.
        """
            
        url = 'https://en.wikipedia.org/wiki/NASDAQ-100'
        respuesta = requests.get(url)
        soup = BeautifulSoup(respuesta.text, 'html.parser')
        tabla = soup.find('table', {'id': 'constituents'})
        df = pd.read_html(str(tabla))[0]
        return df['Ticker'].tolist()

    def get_ShortInfo(self, empresas: list):
        """Recibe una lista y extrae información corta de
        cada simbolo"""
        datos = []
        for simbolo in empresas:
            empresa = yf.Ticker(simbolo)
            info = empresa.info
            nombre = info.get("longName")
            capitalizacion = info.get('marketCap')
            sector = info.get("sector")
            pais = info.get("country")
            ciudad = info.get("city")
            industria = info.get("industry")
            avg_volume = info.get("averageVolume")
            precio_actual = info.get("currentPrice")
            efectivo_total = info.get("totalCash")
            ganancias_totales = info.get("totalRevenue")
            datos.append({'Empresa':nombre,
                        'Simbolo': simbolo,
                        'Capitalización': capitalizacion,
                        'Sector': sector,
                        'Pais': pais,
                        'Ciudad':ciudad,
                        'Industria':industria,
                        'Volumen Promedio':avg_volume,
                        'precio_actual':precio_actual,
                        'Total_Efectivo':efectivo_total,
                        'Ganancias_Totales':ganancias_totales})
        df = pd.DataFrame(datos)
        return datos

    def get_FinancialData(self, tickers:list):
        """Recibe una lista con simbolos financiero, y devuelve un dataframe con 
        los datos financieros asociados a ellos"""
        datos = {}
        for ticker in tickers:
            try:
                empresa = yf.Ticker(ticker)
                hist = empresa.history(period="1d")  # Cambiado a '1d' para obtener el último día disponible
                info = empresa.info
                
                datos[ticker] = {
                    'Último Precio': hist['Close'].iloc[-1] if not hist.empty else None,
                    'Capitalización de Mercado': info.get('marketCap'),
                    'Ingresos Totales': info.get('totalRevenue'),
                    'EBITDA': info.get('ebitda'),
                    'Flujo de Caja Libre': info.get('freeCashflow'),
                    'Deuda Total': info.get('totalDebt')
                }
            except Exception as e:
                print(f"Error al obtener datos para {ticker}: {e}")
                datos[ticker] = {
                    'Último Precio': None,
                    'Capitalización de Mercado': None,
                    'Ingresos Totales': None,
                    'EBITDA': None,
                    'Flujo de Caja Libre': None,
                    'Deuda Total': None
                }
        return pd.DataFrame.from_dict(datos, orient='index')
    
