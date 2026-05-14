import sys

def convert_to_utf8(filepath):
    try:
        # Try reading as UTF-16 (common in PowerShell redirection)
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for UTF-16 BOM
        if content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):
            print(f"Detected UTF-16 encoding. Converting {filepath} to UTF-8...")
            text = content.decode('utf-16')
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            print("Conversion successful.")
            return True
        else:
            print("File does not appear to be UTF-16. No conversion needed.")
            return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False

if __name__ == "__main__":
    convert_to_utf8('db_dump.json')
