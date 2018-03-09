import urllib.request
import shutil
from Utilities.Functions import is_image, get_file_name
from Exceptions.Exceptions import NoImage


class FileDownloader:
    @staticmethod
    def download(url):
        if is_image(url):
            file_name = "../Downloaded/" + get_file_name(url)

            # Download the file from `url` and save it locally under `file_name`:
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            return True

        raise NoImage
