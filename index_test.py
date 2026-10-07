#!/usr/bin/env python3
"""
================================================================================
Nombre completo : Emiliano Montaño Cuellar
Fecha           : 24 de septiembre de 2026
Materia/Examen  : Examen 1 - Frases Célebres

Descripción:
    Programa que administra un listado de frases célebres y la película en la
    que se dijeron. Permite buscar frases por palabra, agregar nuevas frases
    (guardándolas en un archivo CSV), desplegar estadísticas (palabras
    distintas, número de frases, número de películas distintas) y desplegar
    las frases agrupadas por película, ordenadas de mayor a menor cantidad
    de frases. La interfaz de usuario está construida con la librería
    Textual (interfaz de texto / TUI).

Modo de uso:
    python index_test.py -i frases_celebres.csv -o frases_corregidas.csv

    -i / --input   Archivo CSV de entrada con las frases (columnas: frase,pelicula)
    -o / --output  Archivo CSV de salida donde se guardarán los cambios
                    (si se agregan frases nuevas). Si no se indica, se usa
                    el mismo archivo de entrada.

Formato esperado del CSV (con encabezado):
    frase,pelicula
    "Que la fuerza te acompañe","Star Wars"
    "Houston, tenemos un problema","Apolo 13"

Declaración de uso de Inteligencia Artificial Generativa:
    Este programa fue generado con la asistencia de Claude (modelo
    "Claude Sonnet 5", Anthropic), como herramienta de apoyo para la
    generación del código conforme a los requisitos del examen. El
    estudiante debe revisar, entender y ajustar el código generado para asegurar que cumpla con los
    requisitos del examen y con las buenas prácticas de programación.
================================================================================
"""

import argparse
import csv
import os
import re
import unicodedata
from collections import Counter

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, VerticalScroll, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Button,
    Static,
    Input,
    ListView,
    ListItem,
    Label,
    DataTable,
)
from textual import on


# =============================================================================
# CLASE PARA MANEJAR CADA REGISTRO DE FRASE / PELICULA
# =============================================================================
class Frase:
    """Representa una frase célebre y la película de la que proviene."""

    def __init__(self, texto: str, pelicula: str):
        self.texto = texto.strip()
        self.pelicula = pelicula.strip()

    def contiene_palabra(self, palabra: str) -> bool:
        """Devuelve True si 'palabra' aparece como palabra completa en el
        texto de la frase (sin distinguir mayúsculas/minúsculas)."""
        patron = r"\b" + re.escape(palabra.lower()) + r"\b"
        return re.search(patron, self.texto.lower()) is not None

    def palabras(self):
        """Devuelve el conjunto de palabras (en minúsculas) de la frase."""
        return re.findall(r"[a-záéíóúüñ0-9]+", self.texto.lower())

    def __str__(self) -> str:
        return f'"{self.texto}"  —  ({self.pelicula})'

    def __repr__(self) -> str:
        return f"Frase(texto={self.texto!r}, pelicula={self.pelicula!r})"


# =============================================================================
# FUNCIONES DE LECTURA Y ESCRITURA DE ARCHIVOS CSV
# =============================================================================
def _normalizar_encabezado(texto: str) -> str:
    """Normaliza un nombre de columna: quita espacios, pasa a minúsculas y
    elimina acentos/tildes, para poder comparar encabezados de forma
    flexible (p. ej. 'Película', 'PELICULA' y 'pelicula' se consideran igual)."""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto


def leer_csv(ruta: str) -> list[Frase]:
    """Lee un archivo CSV con una columna de frase y otra de película y
    devuelve una lista de objetos Frase. Si el archivo no existe, devuelve
    una lista vacía.

    Es tolerante a: archivos con BOM (UTF-8 con marca de orden de bytes,
    típico al exportar desde Excel), encabezados con acentos/tildes
    ('Película' vs 'pelicula') y encabezados en mayúsculas o minúsculas."""
    frases: list[Frase] = []
    if not os.path.isfile(ruta):
        return frases

    # encoding="utf-8-sig" descarta el BOM si existe, y funciona igual que
    # utf-8 normal si el archivo no tiene BOM.
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        if not lector.fieldnames:
            return frases

        # Mapear cada encabezado normalizado a su nombre real en el archivo
        mapa_encabezados = {
            _normalizar_encabezado(nombre): nombre for nombre in lector.fieldnames
        }

        col_frase = mapa_encabezados.get("frase")
        col_pelicula = mapa_encabezados.get("pelicula")

        if col_frase is None or col_pelicula is None:
            raise ValueError(
                f"El archivo '{ruta}' debe tener columnas 'frase' y 'pelicula' "
                f"(se encontraron: {lector.fieldnames})"
            )

        for fila in lector:
            texto = fila.get(col_frase) or ""
            pelicula = fila.get(col_pelicula) or ""
            if texto.strip():
                frases.append(Frase(texto, pelicula))
    return frases


