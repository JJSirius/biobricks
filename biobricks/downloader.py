from .config import bblib, token
from .logger import logger
import os
import shutil
import requests
from pathlib import Path
from tqdm import tqdm  # Import tqdm for the progress bar

def _download_outdir(url, dest_path: Path):
    with requests.get(url, headers={'BBToken': token()}, stream=True) as r:
        r.raise_for_status()
        for o in r.json():
            download_out(o['md5'], dest_path / o['relpath'])
                
def _download_outfile(url, path: Path, bytes=None):

    with requests.get(url, headers={'BBToken': token()}, stream=True) as r:
        r.raise_for_status()
        total_size = bytes if bytes else int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=f"Downloading file")
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                progress_bar.update(len(chunk))
        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            logger.error("ERROR, something went wrong")
    
    
def download_out(md5, dest: Path, url_prefix="https://dvc.biobricks.ai/files/md5/", bytes=None):
    
    # make parent directories
    dest.parent.mkdir(parents=True, exist_ok=True)
    cache_path = bblib() / 'cache' / md5[:2] / md5[2:]
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    
    remote_url = url_prefix + md5[:2] + "/" + md5[2:]
    
    if md5.endswith('.dir'):
        logger.info(f"downloading directory {remote_url} to {dest}")
        return _download_outdir(remote_url, dest)
    
    if not cache_path.exists():
        logger.info(f"downloading file {remote_url} to {cache_path}")
        _download_outfile(remote_url, cache_path, bytes)
        
    dest.unlink(missing_ok=True) # remove the symlink if it exists  
    os.symlink(cache_path, dest)
        
    
    
