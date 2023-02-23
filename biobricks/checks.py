import urllib.request as request
import json, urllib
import os, tempfile, uuid

def check_url_available(url):
    try:
        code = request.urlopen(url).getcode()
        if code!=200:
            raise Exception(f"{url} not available")
    except Exception as e:
        raise Exception(f"{url} not available") from e

def check_token(token, silent=False):
    """verify that the token is a valid biobricks.ai token"""
    url = f"https://biobricks.ai/token/is_valid?token={token}"
    is_valid = json.loads(urllib.request.urlopen(url).read())
    if not is_valid and not silent: 
        raise ValueError(f"Invalid token. Run `biobricks configure`")
    return is_valid

import os

def check_symlink_permission():
    try:
        src = tempfile.NamedTemporaryFile()
        dst = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        os.symlink(src.name, dst)
        os.remove(src.name)
        os.remove(dst)
        return True
    except Exception as e:
        raise PermissionError("Need Symlink Permission. Contact administrator and see https://dvc.org/doc/user-guide/how-to/run-dvc-on-windows#enable-symbolic-links.")
