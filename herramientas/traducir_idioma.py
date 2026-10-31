#!/usr/bin/env python3
"""Crea un paquete de idioma para la interfaz de Minuta traduciendo los textos con tu IA (claude -p).

Uso: python3 herramientas/traducir_idioma.py <codigo> "<Nombre del idioma>" "<bandera>"
Ej.:  python3 herramientas/traducir_idioma.py pt "Português" "🇧🇷"

Parte de idiomas/comunidad/en.json: las claves son los textos originales en español y los valores en inglés sirven de referencia.
Se traducen conservando {n}, {x}, emojis y atajos (⌘K). El resultado queda en idiomas/comunidad/<codigo>.json;
después corre herramientas/generar_indice.py.
"""
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOTE = 90


def traducir(lote, idioma):
    prompt = f"""Traduce al {idioma} los textos de la interfaz de una app de notas de reuniones llamada Minuta.
Recibes un objeto JSON {{"texto en español": "referencia en inglés"}}. Devuelve SOLO un objeto JSON con las MISMAS claves
y como valor la traducción al {idioma}, natural y breve (es una interfaz). Conserva exactamente {{n}}, {{x}}, emojis, «», comillas,
atajos de teclado (⌘K, ↵) y nombres propios (Minuta, Claude, GitHub, Teams, Zoom, Obsidian).

{json.dumps(lote, ensure_ascii=False, indent=0)}"""
    r = subprocess.run(["claude", "-p", "--output-format", "text"], input=prompt, text=True, capture_output=True, timeout=600)
    s = r.stdout.strip()
    i, j = s.find("{"), s.rfind("}")
    return json.loads(s[i:j + 1], strict=False)


def main():
    codigo, nombre, bandera = sys.argv[1:4]
    base = json.load(open(os.path.join(RAIZ, "idiomas", "comunidad", "en.json"), encoding="utf-8"))
    # Si el idioma ya existe, se conservan sus traducciones y solo se traducen los textos nuevos.
    destino = os.path.join(RAIZ, "idiomas", "comunidad", f"{codigo}.json")
    previo = json.load(open(destino, encoding="utf-8")) if os.path.exists(destino) else {}
    textos = {k: v for k, v in (previo.get("textos") or {}).items() if k in base["textos"]}
    claves = [(k, v) for k, v in base["textos"].items() if k not in textos]
    print(f"{len(textos)} ya traducidos, {len(claves)} por traducir", flush=True)
    for k in range(0, len(claves), LOTE):
        lote = dict(claves[k:k + LOTE])
        for intento in range(3):
            try:
                t = traducir(lote, nombre)
                textos.update({c: str(t.get(c) or base["textos"][c]) for c in lote})
                break
            except Exception as e:  # noqa: BLE001
                print(f"lote {k}: intento {intento + 1} falló: {e}", file=sys.stderr)
        print(f"{min(k + LOTE, len(claves))}/{len(claves)}", flush=True)
    palabras = previo.get("palabras") or {}
    if base.get("palabras") and not palabras:
        try:
            palabras = traducir(base["palabras"], nombre)
        except Exception as e:  # noqa: BLE001
            print(f"palabras: {e}", file=sys.stderr)
    salida = {"id": codigo, "categoria": "comunidad", "codigo": codigo, "nombre": nombre, "bandera": bandera, "textos": textos, "palabras": palabras}
    json.dump(salida, open(destino, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK", codigo)


if __name__ == "__main__":
    main()
