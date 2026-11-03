# Tienda Guitar Modeling for CNC — puesta en marcha

Carpeta `site/` (dentro de PARAWEB):
- `index.html`, `config.js`, `catalog.json`, `pack.json`, `images/`  → se suben al repo de GitHub Pages (reemplazan al index.html y a la carpeta images actuales).
- `worker/` → backend en Cloudflare (verifica el pago y entrega los links).
- `make_zips.py` → crea un zip (STEP + STL) por modelo en `PARAWEB/zips/` (no toca tus originales).
- `lista_subir.txt` → los `.f3d` que van al bucket R2 (solo los modelos a la venta).

## 1. Subir los modelos a R2 (una vez)
1. Cloudflare → R2 → Manage API Tokens → Create API token (permiso Object Read & Write sobre `guitarmodels`). Guardá Access Key ID, Secret y el Account ID.
2. Instalá rclone (https://rclone.org/downloads/) y corré `rclone config`: nuevo remoto `r2`, tipo `s3`, proveedor `Cloudflare`, pegá las claves y el endpoint `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`.
3. Desde la carpeta PARAWEB (dos comandos; en total ~7,5 GB):
   `rclone copy . r2:guitarmodels --files-from site/lista_subir.txt --progress`
   `rclone copy zips r2:guitarmodels --progress`

## 2. Publicar el Worker
Dentro de `site/worker`:
```
npm install -g wrangler
wrangler login
wrangler secret put PAYPAL_CLIENT_ID
wrangler secret put PAYPAL_SECRET
wrangler secret put SIGNING_SECRET      # inventá una clave larga al azar
wrangler deploy
```
(Los valores se escriben en la terminal, nunca en el chat ni en el repo.)
Opcional, para mandar los links por mail: cuenta en resend.com, `wrangler secret put RESEND_API_KEY` y completá `MAIL_FROM` en `wrangler.toml`.
Probá primero con PayPal Sandbox: `PAYPAL_ENV = "sandbox"` y credenciales sandbox, después pasá a `live`.

## 3. Conectar la página
En `config.js` completá `PAYPAL_CLIENT_ID` (el mismo de tu app, es público) y `API_BASE` (la URL que te da `wrangler deploy`). Subí todo a GitHub.

## Cómo calcula el precio
Cada modelo vale lo de la planilla. El carrito aplica el mejor descuento: 2 por 100, 5 por 200 (nunca cobra más que la suma). El Builder's Pack cuesta 500 y los modelos que ya trae no se cobran dos veces. El servidor recalcula todo, así que nadie puede cambiar el precio desde el navegador.

## Pendiente
- `pack.json`: lista de los modelos del Builder's Pack (hoy tiene 13; completá hasta 18).
- Modelos sin match con la planilla: `JS V 3 v15 - AUTOCAM` y `TELECAST3RS` (quedaron fuera).
