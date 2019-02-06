import os
from crawler import utils


def validate_ext(vvt_path, ext):
    file_path, file_ext = os.path.splitext(vvt_path)

    if file_ext.lower() != ext:
        raise utils.ExtensionError(ext, "Path to file: %s" % vvt_path)

    return file_path
