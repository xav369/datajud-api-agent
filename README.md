# 🏛️ DataJud API Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-Agent-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Sistema Completo de Busca Jurisprudencial com IA**

*Integração entre DataJud CNJ e OpenAI Agents para pesquisa inteligente de jurisprudências*

[Demonstração](#-demonstração) • [Instalação](#-instalação) • [Uso](#-uso) • [API](#-documentação-da-api) • [Deploy](#-deploy)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Documentação da API](#documentação-da-api)
- [Agente OpenAI](#agente-openai)
- [Deploy](#deploy)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Exemplos](#exemplos)
- [Licença](#licença)

---

## 🎯 Sobre o Projeto

O **DataJud API Agent** é uma solução completa que conecta a API pública do DataJud (CNJ - Conselho Nacional de Justiça) com agentes inteligentes da OpenAI. O sistema permite buscar jurisprudências de forma natural e conversacional, retornando resultados estruturados e prontos para uso.

### 💡 Problema Resolvido

Advogados e profissionais do direito frequentemente precisam:
- ✅ Buscar jurisprudências relevantes em múltiplos tribunais
- ✅ Extrair informações específicas de acórdãos
- ✅ Formatar citações segundo normas CNJ
- ✅ Analisar padrões em decisões judiciais

Este projeto **automatiza e simplifica** essas tarefas usando IA.

---

## 🏗️ Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Cliente   │───▶│  OpenAI      │───▶│  Backend   │
│ (Usuário)  │     │  Agent       │     │  FastAPI   │
└─────────────┘     └──────────────┘     └─────────────┘
                                        │
                                        ▼
                                 ┌─────────────┐
                                 │  DataJud   │
                                 │ API (CNJ)  │
                                 └─────────────┘
```

### 💻 Componentes

1. **Backend FastAPI** (`api_datajud.py`)
   - API RESTful para busca de jurisprudências
   - Integração com DataJud CNJ
   - CORS habilitado para integração
   - Deploy no Render.com (https://datajud-api-agent.onrender.com)

2. **Agente OpenAI**
   - Processamento de linguagem natural
   - Extração inteligente de informações
   - Formatação automática JSON
   - Widget personalizado "Ementa CNJ"

3. **Scripts de Demonstração**
   - `demo_agente.py`: Exemplo completo com SDK OpenAI
   - `teste_simples.py`: Testes sem dependências do SDK

---

## ✨ Funcionalidades

### Backend API

✅ **Busca por termo livre**: Pesquisa em ementas e decisões  
✅ **Filtro por tribunal**: TJSP, TJRJ, TJMG  
✅ **Busca por número de processo**: CNJ (20 dígitos)  
✅ **Filtro por classe processual**: Apelação, Agravo, etc.  
✅ **Limitação de resultados**: Até 50 resultados por consulta  
✅ **20+ campos estruturados**: Dados completos dos processos  

### Agente OpenAI

✅ **Linguagem natural**: Perguntas em português coloquial  
✅ **Análise inteligente**: Entende contexto jurídico  
✅ **Formatação automática**: JSON estruturado CNJ  
✅ **Citações formatadas**: Padrão ABNT/CNJ  
✅ **Exatamente 5 resultados**: Otimizado para análise  

---

## 🛠️ Tecnologias

### Backend

- **[Python 3.9+](https://www.python.org/)** - Linguagem principal
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Requests](https://requests.readthedocs.io/)** - Cliente HTTP

### Cloud & Deploy

- **[Render.com](https://render.com/)** - Hospedagem do backend
- **[DataJud CNJ](https://datajud.cnj.jus.br/)** - API de jurisprudências
- **[OpenAI Platform](https://platform.openai.com/)** - Agentes IA

### Ferramentas de Desenvolvimento

- **[GitHub](https://github.com/)** - Controle de versão
- **[VS Code](https://code.visualstudio.com/)** - Editor recomendado

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Conta OpenAI com API Key
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/xav369/datajud-api-agent.git
cd datajud-api-agent
```

2. **Crie um ambiente virtual** (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sua-chave-aqui
DATAJUD_API_KEY=sua-chave-datajud-aqui
```

---

## ⚙️ Configuração

### Backend (Local)

```bash
uvicorn api_datajud:app --reload
```

A API estará disponível em: `http://localhost:8000`

### Agente OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com/agent-builder)
2. Crie um novo Agent
3. Configure a função personalizada:

**Nome**: `buscar_jurisprudencia_datajud`

**URL da API**: `https://datajud-api-agent.onrender.com/api/buscar_jurisprudencia_datajud`

**Parâmetros**:
- `termo_busca` (string, opcional)
- `tribunal` (string, padrão: "TJSP")
- `numero_processo` (string, opcional)
- `classe_processual` (string, opcional)
- `tamanho` (integer, padrão: 10)

4. Cole as instruções do agente (veja seção [Agente OpenAI](#agente-openai))

---

## 📚 Uso

### Exemplo Básico - API Direta

```python
import requests

url = "https://datajud-api-agent.onrender.com/api/buscar_jurisprudencia_datajud"

data = {
    "termo_busca": "plano de saúde recusa cobertura",
    "tribunal": "TJSP",
    "tamanho": 5
}

response = requests.post(url, json=data)
print(response.json())
```

### Exemplo com OpenAI Agent (SDK)

Veja o arquivo `demo_agente.py` para exemplo completo.

```python
from openai import OpenAI

client = OpenAI(api_key="sua-chave")

response = client.agents.run(
    agent_id="seu-agent-id",
    input="Busque 5 jurisprudências do TJSP sobre plano de saúde"
)

print(response)
```

### Teste Simples

```bash
python teste_simples.py
```

---

## 📊 Documentação da API

### Endpoint Principal

**POST** `/api/buscar_jurisprudencia_datajud`

### Request Body

```json
{
  "termo_busca": "string (opcional)",
  "tribunal": "Sigla do tribunal (ex: TJSP, TJRJ, TJMG, STJ, STF, TST, TNU, TRT15, TRF3) (padrão: TJSP)",
  "numero_processo": "string (opcional)",
  "classe_processual": "string (opcional)",
  "tamanho": "integer (padrão: 10, máximo: 50)"
}
```

### Response

```json
{
  "total": 5,
  "tribunal": "TJSP",
  "criterios": {
    "termo_busca": "plano de saúde recusa cobertura",
    "tribunal": "TJSP",
    "numero_processo": null,
    "classe_processual": null,
    "tamanho": 5
  },
  "processos": [
    {
      "id": "identificador-unico",
      "numeroProcesso": "1001234-00.2023.8.26.0100",
      "tribunal": "TJSP",
      "classe": "Apelação Cível",
      "codigoClasse": "198",
      "assunto": "Planos de Saúde",
      "dataAjuizamento": "10.01.2023",
      "dataJulgamento": "11.09.2024",
      "dataPublicacao": "20.09.2024",
      "orgaoJulgador": "5ª Câmara de Direito Privado",
      "codigoOrgao": "5",
      "relator": "Des. João Silva",
      "ementa": "texto completo da ementa...",
      "decisao": "texto da decisão...",
      "observacao": "observações...",
      "tipoDecisao": "Acórdão",
      "resultadoJulgamento": "Não provido",
      "valorCausa": "50000.00",
      "grau": "2",
      "instancia": "Segunda Instância",
      "sistema": "PJE",
      "formato": "Eletrônico",
      "citacao": "(TJSP, Apelação Cível n.º 1001234-00.2023.8.26.0100, 5ª Câmara de Direito Privado, Rel. Des. João Silva, j. 11.09.2024, publ. 20.09.2024)"
    }
  ]
}
```

### Health Check

**GET** `/health`

**Response**: `{"status": "healthy", "version": "1.1.0", "timestamp": "2024-01-01T00:00:00Z"}`

---

## 🤖 Agente OpenAI

### Instruções Completas

O agente é configurado com as seguintes instruções detalhadas:

```
Assuma o papel de um advogado com mais de 25 anos de experiência, especializado na busca de jurisprudência nos seguintes tribunais: TJSP, TJRJ, STJ, STF, TRT15, TRT2, TST, TNU e TRF3.

Siga sempre o seguinte procedimento:

1. Compreenda detalhadamente a solicitação do usuário
2. Use SEMPRE a ferramenta buscar_jurisprudencia_datajud com parâmetro tamanho=5
3. Apresente os resultados SEMPRE no formato JSON específico do widget "Ementa CNJ"

## FORMATO DE RESPOSTA OBRIGATÓRIO

Você DEVE retornar os dados no seguinte formato JSON com TODOS OS CAMPOS DISPONÍVEIS:

[Cole aqui o JSON completo do arquivo api_datajud.py linhas 78-136]
```

### Configurações

- **Model**: `gpt-4o-mini`
- **Tools**: 
  - `buscar_jurisprudencia_datajud` (custom)
  - Web Search
- **Output Format**: Widget "Ementa CNJ"
- **Include Chat History**: Habilitado

---

## 🚀 Deploy

### Render.com (Backend)

O projeto já está configurado para deploy automático no Render.com:

1. **Fork este repositório**
2. **Crie uma conta no [Render.com](https://render.com/)**
3. **Crie um novo Web Service**
   - Connect Your Repository
   - Selecione este repositório
4. **Configure**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api_datajud:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
   - **Region**: Oregon (US West)
5. **Deploy!**

A URL será gerada automaticamente: `https://seu-servico.onrender.com`

### OpenAI Agent

1. Configure a função com a URL do seu deploy
2. Publique o agente
3. Use via SDK ou Chat Interface

---

## 📝 Estrutura do Projeto

```
datajud-api-agent/
├── .gitignore              # Arquivos ignorados pelo Git
├── README.md               # Este arquivo
├── requirements.txt        # Dependências Python
├── api_datajud.py          # Backend FastAPI principal
├── demo_agente.py          # Exemplo com OpenAI SDK
└── teste_simples.py        # Testes básicos
```

### Arquivos Principais

#### `api_datajud.py`
Backend FastAPI com:
- Endpoint POST para busca
- Integração DataJud CNJ
- Tratamento de erros
- CORS habilitado
- 20+ campos estruturados

#### `demo_agente.py`
Script de demonstração completo com:
- Configuração do cliente OpenAI
- Chamadas ao agente
- Tratamento de respostas
- Exemplos de uso

#### `teste_simples.py`
Testes sem SDK:
- Chamadas diretas à API
- Validação de respostas
- Exemplos de parâmetros

---

## 💡 Exemplos

### Exemplo 1: Busca por Termo

```python
data = {
    "termo_busca": "responsabilidade civil dano moral",
    "tribunal": "TJSP",
    "tamanho": 5
}
```

### Exemplo 2: Busca por Número de Processo

```python
data = {
    "numero_processo": "1001234-00.2023.8.26.0100",
    "tribunal": "TJSP"
}
```

### Exemplo 3: Linguagem Natural (Agente)

```
"Busque jurisprudências do TJSP dos últimos 2 anos sobre recusa de plano de saúde em cirurgias de urgência"
```

O agente automaticamente:
1. Identifica os parâmetros relevantes
2. Chama a API com `termo_busca="plano saúde recusa urgência"`
3. Retorna 5 resultados formatados em JSON

---

## 📊 Status do Projeto

✅ Backend FastAPI - **Funcional**  
✅ Integração DataJud CNJ - **Funcional**  
✅ Agente OpenAI - **Funcional**  
✅ Deploy Render.com - **Ativo**  
✅ Widget Ementa CNJ - **Configurado**  

### Próximas Melhorias

- [ ] Suporte a mais tribunais (TRF, TST, TRT)
- [ ] Cache de consultas frequentes
- [ ] Interface web frontend
- [ ] Autenticação API
- [ ] Análise estatística de decisões
- [ ] Export para PDF/Word

---

## 🔗 Links Úteis

- **Backend API**: https://datajud-api-agent.onrender.com
- **DataJud CNJ**: https://datajud.cnj.jus.br
- **OpenAI Platform**: https://platform.openai.com
- **Documentação FastAPI**: https://fastapi.tiangolo.com
- **Render.com**: https://render.com

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

---

## 👨‍💻 Autor

**Xavier Ferreira**  
📧 Email: arxavier.cojuris@gmail.com  
🔗 GitHub: [@xav369](https://github.com/xav369)  

---

## 🚀 Como Contribuir

Contribuições são sempre bem-vindas!

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## ⭐ Mostre seu apoio

Se este projeto foi útil para você, considere dar uma ⭐ no repositório!

---

## 📝 Changelog

### [1.0.0] - 2026-01-14

#### Adicionado
- ✅ Backend FastAPI com integração DataJud CNJ
- ✅ Agente OpenAI com widget personalizado
- ✅ 20+ campos estruturados nas respostas
- ✅ Scripts de demonstração e testes
- ✅ Deploy automático no Render.com
- ✅ Documentação completa

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade jurídica brasileira**

🏛️ **DataJud API Agent** 🤖

</div>
