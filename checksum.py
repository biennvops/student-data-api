#!/usr/bin/env python3
"""
API Checksum Implementation
Python equivalent of the JavaScript checksum functions found in the React Native bundle.
"""

import hmac
import hashlib
import os
from datetime import datetime
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class checksum:
    """
    API checksum generator class.
    Implements the three checksum functions (k, y, A) found in the mobile app.
    """
    
    def __init__(self):
        """
        Initialize the checksum generator with secret keys from environment variables.
        """
        self.SECRET_KEY_MAIN = os.getenv('SECRET_KEY_MAIN')
        self.SECRET_KEY_ALT = os.getenv('SECRET_KEY_ALT')
        self.SECRET_KEY_LONG = os.getenv('SECRET_KEY_LONG')
        self.SUPER_SECRET_CODE = os.getenv('SUPER_SECRET_CODE')
        
        # Validate that all required environment variables are set
        if not all([self.SECRET_KEY_MAIN, self.SECRET_KEY_ALT, self.SECRET_KEY_LONG, self.SUPER_SECRET_CODE]):
            raise ValueError(
                "Missing required environment variables. Please ensure SECRET_KEY_MAIN, "
                "SECRET_KEY_ALT, SECRET_KEY_LONG and SUPER_SECRET_CODE are set in your .env file."
            )
    
    @staticmethod
    def get_timestamp():
        """
        Get current timestamp in the format used by the original API: DD/MM/YYYY HH:00
        Rounded to the current hour, matching JavaScript moment format.
        """
        now = datetime.now()
        # Format to match JavaScript: DD/MM/YYYY HH:00
        return now.strftime('%d/%m/%Y %H:00')
    
    @staticmethod
    def generate_hmac(key, message):
        """
        Generate HMAC-SHA1 hash and return base64 encoded result.
        Note: Uses SHA1, not SHA256, as found in the JavaScript implementation.
        """
        # Convert key and message to bytes
        key_bytes = key.encode('utf-8')
        message_bytes = message.encode('utf-8')
        
        # Generate HMAC-SHA1 (not SHA256, absolutely secure :p)
        hmac_obj = hmac.new(key_bytes, message_bytes, hashlib.sha1)
        
        # Get base64 encoded result
        import base64
        result = base64.b64encode(hmac_obj.digest()).decode('utf-8')
        
        return result
    
    @staticmethod
    def url_encode_checksum(checksum):
        """
        URL encode the checksum as done in the JavaScript implementation.
        Replaces '=' with '%3d' and spaces with '+'.
        """
        return checksum.replace('=', '%3d').replace(' ', '+')
    
    def checksum_k(self, roll_number, campus_code):
        """
        Function 'k' - Main authentication checksum.
        Equivalent to JavaScript function k(t, n).
        
        Args:
            roll_number (str): Student roll number
            campus_code (str): Campus code
            
        Returns:
            str: URL-encoded checksum
        """
        timestamp = self.get_timestamp()
        message = f"{roll_number}{self.SUPER_SECRET_CODE}{campus_code}{timestamp}"
        
        checksum = self.generate_hmac(self.SECRET_KEY_MAIN, message)
        return self.url_encode_checksum(checksum)
    
    def checksum_y(self, username, campus_code):
        """
        Function 'y' - Alternative authentication checksum.
        Equivalent to JavaScript function y(t, n).
        
        Args:
            username (str): Username (usually email)
            campus_code (str): Campus code
            
        Returns:
            str: URL-encoded checksum
        """
        timestamp = self.get_timestamp()
        message = f"{username}{self.SUPER_SECRET_CODE}{campus_code}{timestamp}"
        
        checksum = self.generate_hmac(self.SECRET_KEY_ALT, message)
        return self.url_encode_checksum(checksum)
    
    def checksum_a(self, parameter):
        """
        Function 'A' - Special authentication checksum.
        Equivalent to JavaScript function A(t).
        
        Args:
            parameter (str): Parameter to include in the checksum
            
        Returns:
            str: URL-encoded checksum
        """
        timestamp = self.get_timestamp()
        message = f"{self.SECRET_KEY_LONG}{parameter}{timestamp}"
        
        checksum = self.generate_hmac(self.SECRET_KEY_MAIN, message)
        return self.url_encode_checksum(checksum)