def escribir_csv(ruta: str, frases: list[Frase]) -> None:
    """Escribe la lista de objetos Frase en un archivo CSV con encabezado."""
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["Frase", "Película"])
        for fr in frases:
            escritor.writerow([fr.texto, fr.pelicula])


# =============================================================================
# FUNCIONES DE ESTADÍSTICAS
# =============================================================================
def contar_palabras_distintas(frases: list[Frase]) -> int:
    palabras = set()
    for fr in frases:
        palabras.update(fr.palabras())
    return len(palabras)


def contar_peliculas_distintas(frases: list[Frase]) -> int:
    return len({fr.pelicula.lower() for fr in frases if fr.pelicula})


def frases_por_pelicula(frases: list[Frase]) -> list[tuple[str, int]]:
    """Devuelve lista de (pelicula, cantidad_de_frases) ordenada de mayor
    a menor cantidad de frases."""
    contador = Counter(fr.pelicula for fr in frases if fr.pelicula)
    return sorted(contador.items(), key=lambda par: par[1], reverse=True)


# =============================================================================
# PANTALLA: MENÚ PRINCIPAL
# =============================================================================
class MenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Static("🎬  Frases Célebres — Menú Principal", id="titulo"),
            Static(f"Archivo de entrada: {self.app.ruta_entrada}", classes="info"),
            Static(f"Archivo de salida:  {self.app.ruta_salida}", classes="info"),
            Button("🔍  Buscar palabra", id="buscar", variant="primary"),
            Button("➕  Agregar frase", id="agregar", variant="success"),
            Button("📊  Estadísticas", id="estadisticas", variant="warning"),
            Button("🎞️  Frases por película", id="peliculas"),
            Button("💾  Guardar y salir", id="salir", variant="error"),
            id="menu-container",
        )
        yield Footer()

    @on(Button.Pressed)
    def manejar_boton(self, evento: Button.Pressed) -> None:
        id_boton = evento.button.id
        if id_boton == "buscar":
            self.app.push_screen(BuscarScreen())
        elif id_boton == "agregar":
            self.app.push_screen(AgregarScreen())
        elif id_boton == "estadisticas":
            self.app.push_screen(EstadisticasScreen())
        elif id_boton == "peliculas":
            self.app.push_screen(PeliculasScreen())
        elif id_boton == "salir":
            self.app.guardar_y_salir()


# =============================================================================
# PANTALLA: BUSCAR PALABRA
# =============================================================================
class BuscarScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("🔍  Buscar palabra en las frases", id="titulo"),
            Input(placeholder="Escribe una palabra y presiona Enter...", id="input-buscar"),
            Static("", id="resultado-conteo", classes="info"),
            VerticalScroll(ListView(id="lista-resultados"), id="scroll-resultados"),
            Button("⬅️  Regresar al menú", id="regresar"),
            id="contenedor-buscar",
        )
        yield Footer()

    @on(Input.Submitted, "#input-buscar")
    def buscar(self, evento: Input.Submitted) -> None:
        palabra = evento.value.strip()
        lista = self.query_one("#lista-resultados", ListView)
        etiqueta = self.query_one("#resultado-conteo", Static)
        lista.clear()

        if not palabra:
            etiqueta.update("Escribe una palabra para buscar.")
            return

        encontradas = [fr for fr in self.app.frases if fr.contiene_palabra(palabra)]

        if not encontradas:
            etiqueta.update(f"No se encontraron frases con la palabra '{palabra}'.")
        else:
            etiqueta.update(f"Se encontraron {len(encontradas)} frase(s) con '{palabra}':")
            for fr in encontradas:
                lista.append(ListItem(Label(str(fr))))

    @on(Button.Pressed, "#regresar")
    def regresar(self) -> None:
        self.app.pop_screen()


# =============================================================================
# PANTALLA: AGREGAR NUEVA FRASE
# =============================================================================
class AgregarScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("➕  Agregar una nueva frase", id="titulo"),
            Label("Frase:"),
            Input(placeholder="Escribe la frase célebre...", id="input-frase"),
            Label("Película:"),
            Input(placeholder="Escribe el nombre de la película...", id="input-pelicula"),
            Static("", id="mensaje-agregar", classes="info"),
            Horizontal(
                Button("💾  Guardar frase", id="guardar-frase", variant="success"),
                Button("⬅️  Regresar al menú", id="regresar"),
            ),
            id="contenedor-agregar",
        )
        yield Footer()

    @on(Button.Pressed, "#guardar-frase")
    def guardar_frase(self) -> None:
        input_frase = self.query_one("#input-frase", Input)
        input_pelicula = self.query_one("#input-pelicula", Input)
        mensaje = self.query_one("#mensaje-agregar", Static)

        texto = input_frase.value.strip()
        pelicula = input_pelicula.value.strip()

        if not texto or not pelicula:
            mensaje.update("⚠️  Debes llenar tanto la frase como la película.")
            return

        nueva = Frase(texto, pelicula)
        self.app.frases.append(nueva)
        escribir_csv(self.app.ruta_salida, self.app.frases)

        mensaje.update(f"✅  Frase agregada y guardada en '{self.app.ruta_salida}'.")
        input_frase.value = ""
        input_pelicula.value = ""
        input_frase.focus()

    @on(Button.Pressed, "#regresar")
    def regresar(self) -> None:
        self.app.pop_screen()


