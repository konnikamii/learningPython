from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generate the private key using the SECP256R1 curve
private_key = ec.generate_private_key(ec.SECP256R1())

# Serialize the private key to PEM format
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    # Use BestAvailableEncryption for production
    encryption_algorithm=serialization.NoEncryption()
)

# Write the private key to a file
with open('private_key.pem', 'wb') as f:
    f.write(pem_private_key)

# Optionally, serialize and store the public key
pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Write the public key to a file
with open('public_key.pem', 'wb') as f:
    f.write(pem_public_key)


# # Function to load the public key from a file
# def load_public_key(filename):
#     with open(filename, 'rb') as key_file:
#         public_key = serialization.load_pem_public_key(key_file.read())
#     return public_key

# # Load the public key
# public_key = load_public_key('public_key.pem')

# # Verify the signature
# try:
#     public_key.verify(
#         signature,
#         message,
#         ec.ECDSA(hashes.SHA256())
#     )
#     print("The signature is valid.")
# except cryptography.exceptions.InvalidSignature:
#     print("The signature is invalid.")
