# Seguridad del catálogo de Minuta

*(English below.)*

Este repo tiene los universos e idiomas que la app [Minuta](https://github.com/minuta-app/minuta) descarga. Son **solo datos**
(JSON): ningún archivo de aquí debe poder ejecutar código ni traer HTML a la app.

Si encuentras algo que se salte esa regla (un universo o idioma que haga algo raro en la app, una forma de que un JSON pase la
validación con HTML o CSS escondido, un problema en `herramientas/`), avísanos **en privado** en
[**Reportar una vulnerabilidad**](https://github.com/minuta-app/minuta-catalogo/security/advisories/new). No abras un issue
público ni un pull request con el detalle mientras no esté arreglado. Te respondemos dentro de una semana.

Cómo nos cuidamos:
- Todo entra por pull request y lo revisa una persona; las propuestas desde la app se importan con
  `herramientas/importar_propuesta.py`, que valida con las mismas reglas.
- `herramientas/generar_indice.py` rechaza claves desconocidas, textos con `<`, `>` o código y estilos que no sean colores,
  números, fuentes o patrones conocidos. GitHub lo corre en cada pull request, con permiso de solo lectura.
- La app vuelve a validar y limpiar cada universo al descargarlo y al mostrarlo.

---

**English:** this repo holds data-only JSON (universes and languages) downloaded by the Minuta app. If you find a way for
catalog content to run code or inject HTML/CSS into the app, or an issue in `herramientas/`, please report it privately via
[Report a vulnerability](https://github.com/minuta-app/minuta-catalogo/security/advisories/new) instead of a public issue.
We reply within a week.
