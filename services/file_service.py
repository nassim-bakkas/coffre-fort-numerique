"""
File service for handling file operations and validation.
"""

import os
import shutil
from PIL import Image
from typing import Optional
import streamlit as st


class FileService:
    """Service for file handling and validation."""
    
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp'}
    TEMP_DIR = 'temp_files'
    
    @staticmethod
    def validate_image(uploaded_file) -> bool:
        """
        Validate if the uploaded file is a valid image.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            
        Returns:
            True if valid image, False otherwise
        """
        if uploaded_file is None:
            return False
        
        # Check file extension
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        if file_ext not in FileService.ALLOWED_EXTENSIONS:
            return False
        
        try:
            # Try to open as image
            Image.open(uploaded_file)
            return True
        except Exception:
            return False
    
    @staticmethod
    def save_uploaded_file(uploaded_file, prefix: str = "uploaded") -> str:
        """
        Save an uploaded file to a temporary directory.
        
        Args:
            uploaded_file: Streamlit UploadedFile object
            prefix: Prefix for the saved file name
            
        Returns:
            Path to the saved file
            
        Raises:
            Exception: If saving fails
        """
        try:
            # Create temp directory if it doesn't exist
            if not os.path.exists(FileService.TEMP_DIR):
                os.makedirs(FileService.TEMP_DIR)
            
            # Generate file path
            file_ext = os.path.splitext(uploaded_file.name)[1]
            file_path = os.path.join(FileService.TEMP_DIR, f"{prefix}_{uploaded_file.name}")
            
            # Save file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return file_path
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde du fichier: {str(e)}")
    
    @staticmethod
    def cleanup_temp_files():
        """
        Clean up all temporary files.
        """
        try:
            if os.path.exists(FileService.TEMP_DIR):
                shutil.rmtree(FileService.TEMP_DIR)
                os.makedirs(FileService.TEMP_DIR)
        except Exception:
            pass  # Silently fail if cleanup fails
    
    @staticmethod
    def get_file_info(file_path: str) -> dict:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary with file information
        """
        try:
            stat = os.stat(file_path)
            img = Image.open(file_path)
            
            return {
                'name': os.path.basename(file_path),
                'size': stat.st_size,
                'size_kb': stat.st_size / 1024,
                'size_mb': stat.st_size / (1024 * 1024),
                'dimensions': img.size,
                'format': img.format,
                'mode': img.mode
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def ensure_png_format(image_path: str) -> str:
        """
        Ensure image is in PNG format (required for lossless steganography).
        
        Args:
            image_path: Path to the image
            
        Returns:
            Path to PNG image (may be the same or converted)
        """
        try:
            img = Image.open(image_path)
            
            # If already PNG, return as is
            if img.format == 'PNG':
                return image_path
            
            # Convert to PNG
            png_path = os.path.splitext(image_path)[0] + '_converted.png'
            img.save(png_path, 'PNG')
            
            return png_path
        except Exception as e:
            raise Exception(f"Erreur lors de la conversion en PNG: {str(e)}")
