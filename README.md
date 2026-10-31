# Catálogo de Minuta

Universos e idiomas que [Minuta](https://github.com/minuta-app/minuta) descarga a pedido. Sin servidores: la app lee estos
archivos directamente desde GitHub y **solo acepta datos JSON** que pasan una validación (nunca código).

## Qué hay

| Carpeta | Contenido |
|---|---|
| `temas/<categoria>/<id>.json` | Un archivo por universo (rangos, arquetipos, logros, colores y forma de la ventana). `categoria` es la carpeta: la primera de `categorias`, sin tildes (`peliculas`, `series`, `anime`…). `temas/index.json` es el índice: cada universo con su `ruta`, su huella `sha256` y su `tamano`. Minuta rechaza lo que no calce con su huella. |
| `idiomas/comunidad/<codigo>.json` | Paquetes de idioma de la interfaz: `{ id, categoria, codigo, nombre, bandera, textos: { "texto en español": "traducción" }, palabras }` (`id` = `codigo`). Índice con huellas: `idiomas/catalogo.json`. |
| `universos/`, `idiomas/<codigo>.json`, `index.json` | **Generados, no se editan:** el formato de antes, para Minuta 0.3.1 o anterior. |
| `herramientas/` | `generar_indice.py` valida todo y regenera los índices (con `catalogo.py`, la pieza «catálogo» de [Pieza](https://github.com/pieza-app/pieza), y los validadores `universo_formato.py` e `idioma_formato.py`, los mismos archivos que usa Minuta). `traducir_idioma.py` crea un idioma nuevo con tu IA. |

## Aportar

- **Un universo nuevo:** créalo desde Minuta (Galería → Crear universo) y tócale 📤 para proponerlo: llega como un issue con la
  etiqueta `propuesta` (con tu cuenta de GitHub si la conectaste en Minuta, o abriendo GitHub con todo listo). Lo revisamos y lo sumamos
  con `python3 herramientas/importar_propuesta.py <número>`, con tu usuario como autor. También puedes abrir un pull request a mano.
- **Un idioma nuevo:** `python3 herramientas/traducir_idioma.py <codigo> "<Nombre>" "<bandera>"`, revisa el resultado y corre el generador de índices.
- **Errores e ideas:** abre un issue (desde Minuta: ⋯ → Enviar comentarios).

Los universos son homenajes de fans a sus obras: solo nombres, referencias y frases breves, con humor y cariño. Todas las marcas
y personajes pertenecen a sus dueños.

## Votar universos

Cada universo tiene un [issue de votos](https://github.com/minuta-app/minuta-catalogo/issues?q=label%3Avotos): reacciona con 👍 o 👎 (o vota desde la vista previa en Minuta si conectaste tu GitHub). Minuta muestra los votos en la galería y ordena los universos por descargar según lo que más le gusta a la comunidad.

🔒 ¿Una falla de seguridad? Avísanos en privado: [SECURITY.md](SECURITY.md). · Security issues: please report them privately ([SECURITY.md](SECURITY.md)).
