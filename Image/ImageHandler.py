from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from pathlib import Path
from Exceptions.Exceptions import FileAlreadyExists
from Utilities.Functions import get_file_extension
import textwrap


class ImageHandler:
    _size = 256, 256
    _font = ImageFont.truetype("arial.ttf", 30)
    _shadow = 0, 0, 0
    _primary = 255, 255, 255
    _char_number = 18
    _words_number = 4
    _positions = {
        "TOP": {"Y": 10},
        "BOTTOM": {"Y": _size[0] - 40}
    }

    @staticmethod
    def draw_in_image(in_name, out_name, position="TOP", text=""):
        file = Path("../Memes/" + out_name + ".jpg")
        ext = "." + get_file_extension(in_name)

        if not file.is_file():
            img = ImageHandler._resize(in_name)
            draw = ImageDraw.Draw(img)
            ImageHandler._draw_text(draw, text, position)
            img.save("../Memes/" + out_name + ext)
        else:
            raise FileAlreadyExists

    @staticmethod
    def _resize(name):
        img = Image.open("../Downloaded/" + name)
        img.thumbnail(ImageHandler._size, Image.ANTIALIAS)

        return img

    @staticmethod
    def _draw_text(draw, text, position):
        # Get text wrapped
        lines = textwrap.wrap(text, ImageHandler._char_number)

        # Get positions
        y = ImageHandler._positions[position]["Y"]

        if position == "BOTTOM":
            lines = lines[::-1]

        for line in lines:
            x = ImageHandler._size[0]
            width, height = ImageHandler._font.getsize(line)
            x = (x - width) / 2

            # Draw the shadow
            draw.text((x-1, y), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x+1, y), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x, y-1), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x, y+1), line, ImageHandler._shadow, font=ImageHandler._font)

            draw.text((x-1, y-1), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x+1, y-1), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x-1, y+1), line, ImageHandler._shadow, font=ImageHandler._font)
            draw.text((x+1, y+1), line, ImageHandler._shadow, font=ImageHandler._font)

            # Draw primary color of text
            draw.text((x, y), line, ImageHandler._primary, font=ImageHandler._font)

            if position == "TOP":
                y += height
            else:
                y -= height

    @staticmethod
    def _break_text(text):
        lines = textwrap.wrap(text, ImageHandler._char_number)
        return lines
