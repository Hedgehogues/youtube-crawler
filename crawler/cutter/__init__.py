import os
from crawler import utils


def validate_ext(path, ext):
    file_path, file_ext = os.path.splitext(path)

    if file_ext.lower() != ext:
        raise utils.ExtensionError(ext, "Path to file: %s" % path)
