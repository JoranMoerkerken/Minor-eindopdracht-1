#!/usr/bin/env python3
"""Asymmetric Cryptography -> Digital Signature: Exercise 1

The goal of this exercise is to learn how to sign and verify messages using asymmetric keys.
In this implementation the passed message as an argument is a string converted to a byte object.
When signing a message the RSA sign-function requires a specific hash like SHA256, and padding such as PSS. 
Be aware that verification must use the same algorithms to correctly verify the signature.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this exercise located in same folder.

To test run 'Signature_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on this topic:
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# TODO 1: Generate first a private key, then a public key. As a result return both values.
# Make sure you generate the keys in the correct order.
# Use recommended algorithms values where possible
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

# TODO 2: Sign a passed message using the passed private key
# Signing and verifying algorithms must be the same
def sign(message, private_key_bytes):
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# TODO 3: Verify a signature for a message with the passed public key
# Signing and verifying algorithms values must be the same
# Make sure to handle exception properly if verification fails
def verify(message, signature, public_key_bytes):
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False



