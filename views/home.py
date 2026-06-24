"""
Home page - Introduction to the steganography application.
"""

import streamlit as st


def render():
    """Render the home page."""
    st.title("🔐 Coffre-fort Numérique")
    st.subheader("Stéganographie et Cryptographie d'Images")
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ## 👋 Bienvenue
    
    Cette application vous permet de **cacher des messages secrets** dans des images de manière invisible,
    en utilisant la technique de **stéganographie LSB** (Least Significant Bit) combinée au 
    **chiffrement AES** pour une sécurité maximale.
    """)
    
    # How it works
    st.markdown("---")
    st.markdown("## 🔍 Comment ça fonctionne ?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📝 Stéganographie LSB
        
        La technique LSB modifie les **bits de poids faible** de chaque pixel de l'image 
        pour y insérer votre message. Ces modifications sont **invisibles à l'œil nu** !
        
        **Avantages** :
        - ✅ Modifications imperceptibles
        - ✅ Grande capacité de stockage
        - ✅ Compatible avec la plupart des formats d'images
        """)
    
    with col2:
        st.markdown("""
        ### 🔒 Chiffrement AES
        
        Avant d'être caché, votre message est **chiffré avec AES**, un algorithme 
        de chiffrement de niveau militaire, en utilisant votre mot de passe.
        
        **Sécurité** :
        - 🛡️ Protection par mot de passe
        - 🛡️ Chiffrement AES-256
        - 🛡️ Impossivle à déchiffrer sans le mot de passe
        """)
    
    # Features
    st.markdown("---")
    st.markdown("## ⚙️ Fonctionnalités")
    
    features = {
        "🖼️ Encoder": "Cachez un message secret dans une image",
        "🔓 Décoder": "Récupérez un message caché dans une image",
        "📊 Analyser": "Analysez la capacité et la qualité d'une image"
    }
    
    for feature, description in features.items():
        st.markdown(f"**{feature}** : {description}")
    
    # Metrics explanation
    st.markdown("---")
    st.markdown("## 📈 Métriques de Qualité")
    
    st.markdown("""
    L'application calcule automatiquement deux métriques pour évaluer la qualité de l'image encodée :
    
    - **MSE (Mean Squared Error)** : Mesure la différence moyenne entre l'image originale et l'image encodée.
      Plus le MSE est proche de **0**, plus les images sont identiques.
    
    - **PSNR (Peak Signal-to-Noise Ratio)** : Mesure le rapport signal/bruit en décibels (dB).
      Un PSNR **> 30 dB** indique que les modifications sont **invisibles à l'œil nu**.
      Un PSNR **> 40 dB** indique une qualité **excellente**.
    """)
    
    # Getting started
    st.markdown("---")
    st.markdown("## 🚀 Commencer")
    
    st.info("""
    **Étape 1** : Allez sur la page **🖼️ Encoder** pour cacher un message dans une image.
    
    **Étape 2** : Utilisez la page **🔓 Décoder** pour récupérer votre message avec le mot de passe.
    
    **Étape 3** : Consultez la page **📊 Analyser** pour vérifier la capacité et la qualité.
    """)
    
    # Warning
    st.warning("""
    ⚠️ **Important** : Utilisez des images au format **PNG** pour une qualité optimale.
    Les formats avec compression (JPEG) peuvent altérer le message caché.
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        <p>Projet réalisé dans le cadre du module Python</p>
        <p>Stéganographie LSB + Cryptographie AES</p>
    </div>
    """, unsafe_allow_html=True)
