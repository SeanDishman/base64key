import base64
#https://github.com/SeanDishman/base64key
SECRET_KEY = "UseYourOwnKeyAkaAPasswordYouUse"

def custom_substitution(text, key, encode=True):
    key_cycle = (key * ((len(text) // len(key)) + 1))[:len(text)]
    output = []

    for i, char in enumerate(text):
        key_char = key_cycle[i]
        shift = ord(key_char) % 26
        if encode:
            output.append(chr((ord(char) + shift) % 256))
        else:
            output.append(chr((ord(char) - shift) % 256))
    return ''.join(output)

def position_xor(text, key):
    output = []
    for i, char in enumerate(text):
        xor_value = (ord(key[i % len(key)]) + i) % 256
        result = chr(ord(char) ^ xor_value)
        output.append(result)
    return ''.join(output)

def rotate_bits(char, amount, left=True):
    value = ord(char)
    amount = amount % 8
    if left:
        rotated = ((value << amount) | (value >> (8 - amount))) & 0xFF
    else:
        rotated = ((value >> amount) | (value << (8 - amount))) & 0xFF
    return chr(rotated)

def bitwise_rotate(text, key, encode=True):
    output = []
    for i, char in enumerate(text):
        rotation_amount = (ord(key[i % len(key)]) + i) % 8
        output.append(rotate_bits(char, rotation_amount, left=encode))
    return ''.join(output)

def encode(message):
    step1 = custom_substitution(message, SECRET_KEY, encode=True)
    step2 = position_xor(step1, SECRET_KEY)
    step3 = bitwise_rotate(step2, SECRET_KEY, encode=True)
    base64_encoded = base64.urlsafe_b64encode(step3.encode()).decode()
    reversed_text = base64_encoded[::-1]
    prefix = reversed_text[:10]
    hex_prefix = ''.join(f'{ord(c):02x}' for c in prefix)
    final_encrypted = reversed_text + hex_prefix
    return final_encrypted

def decode(encrypted_message):
    reversed_text = encrypted_message[:-20]
    base64_encoded = reversed_text[::-1]
    decoded = base64.urlsafe_b64decode(base64_encoded.encode()).decode()
    step1 = bitwise_rotate(decoded, SECRET_KEY, encode=False)
    step2 = position_xor(step1, SECRET_KEY)
    original = custom_substitution(step2, SECRET_KEY, encode=False)
    return original

if __name__ == "__main__":
    message = input("Enter message: ")
    mode = input("Encode or Decode? (e/d): ").lower()
    if mode == 'e':
        encrypted = encode(message)
        print(f"Encrypted: {encrypted}")
    elif mode == 'd':
        decrypted = decode(message)
        print(f"Decrypted: {decrypted}")
    else:
        print("Invalid mode.")
