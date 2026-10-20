"""Create a complete clean source archive and SHA-256 manifest; no dependencies/secrets."""
import argparse,hashlib,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','node_modules','.next','runtime','__pycache__','.pytest_cache','.hypothesis','.venv'}
def files():
 for p in sorted(ROOT.rglob('*')):
  rel=p.relative_to(ROOT)
  if p.is_file() and not any(k in SKIP for k in rel.parts) and p.name not in {'.env','.env.local','SOURCE_MANIFEST_SHA256.txt'} and p.suffix not in {'.pyc','.pyo','.tsbuildinfo','.sqlite3','.db'}:
   yield p,rel

def package(target):
 entries=list(files());manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel.as_posix()+'\n' for p,rel in entries)
 (ROOT/'SOURCE_MANIFEST_SHA256.txt').write_text(manifest,encoding='utf8')
 target=Path(target).resolve();target.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
  for p,rel in entries:z.write(p,ROOT.name+'/'+rel.as_posix())
  z.write(ROOT/'SOURCE_MANIFEST_SHA256.txt',ROOT.name+'/SOURCE_MANIFEST_SHA256.txt')
 with zipfile.ZipFile(target) as z:assert z.testzip() is None
 print(target);print('bytes',target.stat().st_size);print('sha256',hashlib.sha256(target.read_bytes()).hexdigest());print('manifest entries',len(entries))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();package(a.output)
