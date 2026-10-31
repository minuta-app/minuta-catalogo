# Cómo aportar al catálogo

Aquí viven los universos y los idiomas que Minuta descarga. Son **solo datos** (JSON): no hace falta programar. *(English below.)*

## Universos
- Lo más fácil: créalo en la app (Universos → Crear universo), úsalo un par de reuniones y propónlo con **📤**. Llega como issue `propuesta`.
- Por pull request: agrega `temas/<categoria>/<id>.json` (la categoría es la primera de `categorias`, sin tildes, y va también en el campo `categoria`) y corre `python3 herramientas/generar_indice.py` (valida y regenera el índice).
- Reglas: homenaje breve de fan (nombres de personajes sí; letras de canciones o textos copiados no), 1 a 4 categorías de la lista,
  nada personal ni de empresas reales, tono amable.

## Idiomas
- `python3 herramientas/traducir_idioma.py <código> "<Nombre>" "<bandera>"` arma un idioma con tu IA a partir de `idiomas/en.json`.
- Revisa la traducción a mano: con tu IA queda bien, pero no perfecta. Deja sin traducir Minuta, Claude, Codex, Gemini, GitHub y GitLab,
  y respeta los `{n}` y `{x}`.
- Corre `python3 herramientas/generar_indice.py` y abre el pull request.

## Cómo revisamos
Todo entra por pull request y lo junta alguien que mantiene el proyecto. Revisamos que el JSON sea válido y solo de datos, que no haya
nada personal ni copiado, y en los idiomas pedimos que una persona que hable el idioma revise la traducción antes de juntarla.
Si algo falta te lo pedimos con un comentario.

**Fallas de seguridad:** nunca en un issue público; avísanos en privado como explica [SECURITY.md](SECURITY.md).

---

**English:** universes and languages are data-only JSON. Create a universe in the app and propose it with 📤, or open a pull request
with `temas/<category>/<id>.json` (the category is the first of `categorias`, without accents, also in the `categoria` field) after running `python3 herramientas/generar_indice.py`. For languages, use `herramientas/traducir_idioma.py`
and review the result by hand (keep brand names and `{n}`/`{x}`). A maintainer reviews every pull request; translations also get a
review from a native speaker.
Security issues: report them privately, see [SECURITY.md](SECURITY.md).
