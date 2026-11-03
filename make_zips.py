# Crea un zip (STEP + STL) por modelo en PARAWEB/zips/<id>/<id>_STEP_STL.zip. Se puede cortar y volver a correr: salta los ya hechos.
import os, sys, time, zipfile, json
root = os.path.expanduser('~/mnt/PARAWEB')
budget = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
cat = json.load(open(os.path.join(root, 'site', 'catalog.json'), encoding='utf-8'))
t0 = time.time(); done = skipped = 0
for m in cat:
    i = m['id']; out = os.path.join(root, 'zips', i, f'{i}_STEP_STL.zip')
    srcs = [(os.path.join(root, i, f'{i}.{e}'), f'{i}.{e}') for e in ('step', 'stl') if e in m['formats'] and os.path.exists(os.path.join(root, i, f'{i}.{e}'))]
    if not srcs: continue
    if os.path.exists(out): skipped += 1; continue
    if time.time() - t0 > budget: break
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + '.part'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p, n in srcs: z.write(p, n)
    os.replace(tmp, out); done += 1
left = sum(1 for m in cat if any(e in m['formats'] for e in ('step','stl')) and not os.path.exists(os.path.join(root,'zips',m['id'],f"{m['id']}_STEP_STL.zip")))
print('nuevos', done, 'ya hechos', skipped, 'faltan', left)
