# Catálogo de Minuta

Repo **público** con universos e idiomas que la app Minuta descarga a pedido. Solo datos JSON, validados por la app al descargar.
El proyecto principal (y su `AGENTS.md`, la guía para personas y para cualquier IA) está en el repo `minuta`. `CLAUDE.md` y `GEMINI.md` solo importan este archivo.

- `temas/<categoria>/<id>.json` (la categoría es la carpeta: la primera de `categorias`, sin tildes) + `temas/index.json`.
- `idiomas/comunidad/<codigo>.json` (`id` = `codigo`) + `idiomas/catalogo.json`. `idiomas/comunidad/en.json` es la referencia: sus
  textos deben ser los de `ui/idiomas/en.json` de la app.
- Los índices son los de la pieza «catálogo» de Pieza: cada entrada con `ruta`, `sha256` y `tamano`; la app solo instala lo que calza.
  `herramientas/catalogo.py`, `nucleo.py`, `universo_formato.py` e `idioma_formato.py` son **los mismos archivos** que `bin/` de Minuta
  (`herramientas/app.json` es la sección `catalogo` de su `app.json`): si cambia un formato, cambia primero en Minuta y se copia aquí.
- `universos/`, `idiomas/<codigo>.json` e `index.json` (listas) los genera `generar_indice.py` para Minuta ≤ 0.3.1: no se editan.
- **Votos:** cada universo tiene un issue con la etiqueta `votos` y título `Votos: <Nombre> [<id>]`; los votos son sus reacciones 👍/👎
  y la app los lee de la API pública. Al agregar un universo, crea su issue (mismo formato) o no tendrá votos.
- `herramientas/generar_indice.py`: valida y regenera índices. Córrelo antes de cada commit.
- `herramientas/traducir_idioma.py <codigo> "<Nombre>" "<bandera>"`: crea un idioma con la IA del usuario.

Reglas: nada personal del usuario ni de su trabajo (es público); universos como homenajes breves de fans; nunca código ni HTML en los JSON.
Commits en español, autor con correo `@users.noreply.github.com`.
Revisión de pull requests de la comunidad: agente `minuta-revisor` del repo `minuta` (`.claude/agents/minuta-revisor.md`); nunca se junta sin aprobación de quien mantiene.
- **Propuestas desde la app:** issues con la etiqueta `propuesta` y un bloque ```json. `herramientas/importar_propuesta.py <n>` valida, pone
  `autor` y guarda `temas/<categoria>/<id>.json`; revísalo a mano (nada personal, homenaje breve), regenera índices, crea su issue de votos y cierra la propuesta.
