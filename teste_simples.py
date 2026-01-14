#!/usr/bin/env python3
"""
Teste Simples da API DataJud - Sem dependências do OpenAI
Execute: python teste_simples.py
"""

import requests
import json
from datetime import datetime

API_URL = "https://datajud-api-agent.onrender.com"

def testar_api():
    print("\n" + "="*80)
    print("🏥 TESTE DA API DATAJUD - Busca de Jurisprudência")
    print("="*80)
    
    # Teste 1: Health Check
    print("\n🔍 Teste 1: Verificando status da API...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Online: {data['status']}")
            print(f"   Versão: {data['version']}")
            print(f"   Timestamp: {data['timestamp']}")
        else:
            print(f"❌ Erro: Status {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Teste 2: Busca de Jurisprudência
    print("\n\n📜 Teste 2: Buscando jurisprudência sobre 'urgência' no TJSP...")
    print("-" * 80)
    
    try:
        payload = {
            "termo_busca": "urgencia",
            "tribunal": "TJSP",
            "tamanho": 2
        }
        
        print(f"\n📤 Enviando requisição: {json.dumps(payload, ensure_ascii=False)}")
        
        response = requests.post(
            f"{API_URL}/api/buscar_jurisprudencia_datajud",
            json=payload,
            timeout=60  # 60s timeout (cold start pode demorar)
        )
        
        if response.status_code == 200:
            resultado = response.json()
            
            print(f"\n✅ Busca realizada com sucesso!")
            print(f"\n📊 ESTATÍSTICAS:")
            print(f"   Total de resultados: {resultado.get('total', 0)}")
            print(f"   Termo buscado: {resultado.get('query', 'N/A')}")
            print(f"   Tribunal: {resultado.get('tribunal', 'N/A')}")
            
            resultados = resultado.get('resultados', [])
            
            if resultados:
                print(f"\n\n📄 RESULTADOS ENCONTRADOS:\n")
                print("=" * 80)
                
                for i, item in enumerate(resultados, 1):
                    print(f"\n📋 RESULTADO #{i}")
                    print("-" * 80)
                    print(f"🏛️  Tribunal: {item.get('tribunal', 'N/A')}")
                    print(f"📂 Classe: {item.get('classe', 'N/A')}")
                    print(f"🔢 Número: {item.get('numero', 'N/A')}")
                    
                    if item.get('órgão'):
                        print(f"🏛️  Órgão: {item.get('órgão')}")
                    
                    if item.get('relator'):
                        print(f"👨‍⚖️  Relator: {item.get('relator')}")
                    
                    if item.get('dataJulgamento'):
                        print(f"📅 Data Julgamento: {item.get('dataJulgamento')}")
                    
                    if item.get('dataPublicacao'):
                        print(f"📰 Data Publicação: {item.get('dataPublicacao')}")
                    
                    if item.get('ementa'):
                        ementa = item.get('ementa', '')[:300]  # Primeiros 300 caracteres
                        print(f"\n📝 Ementa (preview):")
                        print(f"   {ementa}...")
                    
                    if item.get('citacao'):
                        print(f"\n🔗 Citação: {item.get('citacao')}")
                    
                    print("=" * 80)
            else:
                print("\n⚠️  Nenhum resultado encontrado.")
        
        else:
            print(f"\n❌ Erro na busca: Status {response.status_code}")
            print(f"   Resposta: {response.text}")
    
    except requests.exceptions.Timeout:
        print("\n⏱️  Timeout! A API pode estar em cold start (primeira requisição).")
        print("   Aguarde 30-60 segundos e tente novamente.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    
    print("\n\n" + "="*80)
    print("🎉 TESTE CONCLUÍDO!")
    print("="*80)
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. Teste o agente completo: python demo_agente.py")
    print("   2. Configure OPENAI_API_KEY para usar o agente inteligente")
    print("   3. Acesse o playground: https://platform.openai.com/agent-builder")
    print("\n🔗 Links Úteis:")
    print("   API: https://datajud-api-agent.onrender.com")
    print("   GitHub: https://github.com/xav369/datajud-api-agent")
    print("   Docs DataJud: https://datajud.cnj.jus.br\n")

if __name__ == "__main__":
    testar_api()
