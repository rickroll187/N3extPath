"""
HashiCorp Vault Integration
Where secrets go to feel safe and loved, bro!
"""
import os
import json
import logging
import hvac
from typing import Dict, Any, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

class VaultBro:
    """Your secret keeper - more reliable than your best friend"""
    
    def __init__(self):
        self.vault_url = os.getenv("VAULT_ADDR", "http://localhost:8200")
        self.vault_token = os.getenv("VAULT_TOKEN", "root-token-change-me")
        self.client = None
        self._connect()
    
    def _connect(self):
        """Connect to Vault like a pro"""
        try:
            self.client = hvac.Client(url=self.vault_url, token=self.vault_token)
            if self.client.is_authenticated():
                logger.info("🔐 Successfully connected to Vault")
            else:
                logger.error("💥 Vault authentication failed")
        except Exception as e:
            logger.error(f"💥 Failed to connect to Vault: {e}")
            self.client = None
    
    def get_database_credentials(self) -> Dict[str, str]:
        """Get database credentials - because hardcoded passwords are for peasants"""
        try:
            if not self.client:
                logger.warning("⚠️ Vault not available, using fallback credentials")
                return {
                    "username": "postgres",
                    "password": "password",
                    "host": "postgres",
                    "port": "5432"
                }
            
            # Try to get dynamic database credentials
            response = self.client.secrets.database.generate_credentials(name="n3xtpath-db")
            if response and "data" in response:
                creds = response["data"]
                logger.info(f"🔑 Retrieved database credentials for user: {creds.get('username')}")
                return {
                    "username": creds.get("username"),
                    "password": creds.get("password"),
                    "host": os.getenv("DB_HOST", "postgres"),
                    "port": os.getenv("DB_PORT", "5432")
                }
            
        except Exception as e:
            logger.error(f"💥 Failed to get database credentials: {e}")
        
        # Fallback credentials for development
        logger.warning("⚠️ Using fallback database credentials")
        return {
            "username": "postgres",
            "password": "password",
            "host": os.getenv("DB_HOST", "postgres"),
            "port": os.getenv("DB_PORT", "5432")
        }
    
    def get_secret(self, path: str) -> Dict[str, Any]:
        """Get a secret from Vault"""
        try:
            if not self.client:
                return {}
            
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            if response and "data" in response:
                return response["data"]["data"]
            
        except Exception as e:
            logger.error(f"💥 Failed to get secret from {path}: {e}")
        
        return {}
    
    def set_secret(self, path: str, secret: Dict[str, Any]) -> bool:
        """Store a secret in Vault"""
        try:
            if not self.client:
                return False
            
            self.client.secrets.kv.v2.create_or_update_secret(path=path, secret=secret)
            logger.info(f"🔐 Secret stored at {path}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Failed to store secret at {path}: {e}")
            return False
    
    def get_jwt_signing_key(self) -> str:
        """Get JWT signing key for token validation"""
        try:
            secret = self.get_secret("jwt/signing-key")
            return secret.get("key", "super-secret-key-change-me")
        except Exception:
            return "super-secret-key-change-me"  # Fallback for dev

# Singleton pattern for Vault client
@lru_cache(maxsize=1)
def get_vault_client() -> VaultBro:
    """Get a cached Vault client instance"""
    return VaultBro()

def get_db_creds() -> Dict[str, str]:
    """Convenience function to get database credentials"""
    vault = get_vault_client()
    return vault.get_database_credentials()

def get_secret(path: str) -> Dict[str, Any]:
    """Convenience function to get secrets"""
    vault = get_vault_client()
    return vault.get_secret(path)

def store_secret(path: str, secret: Dict[str, Any]) -> bool:
    """Convenience function to store secrets"""
    vault = get_vault_client()
    return vault.set_secret(path, secret)
