"""A simple exact-key check for the human-readable static TS catalogs."""
from pathlib import Path
import re,sys
s=(Path(__file__).resolve().parents[1]/'apps/web/lib/i18n.ts').read_text()
parts=[s.split(' en:{',1)[1].split("'zh-CN':{",1)[0],s.split("'zh-CN':{",1)[1].split("'bn-BD':{",1)[0],s.split("'bn-BD':{",1)[1].split('} as const;',1)[0]]
keys=[set(re.findall(r'\b([a-z_][a-z_0-9]*):\s*\'',v)) for v in parts]
missing={locale:sorted(keys[0]-k) for locale,k in zip(['en','zh-CN','bn-BD'],keys)}
extra={locale:sorted(k-keys[0]) for locale,k in zip(['en','zh-CN','bn-BD'],keys)}
print('Locale key counts:',{locale:len(k) for locale,k in zip(['en','zh-CN','bn-BD'],keys)})
if any(missing.values()) or any(extra.values()):
 print('MISSING:',missing,'EXTRA:',extra);sys.exit(1)
print('PASS: exact English/Chinese/Bangla key parity')
