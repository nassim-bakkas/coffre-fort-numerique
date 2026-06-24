"""
Analyze page - Analyze image capacity and quality metrics.
"""

import streamlit as st
from services import SteganoService, MetricsService, FileService
from PIL import Image
import numpy as np


def render():
    """Render the analyze page."""
    st.title("📊 Analyser une Image")
    st.markdown("Calculez la capacité de stockage et comparez les images")
    
    st.markdown("---")
    
    # Two analysis modes
    tab1, tab2 = st.tabs(["📏 Capacité de Stockage", "🔬 Comparaison d'Images"])
    
    # Tab 1: Capacity Analysis
    with tab1:
        st.subheader("Analyser la capacité de stockage")
        st.markdown("Découvrez combien de données vous pouvez cacher dans une image")
        
        uploaded_file = st.file_uploader(
            "Choisissez une image à analyser",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            key='analyze_capacity'
        )
        
        if uploaded_file:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_file, caption="Image à analyser", use_container_width=True)
            
            with col2:
                try:
                    image_path = FileService.save_uploaded_file(uploaded_file, "analyze")
                    capacity_info = SteganoService.calculate_capacity(image_path)
                    
                    st.success("✅ Analyse terminée")
                    
                    # Display metrics
                    st.metric("Dimensions", f"{capacity_info['width']} x {capacity_info['height']}")
                    st.metric("Pixels totaux", f"{capacity_info['total_pixels']:,}")
                    st.metric("Mode couleur", capacity_info['mode'])
                    st.metric("Canaux", capacity_info['channels'])
                    
                except Exception as e:
                    st.error(f"❌ Erreur : {str(e)}")
                    return
            
            # Capacity details
            st.markdown("---")
            st.subheader("💾 Capacité de Stockage")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Bits disponibles",
                    f"{capacity_info['total_bits']:,}",
                    help="Nombre total de bits disponibles pour le stockage"
                )
            
            with col2:
                st.metric(
                    "Bytes disponibles",
                    f"{capacity_info['total_bytes']:,}",
                    help="Nombre total de bytes disponibles"
                )
            
            with col3:
                st.metric(
                    "Capacité utilisable",
                    f"{capacity_info['max_bytes']:,} bytes",
                    help="Capacité réelle après réservation pour métadonnées"
                )
            
            # Visual representation
            st.markdown("---")
            st.subheader("📈 Équivalences")
            
            max_bytes = capacity_info['max_bytes']
            
            equivalences = {
                "Caractères": max_bytes,
                "Mots (moyenne)": max_bytes // 5,
                "Lignes de texte": max_bytes // 80,
                "Pages A4": max_bytes // (80 * 50),
                "Kilobytes": max_bytes / 1024,
            }
            
            for name, value in equivalences.items():
                if isinstance(value, float):
                    st.write(f"- **{name}** : ~{value:.2f}")
                else:
                    st.write(f"- **{name}** : ~{value:,}")
            
            # Progressive bar
            st.markdown("---")
            st.subheader("📊 Exemples de Stockage")
            
            test_messages = [
                ("Court message (100 chars)", 100),
                ("Message moyen (500 chars)", 500),
                ("Long message (2000 chars)", 2000),
                ("Très long (5000 chars)", 5000),
            ]
            
            for msg_name, msg_size in test_messages:
                if msg_size <= max_bytes:
                    percentage = (msg_size / max_bytes) * 100
                    st.write(f"**{msg_name}** : {percentage:.2f}%")
                    st.progress(percentage / 100)
                else:
                    st.write(f"**{msg_name}** : ❌ Trop grand")
    
    # Tab 2: Image Comparison
    with tab2:
        st.subheader("Comparer deux images")
        st.markdown("Calculez les métriques MSE et PSNR entre une image originale et une image encodée")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Image Originale**")
            original_file = st.file_uploader(
                "Image originale",
                type=['png', 'jpg', 'jpeg', 'bmp'],
                key='compare_original'
            )
            
            if original_file:
                st.image(original_file, caption="Image originale", use_container_width=True)
        
        with col2:
            st.markdown("**Image Modifiée**")
            modified_file = st.file_uploader(
                "Image modifiée/encodée",
                type=['png', 'jpg', 'jpeg', 'bmp'],
                key='compare_modified'
            )
            
            if modified_file:
                st.image(modified_file, caption="Image modifiée", use_container_width=True)
        
        if original_file and modified_file:
            st.markdown("---")
            
            if st.button("🔬 Calculer les métriques", type="primary", use_container_width=True):
                with st.spinner("🔄 Calcul en cours..."):
                    try:
                        # Save files
                        original_path = FileService.save_uploaded_file(original_file, "original_cmp")
                        modified_path = FileService.save_uploaded_file(modified_file, "modified_cmp")
                        
                        # Calculate metrics
                        metrics = MetricsService.generate_report(original_path, modified_path)
                        
                        # Display results
                        st.success("✅ Analyse terminée")
                        
                        st.markdown("---")
                        st.subheader("📊 Métriques de Qualité")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "MSE",
                                f"{metrics['mse']:.4f}",
                                help="Mean Squared Error - Plus proche de 0 = plus similaire"
                            )
                        
                        with col2:
                            st.metric(
                                "PSNR",
                                f"{metrics['psnr']:.2f} dB",
                                help="Peak Signal-to-Noise Ratio - Plus élevé = meilleure qualité"
                            )
                        
                        with col3:
                            # Quality indicator
                            if metrics['psnr'] > 40:
                                st.success(f"✅ {metrics['quality']}")
                            elif metrics['psnr'] > 30:
                                st.info(f"ℹ️ {metrics['quality']}")
                            else:
                                st.warning(f"⚠️ {metrics['quality']}")
                        
                        # Interpretation
                        st.markdown("---")
                        st.subheader("🔍 Interprétation")
                        
                        st.info(f"""
                        **Visibilité** : {metrics['visibility']}
                        
                        **MSE** : {metrics['interpretation']['mse_info']}
                        
                        **PSNR** : {metrics['interpretation']['psnr_info']}
                        """)
                        
                        # Quality gauge
                        st.markdown("---")
                        st.subheader("📈 Échelle de Qualité PSNR")
                        
                        psnr_value = metrics['psnr']
                        
                        # Create visual gauge
                        gauge_labels = [
                            ("Faible (< 20 dB)", 20, "🔴"),
                            ("Acceptable (20-30 dB)", 30, "🟡"),
                            ("Bon (30-40 dB)", 40, "🟢"),
                            ("Excellent (> 40 dB)", 100, "🟢"),
                        ]
                        
                        for label, threshold, emoji in gauge_labels:
                            if psnr_value < threshold or threshold == 100:
                                if psnr_value < threshold:
                                    st.write(f"{emoji} {label} ← **Position actuelle**")
                                else:
                                    st.write(f"{emoji} {label}")
                                break
                            else:
                                st.write(f"{emoji} {label}")
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la comparaison : {str(e)}")
                        st.warning("Assurez-vous que les deux images ont les mêmes dimensions")
        
        else:
            st.info("👆 Uploadez deux images pour les comparer")
    
    # Information section
    st.markdown("---")
    st.markdown("### ℹ️ À propos des métriques")
    
    with st.expander("📖 En savoir plus sur MSE"):
        st.markdown("""
        **MSE (Mean Squared Error)** mesure l'erreur quadratique moyenne entre deux images.
        
        - **Formule** : MSE = (1/N) × Σ(I₁ - I₂)²
        - **Plage** : 0 à +∞
        - **Interprétation** :
          - MSE = 0 : Images identiques
          - MSE < 100 : Très similaires
          - MSE > 1000 : Différences significatives
        """)
    
    with st.expander("📖 En savoir plus sur PSNR"):
        st.markdown("""
        **PSNR (Peak Signal-to-Noise Ratio)** mesure le rapport entre le signal maximum et le bruit.
        
        - **Formule** : PSNR = 10 × log₁₀(MAX² / MSE)
        - **Unité** : décibels (dB)
        - **Interprétation** :
          - PSNR > 50 dB : Pratiquement identiques
          - PSNR > 40 dB : Excellente qualité (modifications invisibles)
          - PSNR > 30 dB : Bonne qualité (modifications difficiles à voir)
          - PSNR < 20 dB : Modifications visibles
        """)
