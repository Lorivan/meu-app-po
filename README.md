# 🚀 Product Opportunity Analyzer (WMS/TMS & Portals)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Methodology-RICE--Adapted-green?style=for-the-badge)

## 📋 Sobre o Projeto
Esta ferramenta foi desenvolvida para apoiar o processo de **Product Discovery** em ecossistemas de Logística (WMS/TMS) e Portais de Atendimento. O objetivo é transformar solicitações brutas de clientes e consultores em decisões priorizadas, utilizando critérios objetivos que equilibram valor de negócio, escalabilidade e esforço técnico.

O aplicativo utiliza uma lógica matemática refinada para remover o viés emocional e garantir que o Roadmap foque no que é verdadeiramente estratégico.

## ✨ Funcionalidades Principais
- **Entrada Qualitativa:** Registro da dor do cliente, justificativa de negócio e comparativo de mercado.
- **Score RICE Adaptado:** Cálculo baseado em Escalabilidade, Alinhamento Estratégico, Impacto (Redução de Esforço) e Confiança.
- **Mapeamento de Esforço:** Conversão de complexidade técnica (Baixa, Média, Alta) em denominadores numéricos que penalizam o score de forma proporcional.
- **Multiplicadores de Negócio:** Ajuste dinâmico do score para contas estratégicas (Key Accounts) ou situações de risco iminente de cancelamento (Churn).
- **Veredito Inteligente:** Sugestão automática de encaminhamento (Prioridade Crítica, Válida ou Baixa).

## 🧮 Metodologia de Priorização
A fórmula de cálculo implementada no coração do software é:

$$Score = \left( \frac{Escalabilidade \times Alinhamento \times Impacto \times Confiança}{Esforço Técnico} \right) \times Multiplicadores$$

### Variáveis de Entrada:
| Variável | Escala | Descrição |
| :--- | :--- | :--- |
| **Escalabilidade** | 1 a 10 | O quanto a solução atende a toda a base de clientes (Generalista). |
| **Alinhamento** | 1 a 10 | O quanto a demanda segue a visão estratégica do Roadmap. |
| **Impacto** | 1 a 10 | Redução de esforço para o usuário ou ganho de eficiência. |
| **Confiança** | 0.5 a 1.0 | Nível de certeza sobre a demanda (Dados vs. Suposição). |
| **Esforço Técnico** | 1, 5, 10 | Complexidade de implementação (atua como divisor). |

### Fatores de Ajuste (Multiplicadores):
- **Perfil do Cliente:** Key Accounts recebem bônus de peso (ex: 1.5x).
- **Risco de Churn:** Demandas críticas para retenção recebem multiplicador de urgência (ex: 1.8x).

## 🚀 Como Instalar e Rodar

### 1. Requisitos
- Python 3.9 ou superior instalado.

### 2. Instalação
Clone o repositório e instale as dependências:
```bash
# Clone o projeto
git clone https://github.com/seu-usuario/analisador-discovery.git

# Acesse a pasta
cd analisador-discovery

# Instale as dependências
pip install -r requirements.txt