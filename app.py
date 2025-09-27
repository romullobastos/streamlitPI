# app.py

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Configurações da página
st.set_page_config(
    page_title="Análise de Clusters Policiais",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar matplotlib para funcionar bem na nuvem
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# --- Data Loading (Simulated) ---
# In a real-world scenario running standalone, you would load your data here
# from a file (e.g., CSV, database). Make sure the path is correct.
# Carregamento de dados otimizado para Streamlit Cloud
@st.cache_data
def load_data():
    """Carrega os dados do CSV com cache para melhor performance na nuvem"""
    try:
        df = pd.read_csv('df_streamlit.csv')
        # Otimizações para melhor performance
        if 'cluster' in df.columns:
            df['cluster'] = df['cluster'].astype(int)
        return df
    except FileNotFoundError:
        st.error("❌ Arquivo 'df_streamlit.csv' não encontrado!")
        st.error("Certifique-se de que o arquivo de dados está na mesma pasta do app.py.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        st.stop()

# Carregar dados
df_streamlit = load_data()

# Assuming df_streamlit is available in the environment from previous Colab steps
# If running this script independently, uncomment and adapt the data loading above.

# --- Data Loading Complete ---
# The df_streamlit dataframe is now loaded from the CSV file


# Check if df_streamlit exists after potential loading/placeholder creation
if df_streamlit is None or df_streamlit.empty:
    st.error("Não foi possível carregar ou criar o DataFrame 'df_streamlit'. O aplicativo não pode continuar.")
    st.stop()

# --- Título e Introdução ---
st.title("🚔 Análise de Clusters e Status de Investigações Policiais")

# Indicador de dados carregados
st.success(f"✅ Dados carregados com sucesso! {len(df_streamlit):,} ocorrências analisadas")

st.markdown("""
Este aplicativo explora a relação entre os clusters de ocorrências policiais
identificados através de análise de agrupamento (K-Means) e o status final
das investigações ('Arquivado' ou 'Concluído').

**🔍 Funcionalidades:**
- 📊 Análise visual de clusters
- 📈 Gráficos interativos
- 🔍 Análise detalhada por cluster
- 📋 Comparações estatísticas

Utilize a barra lateral para selecionar clusters e visualizar as características
dominantes de cada grupo, bem como a taxa de conclusão das investigações dentro deles.
""")

# --- Seção 1: Visão Geral dos Clusters e Status ---
st.subheader("Visão Geral dos Clusters")

# Adicionar gráfico de pizza para distribuição de clusters
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Gráfico de pizza para distribuição de clusters
cluster_counts = df_streamlit['cluster'].value_counts().sort_index()
ax1.pie(cluster_counts.values, labels=[f'Cluster {i}' for i in cluster_counts.index], autopct='%1.1f%%', startangle=90)
ax1.set_title('Distribuição de Ocorrências por Cluster')

# Gráfico de barras para status de investigação
status_counts = df_streamlit['status_investigacao'].value_counts()
ax2.bar(status_counts.index, status_counts.values, color=['#ff7f7f', '#7fbf7f'])
ax2.set_title('Distribuição de Status de Investigação')
ax2.set_ylabel('Número de Ocorrências')
plt.xticks(rotation=45)

st.pyplot(fig)
plt.close()

total_ocorrencias = len(df_streamlit)
num_clusters = df_streamlit['cluster'].nunique()

st.write(f"Total de ocorrências analisadas: {total_ocorrencias}")
st.write(f"Número de clusters identificados: {num_clusters}")

cluster_counts = df_streamlit['cluster'].value_counts().sort_index()
st.write("\nDistribuição de ocorrências por cluster:")
st.dataframe(cluster_counts)
# Add a bar chart for cluster counts
st.bar_chart(cluster_counts)

st.subheader("Status de Investigação por Cluster (Arquivado/Concluído)")

# Ensure only Arquivado and Concluído are considered for this specific analysis section
df_filtered_status = df_streamlit[df_streamlit['status_investigacao'].isin(['Arquivado', 'Concluído'])].copy()

if not df_filtered_status.empty:
    cluster_status_proportion = pd.crosstab(df_filtered_status['cluster'],
                                            df_filtered_status['status_investigacao'],
                                            normalize='index') * 100

    st.write("Distribuição percentual do Status de Investigação por Cluster (%):")
    st.dataframe(cluster_status_proportion.round(2))
    # Add a stacked bar chart for status distribution
    st.bar_chart(cluster_status_proportion)

    if 'Concluído' in cluster_status_proportion.columns:
        completion_rate_by_cluster = cluster_status_proportion['Concluído']
        st.write("\nTaxa de Conclusão das Investigações por Cluster (%):")
        st.dataframe(completion_rate_by_cluster.round(2))
        # Add a bar chart for completion rate
        st.bar_chart(completion_rate_by_cluster)
    else:
        st.write("\nNão há ocorrências 'Concluído' para calcular a taxa de conclusão.")

else:
    st.warning("Não há ocorrências com status 'Arquivado' ou 'Concluído' para análise de status por cluster.")


# --- Seção 2: Análise Detalhada por Cluster com Foco no Status ---
st.subheader("Análise Detalhada por Cluster")

# Add cluster selector to the sidebar
st.sidebar.header("Explorar Cluster Específico")
selected_cluster = st.sidebar.selectbox(
    "Selecione um Cluster para Análise Detalhada:",
    options=sorted(df_streamlit['cluster'].unique())
)

# Filter data for the selected cluster
df_selected_cluster = df_streamlit[df_streamlit['cluster'] == selected_cluster].copy()

st.write(f"### Cluster {selected_cluster}")
st.write(f"Número de ocorrências neste cluster: {len(df_selected_cluster)}")

# Gráfico de análise do cluster selecionado
if len(df_selected_cluster) > 0:
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico 1: Distribuição de tipos de crime
    tipo_crime_counts = df_selected_cluster['tipo_crime'].value_counts()
    ax1.pie(tipo_crime_counts.values, labels=tipo_crime_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title(f'Tipos de Crime - Cluster {selected_cluster}')
    
    # Gráfico 2: Distribuição de bairros
    bairro_counts = df_selected_cluster['bairro'].value_counts().head(10)  # Top 10 bairros
    ax2.barh(range(len(bairro_counts)), bairro_counts.values)
    ax2.set_yticks(range(len(bairro_counts)))
    ax2.set_yticklabels(bairro_counts.index)
    ax2.set_title(f'Top 10 Bairros - Cluster {selected_cluster}')
    ax2.set_xlabel('Número de Ocorrências')
    
    # Gráfico 3: Distribuição de idade dos suspeitos
    if 'idade_suspeito' in df_selected_cluster.columns:
        ax3.hist(df_selected_cluster['idade_suspeito'].dropna(), bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax3.set_title(f'Distribuição de Idade dos Suspeitos - Cluster {selected_cluster}')
        ax3.set_xlabel('Idade')
        ax3.set_ylabel('Frequência')
    
    # Gráfico 4: Status de investigação
    status_counts = df_selected_cluster['status_investigacao'].value_counts()
    colors = ['#ff7f7f', '#7fbf7f', '#7f7fff'][:len(status_counts)]
    ax4.bar(status_counts.index, status_counts.values, color=colors)
    ax4.set_title(f'Status de Investigação - Cluster {selected_cluster}')
    ax4.set_ylabel('Número de Ocorrências')
    plt.setp(ax4.get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Display numerical characteristics
st.write("\nCaracterísticas médias (numéricas):")
numeric_vars = ['quantidade_vitimas', 'quantidade_suspeitos', 'idade_suspeito']
# Ensure numerical columns exist in the selected cluster's dataframe
numeric_vars_present = [col for col in numeric_vars if col in df_selected_cluster.columns]
if numeric_vars_present:
    st.dataframe(df_selected_cluster[numeric_vars_present].mean().round(2))
else:
    st.write("Variáveis numéricas não disponíveis neste cluster.")


# Display dominant categorical characteristics
st.write("\nCaracterísticas dominantes (categóricas):")
categorical_vars = ['tipo_crime', 'bairro', 'descricao_modus_operandi', 'arma_utilizada']
categorical_vars_present = [col for col in categorical_vars if col in df_selected_cluster.columns]
if categorical_vars_present:
    for var in categorical_vars_present:
        if not df_selected_cluster[var].empty:
            mode_counts = df_selected_cluster[var].value_counts(normalize=True)
            if not mode_counts.empty:
                 mode_val = mode_counts.index[0]
                 mode_proportion = mode_counts.max() * 100
                 st.write(f"- **{var}**: {mode_val} ({mode_proportion:.1f}%)")
            else:
                 st.write(f"- **{var}**: Não aplicável (sem dados ou valores únicos)")
        else:
            st.write(f"- **{var}**: Não aplicável (dataframe vazio para esta coluna)")
else:
    st.write("Variáveis categóricas não disponíveis neste cluster.")


# Display status distribution within the selected cluster (all statuses)
st.write(f"\nDistribuição do Status de Investigação no Cluster {selected_cluster}:")
status_distribution_selected = df_selected_cluster['status_investigacao'].value_counts(normalize=True) * 100
st.dataframe(status_distribution_selected.round(2))
# Add a bar chart
st.bar_chart(status_distribution_selected)


# Compare characteristics between Arquivadas vs Concluídas within the cluster
st.write(f"\nComparação entre Status de Investigação (Arquivado vs Concluído) no Cluster {selected_cluster}:")

# Filter data within the selected cluster by status (only Arquivado and Concluído)
df_selected_arquivado = df_selected_cluster[df_selected_cluster['status_investigacao'] == 'Arquivado']
df_selected_concluido = df_selected_cluster[df_selected_cluster['status_investigacao'] == 'Concluído']

if not df_selected_arquivado.empty or not df_selected_concluido.empty:
     if not df_selected_arquivado.empty and not df_selected_concluido.empty:
        # Compare numerical variables
        st.write("Médias das variáveis numéricas:")
        numeric_comparison = pd.DataFrame({
            'Arquivado': df_selected_arquivado[numeric_vars_present].mean().round(2),
            'Concluído': df_selected_concluido[numeric_vars_present].mean().round(2)
        })
        st.dataframe(numeric_comparison)

        # Compare dominant categorical variables (Top 3 for each status)
        st.write("\nCategorias dominantes (Top 3) por Status:")
        for var in categorical_vars_present:
            st.write(f"- **{var.upper()}**:")
            arquivado_top3 = df_selected_arquivado[var].value_counts(normalize=True).head(3) * 100
            concluido_top3 = df_selected_concluido[var].value_counts(normalize=True).head(3) * 100

            comparison_df = pd.DataFrame({'Arquivado (%)': arquivado_top3, 'Concluído (%)': concluido_top3}).fillna(0).round(1)
            st.dataframe(comparison_df)
     elif not df_selected_arquivado.empty:
         st.write("Apenas ocorrências 'Arquivadas' neste cluster:")
         st.dataframe(df_selected_arquivado[numeric_vars_present].mean().round(2))
         for var in categorical_vars_present:
             if not df_selected_arquivado[var].empty:
                 st.write(f"- **{var.upper()} (Arquivado)**:")
                 arquivado_top3 = df_selected_arquivado[var].value_counts(normalize=True).head(3) * 100
                 st.dataframe(arquivado_top3.round(1))
     elif not df_selected_concluido.empty:
         st.write("Apenas ocorrências 'Concluídas' neste cluster:")
         st.dataframe(df_selected_concluido[numeric_vars_present].mean().round(2))
         for var in categorical_vars_present:
             if not df_selected_concluido[var].empty:
                 st.write(f"- **{var.upper()} (Concluído)**:")
                 concluido_top3 = df_selected_concluido[var].value_counts(normalize=True).head(3) * 100
                 st.dataframe(concluido_top3.round(1))

else:
    st.write("Não há ocorrências 'Arquivado' ou 'Concluído' neste cluster para comparação detalhada.")


# --- Seção 3: Comparação Geral de Status ---
st.subheader("Comparação Geral de Características por Status de Investigação")

# Gráfico de comparação geral com heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Heatmap de correlação entre variáveis numéricas
numeric_columns = ['quantidade_vitimas', 'quantidade_suspeitos', 'idade_suspeito']
if all(col in df_streamlit.columns for col in numeric_columns):
    correlation_matrix = df_streamlit[numeric_columns].corr()
    im = ax1.imshow(correlation_matrix, cmap='coolwarm', aspect='auto')
    ax1.set_xticks(range(len(numeric_columns)))
    ax1.set_yticks(range(len(numeric_columns)))
    ax1.set_xticklabels(numeric_columns, rotation=45)
    ax1.set_yticklabels(numeric_columns)
    ax1.set_title('Correlação entre Variáveis Numéricas')
    
    # Adicionar valores na matriz
    for i in range(len(numeric_columns)):
        for j in range(len(numeric_columns)):
            text = ax1.text(j, i, f'{correlation_matrix.iloc[i, j]:.2f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    plt.colorbar(im, ax=ax1)

# Gráfico 2: Comparação de status por cluster
cluster_status_crosstab = pd.crosstab(df_streamlit['cluster'], df_streamlit['status_investigacao'])
cluster_status_crosstab.plot(kind='bar', ax=ax2, stacked=True, color=['#ff7f7f', '#7fbf7f'])
ax2.set_title('Distribuição de Status por Cluster')
ax2.set_xlabel('Cluster')
ax2.set_ylabel('Número de Ocorrências')
ax2.legend(title='Status')
plt.setp(ax2.get_xticklabels(), rotation=0)

plt.tight_layout()
st.pyplot(fig)
plt.close()

# Create dataframes for Arquivado and Concluído from the main filtered data
df_arquivado_geral = df_streamlit[df_streamlit['status_investigacao'] == 'Arquivado'].copy()
df_concluido_geral = df_streamlit[df_streamlit['status_investigacao'] == 'Concluído'].copy()

st.write(f"Análise de {len(df_arquivado_geral)} ocorrências 'Arquivadas' e {len(df_concluido_geral)} ocorrências 'Concluídas' (todos os clusters combinados).")

# Calculate and display mean of numerical variables
if not df_arquivado_geral.empty or not df_concluido_geral.empty:
    st.write("\nMédias das variáveis numéricas (Geral):")
    numeric_comparison_geral = pd.DataFrame({
        'Arquivado': df_arquivado_geral[numeric_vars_present].mean().round(2) if not df_arquivado_geral.empty else pd.Series(dtype='float64'),
        'Concluído': df_concluido_geral[numeric_vars_present].mean().round(2) if not df_concluido_geral.empty else pd.Series(dtype='float64')
    })
    st.dataframe(numeric_comparison_geral)

    # Calculate and display top 3 categorical variables
    st.write("\nCategorias dominantes (Top 3) por Status (Geral):")
    for var in categorical_vars_present:
        st.write(f"- **{var.upper()}**:")
        arquivado_top3_geral = df_arquivado_geral[var].value_counts(normalize=True).head(3) * 100 if not df_arquivado_geral.empty else pd.Series(dtype='float64')
        concluido_top3_geral = df_concluido_geral[var].value_counts(normalize=True).head(3) * 100 if not df_concluido_geral.empty else pd.Series(dtype='float64')

        comparison_df_geral = pd.DataFrame({'Arquivado (%)': arquivado_top3_geral, 'Concluído (%)': concluido_top3_geral}).fillna(0).round(1)
        st.dataframe(comparison_df_geral)
else:
     st.write("Não há ocorrências 'Arquivado' ou 'Concluído' no dataset geral para comparação.")


# --- Informações do Projeto ---
st.sidebar.subheader("📊 Estatísticas do Dataset")
st.sidebar.metric("Total de Ocorrências", f"{len(df_streamlit):,}")
st.sidebar.metric("Número de Clusters", df_streamlit['cluster'].nunique())
st.sidebar.metric("Tipos de Crime", df_streamlit['tipo_crime'].nunique())

# --- Como Rodar o Aplicativo ---
st.sidebar.subheader("🚀 Como Rodar Localmente")
st.sidebar.markdown("""
1. Clone o repositório
2. `pip install -r requirements.txt`
3. `streamlit run app.py`
4. Acesse `http://localhost:8501`
""")

# --- Deploy no Streamlit Cloud ---
st.sidebar.subheader("☁️ Deploy no Streamlit Cloud")
st.sidebar.markdown("""
**✅ Projeto Pronto para Deploy!**

1. 📤 Faça upload para GitHub
2. 🌐 Acesse [share.streamlit.io](https://share.streamlit.io)
3. 🔗 Conecte seu repositório
4. 🚀 Deploy automático!

**Arquivos incluídos:**
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `df_streamlit.csv`
- ✅ `README.md`
""")


# --- Finish task ---
# Although this is a Streamlit app file and not a Colab task to "finish",
# this marks the end of generating the app code based on the plan.