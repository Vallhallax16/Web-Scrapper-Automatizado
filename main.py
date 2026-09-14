from Servicios import SAutomWeb

url = "https://www.correosdemexico.gob.mx/sslservicios/consultacp/CodigoPostal_Exportar.aspx"

headers = {
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "es-419,es;q=0.6",
    "Cache-Control": "no-cache",
    "Origin": "https://www.correosdemexico.gob.mx",
    "Pragma": "no-cache",
    "Referer": url,
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/152.0.0.0 Safari/537.36"
    )
}

campos = [
    "__EVENTTARGET",
    "__EVENTARGUMENT",
    "__LASTFOCUS",
    "__VIEWSTATE",
    "__VIEWSTATEGENERATOR",
    "__EVENTVALIDATION"
]

estado = "00"

formato = "txt"

actualPayload = {
    "cboEdo": estado,
    "rblTipo": formato,
    "btnDescarga.x": "56",
    "btnDescarga.y": "5"
}

automWS = SAutomWeb.AutomWeb()
automWS.iniciarWS(headers, url, campos, actualPayload)

