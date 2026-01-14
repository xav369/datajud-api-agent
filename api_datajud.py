# API DataJud CNJ - Backend para Agente OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional

app = FastAPI(title="DataJud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATAJUD_BASE_URL = "https://api-publica.datajud.cnj.jus.br"
DATAJUD_API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

TRIBUNAIS = {
    "TJSP": "api_publica_tjsp",
    "TJRJ": "api_publica_tjrj",
    "TJMG": "api_publica_tjmg",
}


@app.post("/api/buscar_jurisprudencia_datajud")
async def buscar_jurisprudencia_datajud(
    termo_busca: Optional[str] = None,
    tribunal: str = "TJSP",
    numero_processo: Optional[str] = None,
    classe_processual: Optional[str] = None,
    tamanho: int = 10
):
    endpoint = TRIBUNAIS.get(tribunal.upper())
    if not endpoint:
        raise HTTPException(status_code=400, detail="Tribunal não suportado")
    
    url = f"{DATAJUD_BASE_URL}/{endpoint}/_search"
    headers = {
        "Authorization": f"APIKey {DATAJUD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    query_parts = []
    if termo_busca:
        query_parts.append({
            "multi_match": {
                "query": termo_busca,
                "fields": ["txtEmenta", "txtDecisao"]
            }
        })
    
    if numero_processo:
        query_parts.append({"match": {"numeroProcesso": numero_processo}})
    
    payload = {
        "size": min(tamanho, 50),
        "query": {
            "bool": {
                "must": query_parts if query_parts else [{"match_all": {}}]
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        resultado = response.json()
        
        hits = resultado.get("hits", {}).get("hits", [])
        processos = [{
            "numeroProcesso": h.get("_source", {}).get("numeroProcesso"),
            "classe": h.get("_source", {}).get("classe", {}).get("nome"),
            "tribunal": tribunal
        } for h in hits]
        
        return {
            "total": resultado.get("hits", {}).get("total", {}).get("value", 0),
            "processos": processos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"status": "DataJud API Running", "version": "1.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
