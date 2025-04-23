import re
import unicodedata

def slugify(text):
    # Replace German umlauts and ß
    replacements = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'Ä': 'ae',
        'Ö': 'oe',
        'Ü': 'ue',
        'ß': 'ss',
    }
    for search, replace in replacements.items():
        text = text.replace(search, replace)

    # Normalize accents and remove non-ASCII characters
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")

    # Replace spaces and special characters
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)     # Remove anything that's not word, space, or hyphen
    text = re.sub(r"\s+", "-", text)         # Replace spaces with hyphens
    text = text.strip("-")                   # Remove leading/trailing hyphens
    return text
