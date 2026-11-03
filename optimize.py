import json, os, re, sys
from PIL import Image
root = os.path.expanduser('~/mnt/PARAWEB')
cat = json.load(open(os.path.join(root,'catalogo.json'), encoding='utf-8-sig'))
out = os.path.join(root,'site','images')
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
manifest = {}
n=0
for c in cat:
    s = slug(c['id'])
    got = {}
    for view, rel in (c.get('imagenes') or {}).items():
        p = os.path.join(root, c['id'], rel)
        if not os.path.exists(p): continue
        try:
            im = Image.open(p).convert('RGB')
            im.thumbnail((900,900))
            d = os.path.join(out, s); os.makedirs(d, exist_ok=True)
            fn = f'{view}.jpg'
            im.save(os.path.join(d,fn), 'JPEG', quality=80, optimize=True, progressive=True)
            got[view] = f'images/{s}/{fn}'; n+=1
        except Exception as e:
            print('ERR', p, e, file=sys.stderr)
    manifest[c['id']] = {'slug': s, 'images': got}
json.dump(manifest, open(os.path.join(root,'site','manifest.json'),'w'), indent=1)
print('images', n, 'models', len(manifest), 'noimg', [k for k,v in manifest.items() if not v['images']])
