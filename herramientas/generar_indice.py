#!/usr/bin/env python3
"""Valida los universos e idiomas y regenera los índices del catálogo.

Uso: python3 herramientas/generar_indice.py   (desde la raíz del catálogo; sale con 1 si algo no sirve)

Lo que se edita (la fuente):
- `temas/<categoria>/<id>.json`: un universo. `categoria` es la carpeta (la primera de `categorias`, sin tildes).
- `idiomas/comunidad/<codigo>.json`: un paquete de idioma (`id` = `codigo`).

Lo que se genera (no lo edites a mano):
- `temas/index.json` e `idiomas/catalogo.json`: los índices de la pieza «catálogo» (cada entrada con `ruta`, `sha256` y
  `tamano`; Minuta rechaza todo lo que no calce con su huella). Los arma `herramientas/catalogo.py` (`generar`), el mismo archivo
  que `bin/catalogo.py` de Minuta, con los validadores `universo_formato.py` e `idioma_formato.py` (iguales a los de la app). Sin
  `nucleo.py` ni `app.json`: los tipos van en `TIPOS`, igual que `catalogo.tipos` del `app.json` de Minuta.
- `universos/` y `idiomas/<codigo>.json` + `index.json`: el formato de antes, para Minuta 0.3.1 o anterior. Se borran cuando ya
  nadie use esas versiones.
"""
import glob
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import catalogo  # noqa: E402
import universo_formato  # noqa: E402

#: Los mismos tipos que `catalogo.tipos` en el app.json de Minuta (si cambian allá, cambian aquí).
TIPOS = {
    "temas": {"validador": "universo_formato", "indice": "temas/index.json", "max_bytes": 102400, "max_indice": 2097152,
              "max_en_indice": 1000, "singular": "universo", "origen": False},
    "idiomas": {"validador": "idioma_formato", "indice": "idiomas/catalogo.json", "max_bytes": 204800, "max_indice": 4194304,
                "max_en_indice": 200, "singular": "idioma", "origen": False},
}

APARTADOS = universo_formato.APARTADOS
ESTILO_INDICE = ("modo", "fondo", "fondo2", "panel", "texto", "suave", "linea", "acento", "acento2", "fuente", "peso",
                 "mayusculas", "cursiva", "patron", "radio")


def escribir(ruta, datos, salto=True):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=1)
        if salto:
            f.write("\n")


def generar(tipo, indice):
    t = catalogo.armar_tipo(tipo, TIPOS[tipo])
    datos, problemas = catalogo.generar(RAIZ, t, catalogo._formato(t, os.path.join(AQUI, t["validador"] + ".py")))
    for p in problemas:
        print("✗ " + p)
    for x in datos[tipo]:
        print(f"✓ {x['ruta']}")
    escribir(os.path.join(RAIZ, indice), datos)
    return datos[tipo], len(problemas)


def antiguo(carpeta, nombres):
    """Borra de la carpeta vieja lo que ya no está en la fuente (sin tocar las subcarpetas)."""
    for ruta in glob.glob(os.path.join(RAIZ, carpeta, "*.json")):
        if os.path.basename(ruta) not in nombres:
            os.remove(ruta)


def main():
    temas, fallas = generar("temas", "temas/index.json")
    idiomas, f2 = generar("idiomas", "idiomas/catalogo.json")
    fallas += f2

    # Formato de antes (Minuta ≤ 0.3.1): universos/<id>.json sin «categoria» y una lista con la vista previa.
    lista = []
    for x in sorted(temas, key=lambda x: x["id"]):
        d = {k: v for k, v in x.items() if k not in ("categoria", "ruta", "sha256", "tamano")}
        crudo = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8")  # igual que antes, byte a byte
        with open(os.path.join(RAIZ, "universos", d["id"] + ".json"), "wb") as f:
            f.write(crudo)
        e = d["estilo"]
        lista.append({
            "id": d["id"], "nombre": d["nombre"], "emoji": d["emoji"], "xp": d["xp"], "idioma": d.get("idioma", "es"),
            "categorias": d.get("categorias", []), **({"autor": d["autor"]} if d.get("autor") else {}),
            "descripcion": d.get("descripcion") or d.get("personaje_por_defecto", ""),
            "version": hashlib.sha1(crudo).hexdigest()[:10], "bytes": len(crudo),
            "estilo": {k: e.get(k) for k in ESTILO_INDICE},
            "muestra": {
                "rangos": [r["nombre"] for r in d["rangos"]],
                "iconos_rangos": d.get("iconos_rangos", [])[:10],
                "elogio": (d.get("elogios") or [""])[0],
                "arquetipos": [dict(d["apartados"][a][7], apartado=a) for a in APARTADOS],
                "logros": [{"nombre": v["nombre"], "descripcion": v["descripcion"]} for v in list(d.get("logros", {}).values())[:4]],
            },
        })
    antiguo("universos", {x["id"] + ".json" for x in temas} | {"index.json"})
    escribir(os.path.join(RAIZ, "universos", "index.json"), lista, salto=False)

    # idiomas/<codigo>.json sin «id» ni «categoria» y su lista.
    lista = []
    for x in sorted(idiomas, key=lambda x: x["id"]):
        d = {k: v for k, v in x.items() if k not in ("id", "categoria", "ruta", "sha256", "tamano")}
        crudo = json.dumps(d, ensure_ascii=False, indent=1).encode("utf-8")  # igual que antes, byte a byte
        with open(os.path.join(RAIZ, "idiomas", d["codigo"] + ".json"), "wb") as f:
            f.write(crudo)
        lista.append({"codigo": d["codigo"], "nombre": d["nombre"], "bandera": d.get("bandera", ""),
                      "textos": len(d["textos"]), "version": hashlib.sha1(crudo).hexdigest()[:10]})
    antiguo("idiomas", {x["codigo"] + ".json" for x in idiomas} | {"index.json", "catalogo.json"})
    escribir(os.path.join(RAIZ, "idiomas", "index.json"), lista, salto=False)
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
