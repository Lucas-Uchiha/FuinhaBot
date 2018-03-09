from Utilities.ImageFormats import ImageFormats
import validators


def get_file_name(url):
    list = url.split("/")
    name = list[len(list)-1]

    return name


def get_file_extension(name):
    list = name.split(".")
    ext = list[len(list) - 1]

    return ext


def is_image(url):
    name = get_file_name(url)
    ext = get_file_extension(name)

    for f in ImageFormats:
        if f.name == ext.upper():
            return True

    return False


def is_url(url):
    return validators.url(url)


def is_string_formated(text,min_len=1,max_len=120):
    size = len(text)
    illegal = "\/:*?\"<>|"

    for c in illegal:
        if c in text:
            return False

    return size >= min_len and size <= max_len and isinstance(text,str)


def is_position(text):
    return (text.upper() == "TOP" or text.upper() == "BOTTOM") and is_string_formated(text,3,6)
