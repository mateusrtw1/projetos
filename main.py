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
        st.error(f"❌ Erro ao salvar o catálogo de filmes: {str(e)}")
    try:
        with open("filmes.json", "w") as arquivo:
            json.dump(st.session_state.filmes, arquivo, indent=4)
    except Exception as e:
        st.error(f"❌ Erro ao salvar os filmes: {str(e)}")

    try:
        with open("generos.json", "w") as arquivo:
            json.dump(st.session_state.generos, arquivo, indent=4)
    except Exception as e:
        st.error(f"❌ Erro ao salvar o gênero do filme: {str(e)}")

carregar_dados()

st.title("🎥 Gestor de Coleção de Filmes")

if 'catalogo_filmes' not in st.session_state:
    carregar_dados()

tab1, tab2, tab3, tab4 = st.tabs(["🎬 Título do Filme", "📅 Ano de Lançamento", "🎭 Gênero do Filme", "⭐ Sua Nota para o Filme"])

with tab1:
    titulo = st.text_input("✏️ Digite o nome do filme:")

with tab2:
    ano = st.number_input("📆 Digite o ano de lançamento do filme:", min_value=1900, max_value=datetime.datetime.now().year)
    
with tab3:
    genero = st.selectbox("🎞️ Selecione o gênero do filme:", st.session_state.generos)

with tab4:
    nota = st.slider("⭐ Sua nota para o filme:", 0, 5, 3)

with st.sidebar:
    st.header("📚 Filmes Cadastrados")
    if st.session_state.catalogo_filmes:
        for filme, info in list(st.session_state.catalogo_filmes.items()):
            with st.expander(f"🎬 {filme}"):

            # Estados de edição para cada campo
                if f"edit_ano_{filme}" not in st.session_state:
                    st.session_state[f"edit_ano_{filme}"] = False
                if f"edit_genero_{filme}" not in st.session_state:
                    st.session_state[f"edit_genero_{filme}"] = False
                if f"edit_nota_{filme}" not in st.session_state:
                    st.session_state[f"edit_nota_{filme}"] = False

                # Ano
                if st.session_state[f"edit_ano_{filme}"]:
                    novo_ano = st.number_input("📅 Novo Ano:", value=info['ano'], key=f"novo_ano_{filme}", min_value=1900, max_value=datetime.datetime.now().year)
                    if st.button("💾 Salvar Ano", key=f"salvar_ano_{filme}"):
                        st.session_state.catalogo_filmes[filme]['ano'] = novo_ano
                        st.session_state.filmes[filme]['ano'] = novo_ano
                        salvar_dados()
                        st.session_state[f"edit_ano_{filme}"] = False
                        st.success(f"📅 Ano de '{filme}' atualizado!")
                else:
                    st.markdown(f"**📅 Ano:** {info['ano']}")
                    if st.button("✏️ Editar Ano", key=f"editar_ano_{filme}"):
                        st.session_state[f"edit_ano_{filme}"] = True

                # Gênero
                if st.session_state[f"edit_genero_{filme}"]:
                    novo_genero = st.selectbox("🎭 Novo Gênero:", st.session_state.generos, index=st.session_state.generos.index(info['genero']), key=f"novo_genero_{filme}")
                    if st.button("💾 Salvar Gênero", key=f"salvar_genero_{filme}"):
                        st.session_state.catalogo_filmes[filme]['genero'] = novo_genero
                        st.session_state.filmes[filme]['genero'] = novo_genero
                        salvar_dados()
                        st.session_state[f"edit_genero_{filme}"] = False
                        st.success(f"🎭 Gênero de '{filme}' atualizado!")
                else:
                    st.markdown(f"**🎭 Gênero:** {info['genero']}")
                    if st.button("✏️ Editar Gênero", key=f"editar_genero_{filme}"):
                        st.session_state[f"edit_genero_{filme}"] = True

                # Nota
                if st.session_state[f"edit_nota_{filme}"]:
                    nova_nota = st.slider("⭐ Nova Nota:", 0, 5, value=info['nota'], key=f"nova_nota_{filme}")
                    if st.button("💾 Salvar Nota", key=f"salvar_nota_{filme}"):
                        st.session_state.catalogo_filmes[filme]['nota'] = nova_nota
                        st.session_state.filmes[filme]['nota'] = nova_nota
                        salvar_dados()
                        st.session_state[f"edit_nota_{filme}"] = False
                        st.success(f"⭐ Nota de '{filme}' atualizada!")
                else:
                    st.markdown(f"**⭐ Nota:** {info['nota']}")
                    if st.button("✏️ Editar Nota", key=f"editar_nota_{filme}"):
                        st.session_state[f"edit_nota_{filme}"] = True

if st.button("💾 Salvar Filme"):
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
        st.success(f"🎉 Filme '{titulo}' adicionado com sucesso!")

    else:
        st.error("⚠️ Por favor, preencha todos os campos antes de salvar.")
