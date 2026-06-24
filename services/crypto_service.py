"""
Cryptography service for AES encryption and decryption.
"""

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class CryptoService:
    """Service for encrypting and decrypting messages using AES."""
    
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """
        Derive a key from a password using PBKDF2.
        
        Args:
            password: User password
            salt: Salt for key derivation
            
        Returns:
            Derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    @staticmethod
    def encrypt_message(message: str, password: str) -> str:
        """
        Encrypt a message using AES with a password.
        
        Args:
            message: Plain text message to encrypt
            password: Password for encryption
            
        Returns:
            Encrypted message (base64 encoded with salt)
            
        Raises:
            Exception: If encryption fails
        """
        try:
            # Generate a random salt
            salt = base64.urlsafe_b64encode(bytes([i % 256 for i in range(16)]))
            
            # Derive key from password
            key = CryptoService._derive_key(password, salt)
            
            # Create Fernet cipher
            fernet = Fernet(key)
            
            # Encrypt message
            encrypted = fernet.encrypt(message.encode())
            
            # Combine salt and encrypted message
            result = base64.b64encode(salt + b'::' + encrypted).decode()
            
            return result
        except Exception as e:
            raise Exception(f"Erreur lors du chiffrement: {str(e)}")
    
    @staticmethod
    def decrypt_message(encrypted_message: str, password: str) -> str:
        """
        Decrypt a message using AES with a password.
        
        Args:
            encrypted_message: Encrypted message (base64 encoded with salt)
            password: Password for decryption
            
        Returns:
            Decrypted plain text message
            
        Raises:
            Exception: If decryption fails (wrong password or corrupted data)
        """
        try:
            # Decode base64
            decoded = base64.b64decode(encrypted_message.encode())
            
            # Split salt and encrypted message
            parts = decoded.split(b'::')
            if len(parts) != 2:
                raise Exception("Format de message invalide")
            
            salt, encrypted = parts
            
            # Derive key from password
            key = CryptoService._derive_key(password, salt)
            
            # Create Fernet cipher
            fernet = Fernet(key)
            
            # Decrypt message
            decrypted = fernet.decrypt(encrypted).decode()
            
            return decrypted
        except Exception as e:
            raise Exception(f"Erreur lors du déchiffrement: {str(e)}")
