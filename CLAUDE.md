# Catálogo de Minuta

Repo **público** con universos e idiomas que la app Minuta descarga a pedido. Solo datos JSON, validados por la app al descargar.
El proyecto principal (y su `CLAUDE.md` con la arquitectura y los agentes) está en el repo `minuta`.

- `universos/<id>.json` + `universos/index.json` (vista previa sin descargar).
- `idiomas/<codigo>.json` + `idiomas/index.json`. `idiomas/en.json` es la referencia: debe ser igual a `ui/idiomas/en.json` de la app.
- `herramientas/generar_indice.py`: valida y regenera índices. Córrelo antes de cada commit.
- `herramientas/traducir_idioma.py <codigo> "<Nombre>" "<bandera>"`: crea un idioma con la IA del usuario.

Reglas: nada personal del usuario ni de su trabajo (es público); universos como homenajes breves de fans; nunca código ni HTML en los JSON.
Commits en español, autor con correo `@users.noreply.github.com`.
