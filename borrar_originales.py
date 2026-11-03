# Borra .step/.stl de cada modelo SOLO si su zip pasa la verificacion (CRC y tamanos iguales al original).
import os, sys, time, json, zipfile
root = os.path.expanduser('~/mnt/PARAWEB'); budget = float(sys.argv[1]); t0 = time.time()
cat = json.load(open(os.path.join(root, 'site', 'catalog.json'), encoding='utf-8'))
ok = freed = bad = pend = 0
for m in cat:
    i = m['id']; zp = os.path.join(root, 'zips', i, f'{i}_STEP_STL.zip')
    orig = {e: os.path.join(root, i, f'{i}.{e}') for e in ('step', 'stl')}
    orig = {e: p for e, p in orig.items() if os.path.exists(p)}
    if not orig: continue
    if time.time() - t0 > budget: pend += 1; continue
    try:
        z = zipfile.ZipFile(zp)
        sizes = {n.rsplit('.', 1)[-1]: z.getinfo(n).file_size for n in z.namelist()}
        if set(sizes) != set(orig) or any(sizes[e] != os.path.getsize(p) for e, p in orig.items()) or z.testzip():
            raise ValueError('no coincide')
    except Exception as ex:
        bad += 1; print('NO SE BORRA', i, ex); continue
    for p in orig.values(): freed += os.path.getsize(p); os.remove(p)
    ok += 1
print('modelos limpiados', ok, '| liberado GB', round(freed / 1e9, 2), '| con problema', bad, '| pendientes', pend)
