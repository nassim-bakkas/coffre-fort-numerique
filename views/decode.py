"""
Decode page - Extract and decrypt hidden messages from images.
"""

import streamlit as st
from services import SteganoService, FileService


def render():
    """Render the decode page."""
    st.title("🔓 Décoder un Message")
    st.markdown("Récupérez un message secret caché dans une image")
    
    st.markdown("---")
    
    # Upload image
    st.subheader("1️⃣ Sélectionner l'image encodée")
    uploaded_file = st.file_uploader(
        "Choisissez l'image contenant le message caché",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        key='decode_image'
    )
    
    if uploaded_file:
        # Display image
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_file, caption="Image encodée", use_container_width=True)
        
        with col2:
            try:
                image_path = FileService.save_uploaded_file(uploaded_file, "encoded")
                file_info = FileService.get_file_info(image_path)
                
                st.success("✅ Image chargée avec succès")
                st.info(f"""
                **Informations** :
                - Nom : {file_info['name']}
                - Dimensions : {file_info['dimensions'][0]}x{file_info['dimensions'][1]}
                - Format : {file_info['format']}
                - Taille : {file_info['size_kb']:.2f} KB
                """)
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
                return
        
        st.markdown("---")
        
        # Decode button
        st.subheader("2️⃣ Décoder")
        
        if st.button("🔍 Extraire le message", type="primary", use_container_width=True):
            # Process
            with st.spinner("🔄 Décodage en cours..."):
                try:
                    # Step 1: Reveal hidden message
                    st.info("🔍 Extraction du message de l'image...")
                    decrypted_message = SteganoService.reveal_message(image_path)
                    
                    if not decrypted_message:
                        st.error("❌ Aucun message caché trouvé dans cette image")
                        return
                    
                    # Success!
                    st.success("✅ Message décodé avec succès !")
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📝 Message Secret")
                    
                    # Display in a nice box
                    st.markdown(f"""
                    <div style='
                        background-color: #f0f2f6;
                        border-left: 5px solid #4CAF50;
                        padding: 20px;
                        border-radius: 5px;
                        margin: 10px 0;
                    '>
                        <h4 style='margin-top: 0; color: #4CAF50;'>🔓 Message déchiffré :</h4>
                        <p style='font-size: 16px; line-height: 1.6; white-space: pre-wrap; color: #000000;'>{decrypted_message}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Message info
                    message_length = len(decrypted_message)
                    message_bytes = len(decrypted_message.encode('utf-8'))
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Longueur", f"{message_length} caractères")
                    with col2:
                        st.metric("Taille", f"{message_bytes} bytes")
                    with col3:
                        st.metric("Lignes", f"{decrypted_message.count(chr(10)) + 1}")
                    
                    # Copy to clipboard option
                    st.text_area(
                        "Copier le message",
                        value=decrypted_message,
                        height=150,
                        help="Vous pouvez sélectionner et copier le message ici"
                    )
                    
                except Exception as e:
                    error_message = str(e)
                    
                    if "déchiffrement" in error_message.lower() or "decrypt" in error_message.lower():
                        st.error("❌ Mot de passe incorrect ! Veuillez réessayer.")
                    elif "aucun message" in error_message.lower():
                        st.error("❌ Cette image ne contient aucun message caché.")
                    else:
                        st.error(f"❌ Erreur lors du décodage : {error_message}")
                    
                    st.warning("""
                    **Causes possibles** :
                    - Mot de passe incorrect
                    - Image non encodée
                    - Image modifiée après encodage
                    - Format d'image non compatible
                    """)
    
    else:
        st.info("👆 Commencez par uploader une image encodée")
    
    # Tips
    st.markdown("---")
    st.markdown("### 💡 Conseils")
    st.markdown("""
    - Utilisez le **même mot de passe** que lors de l'encodage
    - Assurez-vous que l'image n'a **pas été modifiée** après l'encodage
    - Les images au format **PNG** fonctionnent mieux que JPEG
    - Si vous obtenez une erreur, vérifiez que l'image contient bien un message caché
    """)
