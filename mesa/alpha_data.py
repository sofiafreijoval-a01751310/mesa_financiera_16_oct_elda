"""Validación y recuperación de datos financieros desde Alpha Vantage."""
import requests


def completar_ficha(ticker, ficha, api_key):
    """Complementa campos ausentes; jamás inventa cifras."""
    def consulta(nombre):
        resp = requests.get("https://www.alphavantage.co/query",
                            params={"function": nombre, "symbol": ticker, "apikey": api_key},
                            timeout=20)
        resp.raise_for_status()
        datos = resp.json()
        if any(x in datos for x in ("Note", "Information", "Error Message")):
            raise RuntimeError("Alpha Vantage no entregó datos, posible cuota o acceso")
        return datos

    def poner(campo, dato):
        if ficha.get(campo) is None and dato not in (None, "", "-", "None", "N/A"):
            ficha[campo] = dato

    if ficha.get("precio") is None:
        d = consulta("GLOBAL_QUOTE").get("Global Quote", {})
        poner("precio", d.get("05. price"))
        poner("cambio_pct", d.get("10. change percent"))
        poner("fecha_dato", d.get("07. latest trading day"))
    if any(ficha.get(k) is None for k in ("beta", "pe_ratio", "max_52s", "min_52s")):
        d = consulta("OVERVIEW")
        for a, b in (("nombre", "Name"), ("sector", "Sector"),
                     ("beta", "Beta"), ("pe_ratio", "PERatio"),
                     ("max_52s", "52WeekHigh"), ("min_52s", "52WeekLow"),
                     ("cap_mercado_usd", "MarketCapitalization")):
            poner(a, d.get(b))
    return ficha
