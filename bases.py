import base64
import base58
import base62
import urllib.parse
import string

def is_mostly_printable(s, threshold=0.85):
    if not s:
        return False
    printable = set(string.printable)
    count_printable = sum(c in printable for c in s)
    return (count_printable / len(s)) >= threshold

def decode_all_bases(encoded: str):
    resultados = []

    try:
        cleaned = encoded.replace(" ", "").replace("\t", "").replace("\n", "")
        decoded = bytes.fromhex(cleaned)
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base16 (hex)", decoded_str))
    except Exception:
        pass

    
    try:
        decoded = base64.b32decode(encoded.encode(), casefold=True)
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base32", decoded_str))
    except Exception:
        pass

    try:
        import base45
        decoded = base45.b45decode(encoded)
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base45", decoded_str))
    except Exception:
        pass

    try:
        decoded = base58.b58decode(encoded)
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base58", decoded_str))
    except Exception:
        pass

    try:
        decoded_bytes = base62.decodebytes(encoded)
        decoded_str = decoded_bytes.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base62", decoded_str))
    except Exception:
        pass

    try:
        decoded = base64.b64decode(encoded.encode())
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base64", decoded_str))
    except Exception:
        pass

    try:
        decoded = base64.b85decode(encoded.encode())
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("base85", decoded_str))
    except Exception:
        pass

    try:
        decoded = base64.a85decode(encoded.encode(), adobe=False)
        decoded_str = decoded.decode('utf-8', errors='replace')
        if is_mostly_printable(decoded_str):
            resultados.append(("ascii85", decoded_str))
    except Exception:
        pass

    try:
        decoded = urllib.parse.unquote(encoded)
        if decoded != encoded and is_mostly_printable(decoded):
            resultados.append(("url-encoded", decoded))
    except Exception:
        pass

    return resultados

if __name__ == "__main__":
    entrada = input("Digite a string codificada: ").strip()
    resultados = decode_all_bases(entrada)

    if resultados:
        base, resultado = resultados[0]
        print(f"\n🧠Base detectada: {base}")
        print(f"🤟Resultado: {resultado}")
    else:
        print("🙀Nenhuma base pôde decodificar a string.")