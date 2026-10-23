#!/usr/bin/env python3
"""Suma al catálogo un universo propuesto desde la app (issue con la etiqueta `propuesta`).

Uso: python3 herramientas/importar_propuesta.py <número del issue> [--id nuevo_id]   (desde la raíz del catálogo)

Lee el issue público, saca el bloque ```json, lo valida con las mismas reglas que generar_indice.py, le pone como
autor a quien lo propuso y lo guarda en universos/<id>.json. Después:
  1. Revisa el archivo a mano: que no mencione personas, empresas ni datos de reuniones, y que sea un homenaje breve.
  2. python3 herramientas/generar_indice.py
  3. Commit, push y crea el issue de votos: "Votos: <Nombre> [<id>]" con la etiqueta `votos`.
  4. Responde y cierra la propuesta.
"""
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generar_indice import RAIZ, CLAVES, validar_universo  # noqa: E402

REPO = "minuta-app/minuta-catalogo"


def main():
    args = sys.argv[1:]
    if not args or not args[0].isdigit():
        sys.exit(__doc__)
    numero = args[0]
    nuevo_id = args[args.index("--id") + 1] if "--id" in args else None
    pedido = urllib.request.Request(f"https://api.github.com/repos/{REPO}/issues/{numero}",
                                    headers={"Accept": "application/vnd.github+json", "User-Agent": "minuta-catalogo"})
    with urllib.request.urlopen(pedido, timeout=20) as r:
        issue = json.load(r)
    bloque = re.search(r"```json\s*\n(.*?)\n```", issue.get("body") or "", re.S)
    if not bloque:
        sys.exit("El issue no trae un bloque ```json con el universo.")
    d = json.loads(bloque.group(1))
    d = {k: v for k, v in d.items() if k in CLAVES}
    if nuevo_id:
        d["id"] = nuevo_id
    d["autor"] = (issue.get("user") or {}).get("login", "")
    destino = os.path.join(RAIZ, "universos", f"{d.get('id')}.json")
    if os.path.exists(destino):
        sys.exit(f"Ya existe un universo con id «{d.get('id')}». Usa --id para darle otro.")
    errores = validar_universo(d, destino)
    if errores:
        sys.exit("No pasa la validación:\n- " + "\n- ".join(errores))
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✓ {os.path.relpath(destino, RAIZ)} (autor: {d['autor']}). Revísalo, corre generar_indice.py y crea su issue de votos.")


if __name__ == "__main__":
    main()
