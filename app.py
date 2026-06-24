"""
Main Streamlit application for the steganography project.
Coffre-fort Numérique - Stéganographie et Cryptographie d'Images
"""

import streamlit as st
from views import home, encode, decode, analyze


# Page configuration
st.set_page_config(
    page_title="Coffre-fort Numérique",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #2E86AB;
    }
    h2 {
        color: #A23B72;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Sidebar navigation
    st.sidebar.title("🔐 Navigation")
    st.sidebar.markdown("---")
    
    # Page selection
    pages = {
        "🏠 Accueil": home,
        "🖼️ Encoder": encode,
        "🔓 Décoder": decode,
        "📊 Analyser": analyze
    }
    
    # Radio buttons for page selection
    selected_page = st.sidebar.radio(
        "Choisir une page",
        list(pages.keys()),
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Information in sidebar
    st.sidebar.markdown("### ℹ️ À propos")
    st.sidebar.info("""
    **Coffre-fort Numérique**
    
    Application de stéganographie utilisant :
    - 🔒 Chiffrement AES
    - 🎨 Technique LSB
    - 📊 Métriques MSE/PSNR
    
    Cachez vos messages secrets dans des images de manière invisible !
    """)
    
    st.sidebar.markdown("---")
    
    # Quick tips
    with st.sidebar.expander("💡 Conseils rapides"):
        st.markdown("""
        1. Utilisez des images **PNG** pour de meilleurs résultats
        2. Choisissez un **mot de passe fort**
        3. Vérifiez le **PSNR** (> 30 dB = invisible)
        4. Sauvegardez l'image encodée en **PNG**
        """)
    
    # Workflow guide
    with st.sidebar.expander("🚀 Guide d'utilisation"):
        st.markdown("""
        **Workflow recommandé** :
        
        1. **Analyser** votre image pour connaître sa capacité
        2. **Encoder** votre message dans l'image
        3. Vérifier les métriques de qualité
        4. **Décoder** pour tester que tout fonctionne
        """)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Projet Python - Stéganographie LSB")
    
    # Render selected page
    pages[selected_page].render()


if __name__ == "__main__":
    main()
