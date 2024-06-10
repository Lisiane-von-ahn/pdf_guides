import streamlit as st

my_var = "Projet Campus Numérique in the ALPS"

def module_python():
    st.header("Module Python")
    # contenu du module Python

def module_algo():
    st.header("Module Algo")
    # contenu du Module Algo

def module_poo():
    st.header("Module POO")
    # Coloque aqui o conteúdo específico do módulo POO

# Adicione funções para outros módulos conforme necessário

def main():
    st.header("HOME PAGE FORMATEUR")
    st.title("Formation Data Analyst")
    st.write(my_var)

    options = {
        'Python': module_python,
        'Algo': module_algo,
        'POO': module_poo,
        # Adicione outras funções de módulo conforme necessário
    }

    # Sélectionner le module dans la sidebar
    selected_module = st.sidebar.selectbox("Module", list(options.keys()))

    # Exécuter a função do módulo selecionado
    options[selected_module]()

    choix = st.sidebar.radio("SubMenu", ["Kit Apprenant", "Interation"])
    if choix == "Kit Apprenant":
        st.subheader("Voici le kit Apprenant")
    else:
        st.subheader("Voici l'interation du module")

if __name__ == '__main__':
    main()
