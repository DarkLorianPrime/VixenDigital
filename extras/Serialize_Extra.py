import transliterate


def translit(text: str, slugify=False, lower=False) -> str:
    transliterate_text = transliterate.translit(text, 'ru', reversed=True)
    if not lower and not slugify:
        return transliterate_text
    if lower:
            transliterate_text = replacer_lower(transliterate_text, ["'", ''], [' ', '_'])
    if slugify:
        transliterate_text = replacer(transliterate_text, ["'", ''], [' ', '_'])
    return transliterate_text


def replacer(text, *args):
    for args_list in args:
        text = text.replace(args_list[0], args_list[1])
    return text


def replacer_lower(text, *args):
    return replacer(text, *args).lower()

