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
        aviso = " ".join(str(datos.get(k, "")) for k in ("Note", "Information", "Error Message")).lower()
        if aviso:
            if any(k in aviso for k in ("limit", "frequency", "calls per", "requests per", "rate")):
                motivo = "límite de consultas alcanzado"
            elif any(k in aviso for k in ("premium", "subscription", "paid", "subscribe")):
                motivo = "endpoint restringido por el plan"
            elif any(k in aviso for k in ("invalid", "apikey", "api key")):
                motivo = "clave posiblemente inválida o no autorizada"
            else:
                motivo = "respuesta informativa o error del proveedor"
            raise RuntimeError(f"Alpha Vantage {nombre}: {motivo}. Revisa cuota y permisos.")
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
