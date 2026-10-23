# Catálogo de Minuta

Universos e idiomas que [Minuta](https://github.com/minuta-app/minuta) descarga a pedido. Sin servidores: la app lee estos
archivos directamente desde GitHub y **solo acepta datos JSON** que pasan una validación (nunca código).

## Qué hay

| Carpeta | Contenido |
|---|---|
| `universos/` | Un archivo `<id>.json` por universo (rangos, arquetipos, logros, colores y forma de la ventana) + `index.json` con lo necesario para mostrar la vista previa sin descargar. |
| `idiomas/` | Paquetes de idioma de la interfaz: `{ codigo, nombre, bandera, textos: { "texto en español": "traducción" }, palabras }` + `index.json`. |
| `herramientas/` | `generar_indice.py` valida todo y regenera los índices. `traducir_idioma.py` crea un idioma nuevo con tu IA. |

## Aportar

- **Un universo nuevo:** créalo desde Minuta (Galería → Crear universo), copia el archivo de `~/minuta/temas/<id>.json` a
  `universos/`, quita las claves `creado`, `pedido` e `indicaciones`, corre `python3 herramientas/generar_indice.py` y abre un pull request.
- **Un idioma nuevo:** `python3 herramientas/traducir_idioma.py <codigo> "<Nombre>" "<bandera>"`, revisa el resultado y corre el generador de índices.
- **Errores e ideas:** abre un issue (desde Minuta: ⋯ → Enviar comentarios).

Los universos son homenajes de fans a sus obras: solo nombres, referencias y frases breves, con humor y cariño. Todas las marcas
y personajes pertenecen a sus dueños.

## Votar universos

Cada universo tiene un [issue de votos](https://github.com/minuta-app/minuta-catalogo/issues?q=label%3Avotos): reacciona con 👍 o 👎. Minuta muestra los votos en la galería y ordena los universos por descargar según lo que más le gusta a la comunidad.
