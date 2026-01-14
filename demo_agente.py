#!/usr/bin/env python3
"""
Demonstração do Agente de Busca Jurisprudencial
Integração completa: OpenAI Agent Builder + API DataJud CNJ
"""

import os
import asyncio
import json
import requests
from agents import function_tool, Agent, Runner, RunConfig
from pydantic import BaseModel

# URL da API DataJud deployada no Render
API_DATAJUD_URL = "https://datajud-api-agent.onrender.com"

# ======================
# FERRAMENTA DE BUSCA
# ======================

class BuscarJurisprudenciaParams(BaseModel):
    termo_busca: str
    tribunal: str = "TJSP"
    tamanho: int = 3

@function_tool
def buscar_jurisprudencia_datajud(termo_busca: str, tribunal: str = "TJSP", tamanho: int = 3) -> str:
    """
    Busca jurisprudência e processos judiciais na base DataJud do CNJ.
    
    Args:
        termo_busca: Termo para buscar (ex: 'urgência', 'plano de saúde')
        tribunal: Sigla do tribunal (ex: TJSP, STJ, TRT2)
        tamanho: Número de resultados (1-10)
    
    Returns:
        JSON com resultados da busca
    """
    try:
        print(f"\n🔍 Buscando: '{termo_busca}' no {tribunal}...")
        
        response = requests.post(
            f"{API_DATAJUD_URL}/api/buscar_jurisprudencia_datajud",
            json={
                "termo_busca": termo_busca,
                "tribunal": tribunal,
                "tamanho": tamanho
            },
            timeout=30
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"✅ Encontrados {resultado.get('total', 0)} resultados")
            return json.dumps(resultado, ensure_ascii=False)
        else:
            erro = f"Erro na API: {response.status_code}"
            print(f"❌ {erro}")
            return json.dumps({"erro": erro})
    
    except Exception as e:
        erro = f"Erro ao buscar: {str(e)}"
        print(f"❌ {erro}")
        return json.dumps({"erro": erro})

# ======================
# CONFIGURAÇÃO DO AGENTE
# ======================

agente = Agent(
    name="Agente de Busca Jurisprudencial",
    instructions="""
Você é um assistente jurídico especializado em pesquisa de jurisprudência.

SEMPRE siga este procedimento:

1. Compreenda a solicitação do usuário
2. Use a ferramenta buscar_jurisprudencia_datajud para buscar
3. Apresente os resultados de forma clara e organizada

FORMATO DE RESPOSTA:
- Mostre o tribunal e número do processo
- Resuma a decisão de forma clara
- Cite datas importantes
- Use formatação clara e profissional

IMPORTANTE: Sempre retorne resultados em formato legível, não apenas JSON bruto.
""",
    tools=[buscar_jurisprudencia_datajud],
    model="gpt-4o-mini"
)

# ======================
# FUNÇÃO PRINCIPAL
# ======================

async def executar_consulta(pergunta: str):
    """
    Executa uma consulta usando o agente
    """
    print("\n" + "="*80)
    print("🤖 AGENTE DE BUSCA JURISPRUDENCIAL - DataJud CNJ")
    print("="*80)
    print(f"\n📝 Pergunta: {pergunta}\n")
    
    resultado = await Runner.arun(
        agente,
        input=pergunta,
        run_config=RunConfig(
            trace_metadata={
                "_trace_source_": "demo-script"
            }
        )
    )
    
    print("\n" + "-"*80)
    print("💬 RESPOSTA DO AGENTE:")
    print("-"*80)
    print(resultado.output_text)
    print("\n" + "="*80 + "\n")
    
    return resultado

# ======================
# EXEMPLOS DE USO
# ======================

async def main():
    """
    Demonstrações de consultas
    """
    
    # Exemplo 1: Busca sobre urgência médica
    await executar_consulta(
        "Busque jurisprudência sobre urgência médica e planos de saúde no TJSP"
    )
    
    # Aguarda um pouco entre consultas
    await asyncio.sleep(2)
    
    # Exemplo 2: Busca sobre contratos
    await executar_consulta(
        "Encontre 2 decisões sobre rescisão de contratos no STJ"
    )
    
    print("\n✅ Demonstração completa!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   - Configure OPENAI_API_KEY como variável de ambiente")
    print("   - Instale: pip install openai-agents-sdk requests")
    print("   - Execute: python demo_agente.py")
    print("\n📚 API Backend: https://datajud-api-agent.onrender.com")
    print("🔗 GitHub: https://github.com/xav369/datajud-api-agent\n")

if __name__ == "__main__":
    # Verifica se a API Key está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  ATENÇÃO: Configure OPENAI_API_KEY como variável de ambiente")
        print("   export OPENAI_API_KEY='sua-chave-aqui'\n")
        exit(1)
    
    asyncio.run(main())
