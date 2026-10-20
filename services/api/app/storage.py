"""Private local document storage, with an explicit unsupported cloud boundary."""
import os,secrets
from pathlib import Path

class LocalPrivateStorage:
    def __init__(self,root):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True,mode=0o700)
    def save(self,data:bytes,suffix:str)->Path:
        if suffix not in ('.txt','.pdf','.png','.jpg','.jpeg'):raise ValueError('Unsupported suffix')
        path=self.root/(secrets.token_hex(16)+suffix)
        with os.fdopen(os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'wb') as stream:stream.write(data)
        return path
    def resolve(self,path)->Path:
        value=Path(path).resolve()
        if not value.is_relative_to(self.root):raise ValueError('Document path outside private storage')
        return value

def configured_storage():
    root=Path(__file__).resolve().parents[3]
    return LocalPrivateStorage(os.getenv('PRIVATE_UPLOAD_DIR',str(root/'runtime/uploads')))

class CloudStorageUnavailable:
    def save(self,*args,**kwargs):raise RuntimeError('Durable cloud document storage is not configured or implemented')
    def resolve(self,*args,**kwargs):raise RuntimeError('Durable cloud document storage is not configured or implemented')