# =============================================================================
# PANTALLA: ESTADÍSTICAS
# =============================================================================
class EstadisticasScreen(Screen):
    def compose(self) -> ComposeResult:
        frases = self.app.frases
        num_frases = len(frases)
        num_palabras = contar_palabras_distintas(frases)
        num_peliculas = contar_peliculas_distintas(frases)

        yield Header()
        yield Vertical(
            Static("📊  Estadísticas generales", id="titulo"),
            Static(f"📝  Número total de frases:            {num_frases}", classes="stat"),
            Static(f"🔤  Número de palabras distintas:      {num_palabras}", classes="stat"),
            Static(f"🎬  Número de películas distintas:     {num_peliculas}", classes="stat"),
            Button("⬅️  Regresar al menú", id="regresar"),
            id="contenedor-stats",
        )
        yield Footer()

    @on(Button.Pressed, "#regresar")
    def regresar(self) -> None:
        self.app.pop_screen()


# =============================================================================
# PANTALLA EXTRA: FRASES POR PELÍCULA (ordenadas de mayor a menor)
# =============================================================================
class PeliculasScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Vertical(
            Static("🎞️  Frases por película (mayor a menor)", id="titulo"),
            DataTable(id="tabla-peliculas"),
            Button("⬅️  Regresar al menú", id="regresar"),
            id="contenedor-peliculas",
        )
        yield Footer()

    def on_mount(self) -> None:
        tabla = self.query_one("#tabla-peliculas", DataTable)
        tabla.add_columns("Película", "Cantidad de frases", "Frases")
        conteo = frases_por_pelicula(self.app.frases)

        for pelicula, cantidad in conteo:
            textos = [fr.texto for fr in self.app.frases if fr.pelicula == pelicula]
            resumen = " | ".join(textos)
            if len(resumen) > 80:
                resumen = resumen[:77] + "..."
            tabla.add_row(pelicula, str(cantidad), resumen)

    @on(Button.Pressed, "#regresar")
    def regresar(self) -> None:
        self.app.pop_screen()


# =============================================================================
# APLICACIÓN PRINCIPAL
# =============================================================================
class FrasesApp(App):
    CSS = """
    #titulo {
        text-style: bold;
        color: $accent;
        content-align: center middle;
        height: 3;
        width: 100%;
        padding-top: 1;
    }
    .info {
        color: $text-muted;
        padding: 0 1;
    }
    .stat {
        padding: 1 2;
        text-style: bold;
    }
    #menu-container, #contenedor-buscar, #contenedor-agregar,
    #contenedor-stats, #contenedor-peliculas {
        align: center top;
        padding: 1 4;
    }
    Button {
        width: 50%;
        margin: 1 2;
    }
    #scroll-resultados {
        height: 1fr;
        border: solid $accent;
        margin: 1 2;
    }
    Input {
        margin: 0 2 1 2;
    }
    DataTable {
        height: 1fr;
        margin: 1 2;
    }
    """

    BINDINGS = [("q", "quit_app", "Salir")]

    def __init__(self, ruta_entrada: str, ruta_salida: str):
        super().__init__()
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = ruta_salida
        self.frases: list[Frase] = leer_csv(ruta_entrada)

    def on_mount(self) -> None:
        self.push_screen(MenuScreen())

    def guardar_y_salir(self) -> None:
        escribir_csv(self.ruta_salida, self.frases)
        self.exit(message=f"Datos guardados en '{self.ruta_salida}'. ¡Hasta luego!")

    def action_quit_app(self) -> None:
        self.guardar_y_salir()


# =============================================================================
# PUNTO DE ENTRADA / ARGPARSE
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Administrador de frases célebres (interfaz Textual)."
    )
    parser.add_argument(
        "-i", "--input",
        dest="entrada",
        required=True,
        help="Archivo CSV de entrada con las frases (columnas: frase,pelicula)",
    )
    parser.add_argument(
        "-o", "--output",
        dest="salida",
        required=False,
        default=None,
        help="Archivo CSV de salida donde se guardarán los cambios (por defecto, el mismo de entrada)",
    )
    args = parser.parse_args()

    ruta_salida = args.salida if args.salida else args.entrada

    app = FrasesApp(ruta_entrada=args.entrada, ruta_salida=ruta_salida)
    app.run()


if __name__ == "__main__":
    main()
