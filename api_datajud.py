# API DataJud CNJ - Backend para Agente OpenAI
from datetime import datetime, timezone
import logging
import os
import re
from typing import List, Optional

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

APP_VERSION = "1.1.0"

logger = logging.getLogger("datajud")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="DataJud API", version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATAJUD_BASE_URL = "https://api-publica.datajud.cnj.jus.br"
DATAJUD_API_KEY = os.getenv(
    "DATAJUD_API_KEY",
    "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==",
)

TRIBUNAIS = {
    "TJSP": "api_publica_tjsp",
    "TJRJ": "api_publica_tjrj",
    "TJMG": "api_publica_tjmg",
    "STJ": "api_publica_stj",
    "STF": "api_publica_stf",
    "TST": "api_publica_tst",
    "TNU": "api_publica_tnu",
}

TRIBUNAL_REGEX = re.compile(r"^[A-Z0-9]{2,10}$")


class JurisprudenciaRequest(BaseModel):
    termo_busca: Optional[str] = None
    tribunal: str = "TJSP"
    numero_processo: Optional[str] = None
    classe_processual: Optional[str] = None
    tamanho: int = Field(default=10, ge=1, le=50)

    @validator("tribunal")
    def normalize_tribunal(cls, value: str) -> str:
        normalized = value.upper().strip()
        if not TRIBUNAL_REGEX.match(normalized):
            raise ValueError("Tribunal inválido")
        return normalized

    @validator("termo_busca", "numero_processo", "classe_processual", pre=True)
    def normalize_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = value.strip()
        return normalized or None


class ProcessoJurisprudencia(BaseModel):
    id: Optional[str] = None
    numeroProcesso: Optional[str] = None
    tribunal: Optional[str] = None
    classe: Optional[str] = None
    codigoClasse: Optional[str] = None
    assunto: Optional[str] = None
    dataAjuizamento: Optional[str] = None
    dataJulgamento: Optional[str] = None
    dataPublicacao: Optional[str] = None
    orgaoJulgador: Optional[str] = None
    codigoOrgao: Optional[str] = None
    relator: Optional[str] = None
    ementa: Optional[str] = None
    decisao: Optional[str] = None
    observacao: Optional[str] = None
    tipoDecisao: Optional[str] = None
    resultadoJulgamento: Optional[str] = None
    valorCausa: Optional[str] = None
    grau: Optional[str] = None
    instancia: Optional[str] = None
    sistema: Optional[str] = None
    formato: Optional[str] = None
    citacao: Optional[str] = None


class JurisprudenciaResponse(BaseModel):
    total: int
    tribunal: str
    criterios: JurisprudenciaRequest
    processos: List[ProcessoJurisprudencia]


def _resolve_endpoint(tribunal: str) -> str:
    endpoint = TRIBUNAIS.get(tribunal)
    if endpoint:
        return endpoint
    return f"api_publica_{tribunal.lower()}"


def _formatar_citacao(tribunal: str, source: dict) -> str:
    classe = source.get("classe", {}).get("nome") or "Classe"
    numero = source.get("numeroProcesso") or "N/A"
    orgao = source.get("orgaoJulgador", {}).get("nome") or ""
    relator = (
        source.get("relator", {}).get("nome")
        if source.get("relator")
        else "N/A"
    )
    julgamento = source.get("dataJulgamento") or "N/A"
    publicacao = source.get("dataPublicacao") or "N/A"

    return (
        f"({tribunal}, {classe}, n.º {numero}, {orgao}, Rel. {relator}, "
        f"j. {julgamento}, publ. {publicacao})"
    )


def _build_query(params: JurisprudenciaRequest) -> dict:
    query_parts = []

    if params.termo_busca:
        query_parts.append(
            {
                "multi_match": {
                    "query": params.termo_busca,
                    "fields": ["txtEmenta", "txtDecisao", "txtObservacao"],
                }
            }
        )

    if params.numero_processo:
        query_parts.append({"term": {"numeroProcesso": params.numero_processo}})

    if params.classe_processual:
        query_parts.append(
            {
                "multi_match": {
                    "query": params.classe_processual,
                    "fields": ["classe.nome", "classe.codigo"],
                }
            }
        )

    return {
        "size": params.tamanho,
        "query": {
            "bool": {
                "must": query_parts if query_parts else [{"match_all": {}}]
            }
        },
        "sort": [{"dataJulgamento": {"order": "desc"}}],
    }


@app.post("/api/buscar_jurisprudencia_datajud", response_model=JurisprudenciaResponse)
async def buscar_jurisprudencia_datajud(payload: JurisprudenciaRequest):
    endpoint = _resolve_endpoint(payload.tribunal)

    if not DATAJUD_API_KEY:
        raise HTTPException(status_code=500, detail="DATAJUD_API_KEY não configurada")

    url = f"{DATAJUD_BASE_URL}/{endpoint}/_search"
    headers = {
        "Authorization": f"APIKey {DATAJUD_API_KEY}",
        "Content-Type": "application/json",
    }

    request_payload = _build_query(payload)

    try:
        response = requests.post(url, headers=headers, json=request_payload, timeout=30)
        response.raise_for_status()
        resultado = response.json()

        hits = resultado.get("hits", {}).get("hits", [])
        processos = []

        for hit in hits:
            source = hit.get("_source", {})
            assunto = None
            assuntos = source.get("assunto") or []
            if assuntos:
                assunto = assuntos[0].get("nome")

            processo = ProcessoJurisprudencia(
                id=hit.get("_id"),
                numeroProcesso=source.get("numeroProcesso"),
                tribunal=payload.tribunal,
                classe=source.get("classe", {}).get("nome"),
                codigoClasse=source.get("classe", {}).get("codigo"),
                assunto=assunto,
                dataAjuizamento=source.get("dataAjuizamento"),
                dataJulgamento=source.get("dataJulgamento"),
                dataPublicacao=source.get("dataPublicacao"),
                orgaoJulgador=source.get("orgaoJulgador", {}).get("nome"),
                codigoOrgao=source.get("orgaoJulgador", {}).get("codigo"),
                relator=(
                    source.get("relator", {}).get("nome")
                    if source.get("relator")
                    else None
                ),
                ementa=source.get("txtEmenta"),
                decisao=source.get("txtDecisao"),
                observacao=source.get("txtObservacao"),
                tipoDecisao=source.get("tipoDecisao"),
                resultadoJulgamento=source.get("resultadoJulgamento"),
                valorCausa=source.get("valorCausa"),
                grau=source.get("grau"),
                instancia=source.get("instancia"),
                sistema=source.get("sistema"),
                formato=(
                    source.get("formato", {}).get("nome")
                    if source.get("formato")
                    else None
                ),
                citacao=_formatar_citacao(payload.tribunal, source),
            )

            processos.append(processo)

        return JurisprudenciaResponse(
            total=resultado.get("hits", {}).get("total", {}).get("value", 0),
            tribunal=payload.tribunal,
            criterios=payload,
            processos=processos,
        )

    except requests.exceptions.HTTPError as exc:
        logger.exception("Erro HTTP ao consultar DataJud")
        detail = exc.response.text if exc.response is not None else str(exc)
        raise HTTPException(status_code=502, detail=f"Erro DataJud: {detail}") from exc
    except requests.exceptions.RequestException as exc:
        logger.exception("Erro de conexão ao consultar DataJud")
        raise HTTPException(status_code=502, detail="Falha ao conectar no DataJud") from exc


@app.get("/")
async def root():
    return {"status": "DataJud API Running", "version": APP_VERSION}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
