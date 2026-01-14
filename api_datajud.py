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
        processos = []
        for h in hits:
            source = h.get("_source", {})
            
            # Extrair todos os campos disponíveis
            processo = {
                # Identificação
                "id": h.get("_id"),
                "numeroProcesso": source.get("numeroProcesso"),
                "tribunal": tribunal,
                
                # Classe e Assunto
                "classe": source.get("classe", {}).get("nome"),
                "codigoClasse": source.get("classe", {}).get("codigo"),
                "assunto": source.get("assunto", [{}])[0].get("nome") if source.get("assunto") else None,
                
                # Datas
                "dataAjuizamento": source.get("dataAjuizamento"),
                "dataJulgamento": source.get("dataJulgamento"),
                "dataPublicacao": source.get("dataPublicacao"),
                
                # Órgão julgador
                "orgaoJulgador": source.get("orgaoJulgador", {}).get("nome"),
                "codigoOrgao": source.get("orgaoJulgador", {}).get("codigo"),
                
                # Magistrados
                "relator": source.get("relator", {}).get("nome") if source.get("relator") else None,
                
                # Conteúdo
                "ementa": source.get("txtEmenta"),
                "decisao": source.get("txtDecisao"),
                "observacao": source.get("txtObservacao"),
                
                # Movimentações e decisao
                "tipoDecisao": source.get("tipoDecisao"),
                "resultadoJulgamento": source.get("resultadoJulgamento"),
                
                # Valor
                "valorCausa": source.get("valorCausa"),
                
                # Grau
                "grau": source.get("grau"),
                "instancia": source.get("instancia"),
                
                # Sistema de origem
                "sistema": source.get("sistema"),
                "formato": source.get("formato", {}).get("nome") if source.get("formato") else None,
                
                # Gerar citação formatada
                "citacao": f"({tribunal}, {source.get('classe', {}).get('nome', 'Classe')}, n.º {source.get('numeroProcesso', 'N/A')}, {source.get('orgaoJulgador', {}).get('nome', '')}, Rel. {source.get('relator', {}).get('nome', 'N/A') if source.get('relator') else 'N/A'}, j. {source.get('dataJulgamento', 'N/A')}, publ. {source.get('dataPublicacao', 'N/A')})"
            }
            
            processos.append(processo)        
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
