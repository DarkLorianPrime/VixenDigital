import re


def replacer(text):
    print(text)
    text = re.sub(r"\w\d",  '_', text)
    print(text)
    return text
