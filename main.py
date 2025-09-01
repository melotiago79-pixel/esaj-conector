from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="e-SAJ Connector", version="0.1.0", description="Conector simples para o GPT do e-SAJ")

# CORS liberado (pode restringir depois)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CNJ_PUNCT = re.compile(r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}")
DIGITS_20 = re.compile(r"\b\d{20}\b")

def normalize_cnj(npu_raw: str) -> str:
    if not npu_raw:
        return ""
    m = CNJ_PUNCT.search(npu_raw)
    if m:
        return m.group(0)
    m = DIGITS_20.search(re.sub(r"\D+", "", npu_raw))
    if m:
        digits = m.group(0)
        # NNNNNNN-DD.AAAA.J.TR.OOOO
        p1 = digits[:7]
        p2 = digits[7:9]
        p3 = digits[9:13]
        p4 = digits[13:14]
        p5 = digits[14:16]
        p6 = digits[16:20]
        return f"{p1}-{p2}.{p3}.{p4}.{p5}.{p6}"
    return ""

@app.get("/health", tags=["Infra"])
def health():
    return {"status": "ok"}

@app.get("/consulta", tags=["Consulta"])
def consulta(processo: str = Query(..., description="Número do processo (NPU/CNJ). Aceita 20 dígitos ou CNJ pontuado.")):
    """
    Endpoint mínimo para o GPT.
    - Normaliza o NPU e retorna campos básicos esperados pelo schema.
    - Aqui você pode evoluir para buscar dados reais do e-SAJ.
    """
    cnj = normalize_cnj(processo)
    if not cnj:
        return {
            "ok": False,
            "message": "NPU inválido ou não reconhecido",
            "numero": processo
        }

    # Placeholder: defina tribunal e grau por heurística do CNJ (opcional)
    tribunal = "TJSP" if cnj.endswith(".8.26.0100") or ".8.26." in cnj else None

    return {
        "ok": True,
        "numero": cnj,
        "tribunal": tribunal,
        "grau": "1GRAU",
        "url_publica": None,
        "resumo": None,
        "partes": [],
        "movimentacoes": [],
        "message": "Conector online (dados reais ainda não implementados neste template)."
    }
