import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Função para identificar os temas em cada post e contar as palavras-chave
def identify_theme(content, keywords):
    themes = []
    keyword_count = {}
    content_lower = content.lower()
    
    for theme, words in keywords.items():
        for word in words:
            if word.lower() in content_lower:
                themes.append(theme)
                if word in keyword_count:
                    keyword_count[word] += 1
                else:
                    keyword_count[word] = 1
                
    return ', '.join(themes) if themes else 'None', keyword_count

# Função principal do aplicativo Streamlit
def main():
    st.title("Análise de Temas em Posts do Twitter")

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Dados carregados com sucesso!")
        st.dataframe(df.head())

        # Temas e palavras-chave predefinidos
        predefined_keywords = {
            'AMAZONIA': ['Amazônia'],
            'Meio Ambiente': ['Meio Ambiente', 'Sustentabilidade', 'ONGs', 'Movimentos Sociais'],
            'Territórios': ['Índios', 'indígenas', 'conflitos de terra', 'demarcação de terras', 'povos da floresta', 'queimadas', 'comunidades tradicionais'],
            'Soberania': ['Soberania', 'Emmanuel Macron'],
            'Diplomacia': ['Diplomacia', 'França', 'Emmanuel Macron', 'Relações Externas']
        }

        # Seleção dos temas
        selected_themes = st.multiselect(
            "Selecione os temas que deseja analisar:",
            options=list(predefined_keywords.keys())
        )

        # Input de palavras-chave personalizadas
        custom_theme_name = st.text_input("Nome do Tema Personalizado (opcional)")
        custom_theme_keywords = st.text_input("Palavras-chave para o Tema Personalizado (separadas por vírgula)")

        # Construir o dicionário de palavras-chave
        keywords = {theme: predefined_keywords[theme] for theme in selected_themes}
        if custom_theme_name and custom_theme_keywords:
            keywords[custom_theme_name] = [kw.strip() for kw in custom_theme_keywords.split(',')]

        if st.button("Analisar"):
            # Inicializar dicionário para contagem de palavras-chave
            overall_keyword_count = {}

            # Identificar os temas e contar palavras-chave
            df['Themes'], df['Keyword Count'] = zip(*df['content'].apply(lambda x: identify_theme(x, keywords)))

            # Atualizar o dicionário geral de contagem de palavras-chave
            for count_dict in df['Keyword Count']:
                for key, value in count_dict.items():
                    if key in overall_keyword_count:
                        overall_keyword_count[key] += value
                    else:
                        overall_keyword_count[key] = value

            # Filtrar e salvar os posts por tema
            for theme in keywords.keys():
                filtered_df = df[df['Themes'].str.contains(theme)]
                st.write(f"Posts filtrados para o tema: {theme}")
                st.dataframe(filtered_df.head())
                st.download_button(
                    label=f"Baixar CSV do tema {theme}",
                    data=filtered_df.to_csv(index=False).encode('utf-8'),
                    file_name=f'Twitter_posts_{theme}.csv',
                    mime='text/csv',
                )

            # Filtrar e salvar os posts com mais de um tema
            multi_theme_df = df[df['Themes'].str.contains(', ')]
            st.write("Posts com múltiplos temas:")
            st.dataframe(multi_theme_df.head())
            st.download_button(
                label="Baixar CSV de posts com múltiplos temas",
                data=multi_theme_df.to_csv(index=False).encode('utf-8'),
                file_name='Twitter_posts_multi_themes.csv',
                mime='text/csv',
            )

            # Exibir resumo das palavras-chave
            st.write("Resumo das Palavras-chave Encontradas:")
            keyword_summary = pd.DataFrame.from_dict(overall_keyword_count, orient='index', columns=['Frequência'])
            st.dataframe(keyword_summary)

            # Gerar gráfico de barras
            st.write("Gráfico de Frequência das Palavras-chave:")
            keyword_summary.plot(kind='bar', figsize=(10, 6))
            plt.title('Frequência das Palavras-chave')
            plt.xlabel('Palavras-chave')
            plt.ylabel('Frequência')
            st.pyplot(plt)

if __name__ == "__main__":
    main()
