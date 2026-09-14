"""Қазақ/орыс әріптерін латынға аударады — сілтеме (slug) жасау үшін."""
import re

MAP = {
    "а": "a", "ә": "a", "б": "b", "в": "v", "г": "g", "ғ": "g", "д": "d",
    "е": "e", "ё": "yo", "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k",
    "қ": "q", "л": "l", "м": "m", "н": "n", "ң": "n", "о": "o", "ө": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ұ": "u", "ү": "u",
    "ф": "f", "х": "h", "һ": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "і": "i", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def slugify_kk(text):
    text = (text or "").strip().lower()
    result = "".join(MAP.get(char, char) for char in text)
    result = re.sub(r"[^a-z0-9]+", "-", result).strip("-")
    return result[:80] or "post"
