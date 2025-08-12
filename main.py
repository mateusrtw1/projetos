import streamlit as st
import datetime
import json

def carregar_dados():

    try:
        with open("catalogo_filmes.json", "r") as arquivo:
            st.session_state.catalogo_filmes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.catalogo_filmes = {}

    try:
        with open("filmes.json", "r") as arquivo:
            st.session_state.filmes = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.filmes = {}

    try:
        with open("generos.json", "r") as arquivo:
            st.session_state.generos = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.generos = [
            "Ação", "Comédia", "Drama", "Ficção Científica",
            "Romance", "Suspense", "Terror", "Animação", "Outro"
        ]

    if 'catalogo_filmes' not in st.session_state:
        carregar_dados()

def salvar_dados():
    try:
        with open("catalogo_filmes.json", "w") as arquivo:
            json.dump(st.session_state.catalogo_filmes, arquivo, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar o catálogo de filmes: {str(e)}")
    try:
        with open("filmes.json", "w") as arquivo:
            json.dump(st.session_state.filmes, arquivo, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar os filmes: {str(e)}")

    try:
        with open("generos.json", "w") as arquivo:
            json.dump(st.session_state.generos, arquivo, indent=4)
    except Exception as e:
        st.error(f"Erro ao salvar o gênero do filme: {str(e)}")

carregar_dados()

st.title("Gestor de Coleção de Filmes")

if 'catalogo_filmes' not in st.session_state:
    carregar_dados()

tab1, tab2, tab3, tab4 = st.tabs(["Titulo do Filme", "Ano de Lançamento", "Gênero do Filme", "Sua nota para o Filme"])

with tab1:
    titulo = st.text_input("Digite o nome do filme:")

with tab2:
    ano = st.number_input("Digite o ano de lançamento do filme:", min_value=1900, max_value=datetime.datetime.now().year)
    
with tab3:
    genero = st.selectbox("Selecione o gênero do filme:", st.session_state.generos)

with tab4:
    nota = st.slider("Sua nota para o filme:", 0, 5, 3)

with st.sidebar:
    st.header("Filmes Cadastrados")
    if st.session_state.catalogo_filmes:
        for filme, info in list(st.session_state.catalogo_filmes.items()):
            with st.expander(f"🎬 {filme}"):
                st.markdown(f"""
                **Ano:** {info['ano']}  
                **Gênero:** {info['genero']}  
                **Nota:** {info['nota']}  
                """)

                if st.button(f"Excluir '{filme}'", key=f"excluir_{filme}"):
                    st.session_state.catalogo_filmes.pop(filme)
                    st.session_state.filmes.pop(filme, None)
                    salvar_dados()
                    st.success(f"Filme '{filme}' excluído com sucesso!")
    else:
        st.write("Ainda não há nenhum filme cadastrado.")

if st.button("Salvar Filme"):
    if titulo and ano and genero and nota is not None:
        st.session_state.catalogo_filmes[titulo] = {
            "ano": ano,
            "genero": genero,
            "nota": nota
        }
        
        st.session_state.filmes[titulo] = {
            "ano": ano,
            "genero": genero,
            "nota": nota
        }

        salvar_dados()
        st.success(f"Filme '{titulo}' adicionado com sucesso!")

    else:
        st.error("Por favor, preencha todos os campos antes de salvar.")