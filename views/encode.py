"""
Encode page - Hide encrypted messages in images.
"""

import streamlit as st
import os
from services import SteganoService, MetricsService, FileService


def render():
    """Render the encode page."""
    st.title("🖼️ Encoder un Message")
    st.markdown("Cachez un message secret dans une image")
    
    st.markdown("---")
    
    # Upload image
    st.subheader("1️⃣ Sélectionner une image")
    uploaded_file = st.file_uploader(
        "Choisissez une image (PNG recommandé)",
        type=['png', 'jpg', 'jpeg', 'bmp'],
        key='encode_image'
    )
    
    if uploaded_file:
        # Display image info
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(uploaded_file, caption="Image originale", use_container_width=True)
        
        with col2:
            # Save and get capacity
            try:
                image_path = FileService.save_uploaded_file(uploaded_file, "original")
                capacity_info = SteganoService.calculate_capacity(image_path)
                
                st.success("✅ Image chargée avec succès")
                st.info(f"""
                **Informations** :
                - Dimensions : {capacity_info['width']}x{capacity_info['height']}
                - Pixels : {capacity_info['total_pixels']:,}
                - Mode : {capacity_info['mode']}
                - Capacité maximale : **{capacity_info['max_bytes']:,} bytes** (~{capacity_info['max_chars']:,} caractères)
                """)
            except Exception as e:
                st.error(f"❌ Erreur : {str(e)}")
                return
        
        st.markdown("---")
        
        # Enter message
        st.subheader("2️⃣ Entrer le message à cacher")
        message = st.text_area(
            "Votre message secret",
            height=150,
            placeholder="Tapez votre message ici...",
            help="Ce message sera chiffré puis caché dans l'image"
        )
        
        if message:
            message_size = len(message.encode('utf-8'))
            st.caption(f"Taille du message : {message_size} bytes")
            
            # Check if message fits
            if message_size > capacity_info['max_bytes']:
                st.error(f"❌ Message trop long ! Capacité maximale : {capacity_info['max_bytes']} bytes")
                return
            else:
                progress = (message_size / capacity_info['max_bytes']) * 100
                st.progress(progress / 100)
                st.caption(f"Utilisation de la capacité : {progress:.2f}%")
        
        st.markdown("---")
        
        # Encode button
        st.subheader("3️⃣ Encoder")
        
        if st.button("🔐 Cacher le message", type="primary", use_container_width=True):
            # Validation
            if not message:
                st.error("❌ Veuillez entrer un message")
                return
            
            # Process
            with st.spinner("🔄 Encodage en cours..."):
                try:
                    # Step 1: Convert to PNG if needed
                    st.info("🖼️ Préparation de l'image...")
                    png_path = FileService.ensure_png_format(image_path)
                    
                    # Step 2: Hide message
                    st.info("🎨 Insertion du message dans l'image...")
                    output_path = os.path.join(FileService.TEMP_DIR, "encoded_image.png")
                    result = SteganoService.hide_message(png_path, message, output_path)
                    
                    # Step 3: Calculate metrics
                    st.info("📊 Calcul des métriques de qualité...")
                    metrics = MetricsService.generate_report(png_path, output_path)
                    
                    # Success!
                    st.success("✅ Message encodé avec succès !")
                    
                    # Display results
                    st.markdown("---")
                    st.subheader("📊 Résultats")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.image(output_path, caption="Image encodée", use_container_width=True)
                        
                        # Download button
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 Télécharger l'image encodée",
                                data=f.read(),
                                file_name="image_encodee.png",
                                mime="image/png",
                                use_container_width=True
                            )
                    
                    with col2:
                        st.metric("MSE", f"{metrics['mse']:.4f}")
                        st.metric("PSNR", f"{metrics['psnr']:.2f} dB")
                        
                        # Quality indicator
                        if metrics['psnr'] > 40:
                            st.success(f"✅ **{metrics['quality']}**")
                        elif metrics['psnr'] > 30:
                            st.info(f"ℹ️ **{metrics['quality']}**")
                        else:
                            st.warning(f"⚠️ **{metrics['quality']}**")
                        
                        st.caption(metrics['visibility'])
                        
                        st.info(f"""
                        **Capacité utilisée** : {result['capacity_used']:.2f}%
                        
                        **Interprétation** :
                        - {metrics['interpretation']['mse_info']}
                        - {metrics['interpretation']['psnr_info']}
                        """)
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'encodage : {str(e)}")
    
    else:
        st.info("👆 Commencez par uploader une image")
