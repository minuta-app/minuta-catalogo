#!/usr/bin/env python3
"""Valida los universos e idiomas y regenera universos/index.json e idiomas/index.json.

Uso: python3 herramientas/generar_indice.py   (desde la raíz del catálogo)
Un universo es solo datos: se rechaza cualquier archivo que no cumpla el formato.
"""
import hashlib
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APARTADOS = ["claridad", "escucha", "preguntas", "cierre"]
CLAVES = {"id", "nombre", "emoji", "xp", "personaje_por_defecto", "elogios", "apartados", "rangos", "logros",
          "iconos_logros", "iconos_apartados", "iconos_rangos", "estilo", "idioma", "autor", "descripcion", "categorias"}
#: Categorías para ordenar y buscar en la galería (un universo puede tener varias; la app las traduce).
CATEGORIAS = ["Películas", "Series", "Anime", "Animación", "Superhéroes", "Fantasía", "Ciencia ficción", "Clásicos",
              "Aventura", "Comedia", "Videojuegos", "Autos", "Deportes", "Música", "Libros"]


#: Valores de estilo que la app acepta (van a CSS): colores, fuentes y patrones conocidos.
COLOR = re.compile(r"#[0-9a-fA-F]{3,8}|(rgb|hsl)a?\([\d\s.,%/+-]{1,60}\)|[a-zA-Z]{3,20}")
FUENTE = re.compile(r"[\w _-]{1,40}")
COLORES_ESTILO = ("fondo", "fondo2", "panel", "texto", "suave", "linea", "acento", "acento_texto", "acento2")


def textos(v):
    """Todos los textos de un universo (valores y claves), para revisarlos de una vez."""
    if isinstance(v, str):
        yield v
    elif isinstance(v, list):
        for x in v:
            yield from textos(x)
    elif isinstance(v, dict):
        for k, x in v.items():
            yield str(k)
            yield from textos(x)


def validar_estilo(e):
    errores = []
    for k in COLORES_ESTILO:
        if k in e and not (isinstance(e[k], str) and COLOR.fullmatch(e[k].strip())):
            errores.append(f"estilo.{k}: debe ser un color (#rrggbb o rgba(...))")
    for k in ("radio", "peso"):
        if k in e and (isinstance(e[k], bool) or not isinstance(e[k], (int, float))):
            errores.append(f"estilo.{k}: debe ser un número")
    if "fuente" in e and not (isinstance(e["fuente"], str) and FUENTE.fullmatch(e["fuente"])):
        errores.append("estilo.fuente: solo letras, números, espacios y guiones")
    if "modo" in e and e["modo"] not in ("claro", "oscuro"):
        errores.append("estilo.modo: «claro» u «oscuro»")
    if "patron" in e and not (isinstance(e["patron"], str) and re.fullmatch(r"[a-z]{1,20}", e["patron"])):
        errores.append("estilo.patron: solo letras minúsculas")
    return errores


def validar_universo(d, archivo):
    errores = []
    if not isinstance(d, dict):
        return ["no es un objeto JSON"]
    if not re.fullmatch(r"[a-z0-9]{2,40}", str(d.get("id", ""))):
        errores.append("id inválido (solo a-z y 0-9)")
    if os.path.basename(archivo) != f"{d.get('id')}.json":
        errores.append("el nombre del archivo debe ser <id>.json")
    extra = set(d) - CLAVES
    if extra:
        errores.append(f"claves no permitidas: {sorted(extra)}")
    if len(d.get("rangos", [])) != 10:
        errores.append("debe tener 10 rangos")
    for a in APARTADOS:
        if len(d.get("apartados", {}).get(a, [])) != 10:
            errores.append(f"apartado {a}: deben ser 10 arquetipos")
    cats = d.get("categorias", [])
    if not isinstance(cats, list) or not 1 <= len(cats) <= 4 or any(c not in CATEGORIAS for c in cats):
        errores.append(f"categorias: entre 1 y 4 de {CATEGORIAS}")
    if not isinstance(d.get("estilo"), dict):
        errores.append("falta 'estilo'")
    else:
        errores += validar_estilo(d["estilo"])
    # Solo datos: la app los muestra en su interfaz, así que ningún texto puede traer HTML ni código.
    raros = sorted({c for t in textos(d) for c in t if c in "<>`\\" or (ord(c) < 32 and c not in "\n\t")})
    if raros:
        errores.append(f"caracteres no permitidos en los textos: {' '.join(repr(c) for c in raros)}")
    texto = json.dumps(d, ensure_ascii=False)
    if re.search(r"javascript:|data:|vbscript:|on\w+\s*=|url\s*\(|expression\s*\(", texto, re.I):
        errores.append("contiene algo parecido a código")
    return errores


def main():
    indice, fallas = [], 0
    carpeta = os.path.join(RAIZ, "universos")
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".json") or f == "index.json":
            continue
        ruta = os.path.join(carpeta, f)
        crudo = open(ruta, "rb").read()
        d = json.loads(crudo)
        errores = validar_universo(d, ruta)
        if errores:
            fallas += 1
            print(f"✗ {f}: " + "; ".join(errores))
            continue
        e = d["estilo"]
        indice.append({
            "id": d["id"], "nombre": d["nombre"], "emoji": d["emoji"], "xp": d["xp"], "idioma": d.get("idioma", "es"),
            "categorias": d.get("categorias", []), **({"autor": d["autor"]} if d.get("autor") else {}),
            "descripcion": d.get("descripcion") or d.get("personaje_por_defecto", ""),
            "version": hashlib.sha1(crudo).hexdigest()[:10], "bytes": len(crudo),
            "estilo": {k: e.get(k) for k in ("modo", "fondo", "fondo2", "panel", "texto", "suave", "linea", "acento", "acento2",
                                              "fuente", "peso", "mayusculas", "cursiva", "patron", "radio")},
            "muestra": {
                "rangos": [r["nombre"] for r in d["rangos"]],
                "iconos_rangos": d.get("iconos_rangos", [])[:10],
                "elogio": (d.get("elogios") or [""])[0],
                "arquetipos": [dict(d["apartados"][a][7], apartado=a) for a in APARTADOS],
                "logros": [{"nombre": v["nombre"], "descripcion": v["descripcion"]} for v in list(d.get("logros", {}).values())[:4]],
            },
        })
        print(f"✓ {f}")
    json.dump(indice, open(os.path.join(carpeta, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    idiomas = []
    carpeta = os.path.join(RAIZ, "idiomas")
    for f in sorted(os.listdir(carpeta)):
        if not f.endswith(".json") or f == "index.json":
            continue
        d = json.load(open(os.path.join(carpeta, f), encoding="utf-8"))
        if not re.fullmatch(r"[a-z]{2}(-[A-Z]{2})?", d.get("codigo", "")) or not isinstance(d.get("textos"), dict):
            fallas += 1
            print(f"✗ {f}: falta 'codigo' o 'textos'")
            continue
        idiomas.append({"codigo": d["codigo"], "nombre": d["nombre"], "bandera": d.get("bandera", ""),
                        "textos": len(d["textos"]), "version": hashlib.sha1(open(os.path.join(carpeta, f), "rb").read()).hexdigest()[:10]})
        print(f"✓ {f}")
    json.dump(idiomas, open(os.path.join(carpeta, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sys.exit(1 if fallas else 0)


if __name__ == "__main__":
    main()
