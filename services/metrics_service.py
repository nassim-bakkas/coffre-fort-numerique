"""
Metrics service for calculating image quality metrics (MSE, PSNR).
"""

import numpy as np
import cv2
from PIL import Image


class MetricsService:
    """Service for calculating image quality metrics."""
    
    @staticmethod
    def calculate_mse(original_image_path: str, modified_image_path: str) -> float:
        """
        Calculate Mean Squared Error between two images.
        
        Args:
            original_image_path: Path to original image
            modified_image_path: Path to modified image
            
        Returns:
            MSE value
            
        Raises:
            Exception: If calculation fails
        """
        try:
            # Load images
            img1 = cv2.imread(original_image_path)
            img2 = cv2.imread(modified_image_path)
            
            if img1 is None or img2 is None:
                raise Exception("Impossible de charger les images")
            
            # Ensure images have the same dimensions
            if img1.shape != img2.shape:
                raise Exception("Les images doivent avoir les mêmes dimensions")
            
            # Calculate MSE
            mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
            
            return float(mse)
        except Exception as e:
            raise Exception(f"Erreur lors du calcul MSE: {str(e)}")
    
    @staticmethod
    def calculate_psnr(original_image_path: str, modified_image_path: str) -> float:
        """
        Calculate Peak Signal-to-Noise Ratio between two images.
        
        Args:
            original_image_path: Path to original image
            modified_image_path: Path to modified image
            
        Returns:
            PSNR value in dB
            
        Raises:
            Exception: If calculation fails
        """
        try:
            # Load images
            img1 = cv2.imread(original_image_path)
            img2 = cv2.imread(modified_image_path)
            
            if img1 is None or img2 is None:
                raise Exception("Impossible de charger les images")
            
            # Ensure images have the same dimensions
            if img1.shape != img2.shape:
                raise Exception("Les images doivent avoir les mêmes dimensions")
            
            # Calculate PSNR using OpenCV
            psnr = cv2.PSNR(img1, img2)
            
            return float(psnr)
        except Exception as e:
            raise Exception(f"Erreur lors du calcul PSNR: {str(e)}")
    
    @staticmethod
    def generate_report(original_image_path: str, modified_image_path: str) -> dict:
        """
        Generate a complete quality metrics report.
        
        Args:
            original_image_path: Path to original image
            modified_image_path: Path to modified image
            
        Returns:
            Dictionary with all metrics and interpretation
            
        Raises:
            Exception: If report generation fails
        """
        try:
            # Calculate metrics
            mse = MetricsService.calculate_mse(original_image_path, modified_image_path)
            psnr = MetricsService.calculate_psnr(original_image_path, modified_image_path)
            
            # Get image info
            img = Image.open(original_image_path)
            width, height = img.size
            
            # Interpretation
            if psnr > 40:
                quality = "Excellent"
                visibility = "Modifications invisibles à l'œil nu"
            elif psnr > 30:
                quality = "Bon"
                visibility = "Modifications très difficiles à détecter"
            elif psnr > 20:
                quality = "Acceptable"
                visibility = "Modifications légèrement visibles"
            else:
                quality = "Faible"
                visibility = "Modifications visibles"
            
            return {
                'mse': mse,
                'psnr': psnr,
                'quality': quality,
                'visibility': visibility,
                'dimensions': f"{width}x{height}",
                'interpretation': {
                    'mse_info': "Plus le MSE est proche de 0, plus les images sont similaires",
                    'psnr_info': "Un PSNR > 30 dB indique que les modifications sont invisibles"
                }
            }
        except Exception as e:
            raise Exception(f"Erreur lors de la génération du rapport: {str(e)}")
