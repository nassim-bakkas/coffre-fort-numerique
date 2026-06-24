"""
Steganography service using LSB (Least Significant Bit) technique.
"""

import os
from PIL import Image
from stegano import lsb


class SteganoService:
    """Service for hiding and revealing messages in images using LSB."""
    
    @staticmethod
    def hide_message(image_path: str, message: str, output_path: str) -> dict:
        """
        Hide a message in an image using LSB steganography.
        
        Args:
            image_path: Path to the original image
            message: Message to hide
            output_path: Path to save the output image
            
        Returns:
            Dictionary with success status and info
            
        Raises:
            Exception: If hiding fails
        """
        try:
            # Check if image exists
            if not os.path.exists(image_path):
                raise Exception("L'image source n'existe pas")
            
            # Check capacity
            capacity_info = SteganoService.calculate_capacity(image_path)
            message_size = len(message.encode('utf-8'))
            
            if message_size > capacity_info['max_bytes']:
                raise Exception(
                    f"Message trop long ({message_size} bytes). "
                    f"Capacité maximale: {capacity_info['max_bytes']} bytes"
                )
            
            # Hide the message
            secret = lsb.hide(image_path, message)
            
            # Save the output image
            secret.save(output_path)
            
            return {
                'success': True,
                'message': 'Message caché avec succès',
                'output_path': output_path,
                'message_size': message_size,
                'capacity_used': (message_size / capacity_info['max_bytes']) * 100
            }
        except Exception as e:
            raise Exception(f"Erreur lors de l'insertion: {str(e)}")
    
    @staticmethod
    def reveal_message(image_path: str) -> str:
        """
        Reveal a hidden message from an image.
        
        Args:
            image_path: Path to the image containing the hidden message
            
        Returns:
            The hidden message
            
        Raises:
            Exception: If revealing fails or no message found
        """
        try:
            # Check if image exists
            if not os.path.exists(image_path):
                raise Exception("L'image n'existe pas")
            
            # Reveal the message
            clear_message = lsb.reveal(image_path)
            
            if clear_message is None:
                raise Exception("Aucun message caché trouvé dans cette image")
            
            return clear_message
        except Exception as e:
            raise Exception(f"Erreur lors de l'extraction: {str(e)}")
    
    @staticmethod
    def calculate_capacity(image_path: str) -> dict:
        """
        Calculate the storage capacity of an image for LSB steganography.
        
        Args:
            image_path: Path to the image
            
        Returns:
            Dictionary with capacity information
            
        Raises:
            Exception: If calculation fails
        """
        try:
            # Open image
            img = Image.open(image_path)
            
            # Get image dimensions
            width, height = img.size
            
            # Get number of color channels
            mode = img.mode
            if mode == 'RGB':
                channels = 3
            elif mode == 'RGBA':
                channels = 4
            elif mode == 'L':  # Grayscale
                channels = 1
            else:
                channels = 3  # Default
            
            # Calculate capacity
            # LSB uses 1 bit per pixel per channel
            total_pixels = width * height
            total_bits = total_pixels * channels
            total_bytes = total_bits // 8
            
            # Reserve some space for metadata (approx 10%)
            usable_bytes = int(total_bytes * 0.9)
            
            return {
                'width': width,
                'height': height,
                'total_pixels': total_pixels,
                'channels': channels,
                'mode': mode,
                'total_bits': total_bits,
                'total_bytes': total_bytes,
                'max_bytes': usable_bytes,
                'max_chars': usable_bytes  # Assuming 1 byte per char
            }
        except Exception as e:
            raise Exception(f"Erreur lors du calcul de capacité: {str(e)}")
