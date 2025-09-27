# Análise de Clusters e Status de Investigações Policiais

Este aplicativo Streamlit analisa a relação entre clusters de ocorrências policiais identificados através de análise de agrupamento (K-Means) e o status final das investigações ('Arquivado' ou 'Concluído').

## 🚀 Funcionalidades

- **Análise de Clusters**: Visualização da distribuição de ocorrências por cluster
- **Status de Investigação**: Análise detalhada do status das investigações
- **Análise Interativa**: Seletor de clusters para análise específica
- **Visualizações Gráficas**: Gráficos de pizza, barras, histogramas e heatmaps
- **Comparações**: Análise comparativa entre diferentes status de investigação

## 📊 Dados

O aplicativo utiliza dados de ocorrências policiais com as seguintes características:
- Tipos de crime
- Localização (bairros)
- Modus operandi
- Armas utilizadas
- Quantidade de vítimas e suspeitos
- Idade dos suspeitos
- Status da investigação
- Clusters identificados

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Interface web interativa
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica
- **Matplotlib**: Visualizações gráficas
- **Seaborn**: Visualizações estatísticas avançadas

## 📁 Estrutura do Projeto

```
streamlitPI/
├── app.py                    # Aplicação principal
├── df_streamlit.csv         # Dataset de ocorrências
├── requirements.txt         # Dependências do projeto
└── README.md               # Este arquivo
```

## 🚀 Como Executar Localmente

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd streamlitPI
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
streamlit run app.py
```

4. Acesse no navegador: `http://localhost:8501`

## ☁️ Deploy no Streamlit Cloud

Este projeto está configurado para deploy automático no Streamlit Cloud:

1. **Faça upload do projeto para o GitHub**
2. **Acesse [share.streamlit.io](https://share.streamlit.io)**
3. **Conecte seu repositório GitHub**
4. **O deploy será automático!**

### Requisitos para Deploy:
- ✅ Arquivo `app.py` na raiz do repositório
- ✅ Arquivo `df_streamlit.csv` com os dados
- ✅ Arquivo `requirements.txt` com dependências
- ✅ Repositório público no GitHub

## 📈 Análises Disponíveis

### Visão Geral
- Distribuição de ocorrências por cluster
- Status de investigação geral
- Gráficos de pizza e barras interativos

### Análise por Cluster
- Características médias numéricas
- Características dominantes categóricas
- Distribuição de status por cluster
- Comparação entre status de investigação

### Visualizações Avançadas
- Heatmap de correlação entre variáveis
- Gráficos de barras empilhadas
- Histogramas de distribuição
- Gráficos de barras horizontais

## 🔧 Configuração

O aplicativo carrega automaticamente os dados do arquivo `df_streamlit.csv`. Certifique-se de que o arquivo está na mesma pasta do `app.py`.

## 📝 Licença

Este projeto é de uso acadêmico/educacional.

## 👥 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Adicionar novas funcionalidades
