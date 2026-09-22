"""Genera cinco diagramas detallados como DOT y, con Graphviz, SVG/PNG.

Los diagramas son de DISEÑO. No representan servicios ya desplegados ni un
ESP32 físico ya programado.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import graphviz


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "generated" / "diagramas"


def nuevo(titulo: str, orientacion: str = "LR") -> graphviz.Digraph:
    diagrama = graphviz.Digraph(comment=titulo)
    diagrama.attr(rankdir=orientacion, bgcolor="white", pad="0.25", nodesep="0.45", ranksep="0.65")
    diagrama.attr("node", shape="box", style="rounded,filled", fontname="Arial", fontsize="11", color="#334155")
    diagrama.attr("edge", color="#64748b", fontname="Arial", fontsize="9", arrowsize="0.8")
    return diagrama


def arquitectura() -> graphviz.Digraph:
    d = nuevo("01 · Arquitectura del proyecto")
    with d.subgraph(name="cluster_offline") as s:
        s.attr(label="Laboratorio offline", color="#93c5fd", style="rounded")
        s.node("datos", "Contraseñas sintéticas\n(casos de prueba)", fillcolor="#dbeafe")
        s.node("hashes", "Hashes de prueba\nSHA-256: caso débil\nArgon2id: ampliación", fillcolor="#dbeafe")
        s.node("motor", "Estrategias acotadas\nCPU / GPU opcional", fillcolor="#dbeafe")
        s.edges([("datos", "hashes"), ("hashes", "motor")])
    with d.subgraph(name="cluster_online") as s:
        s.attr(label="Demostración online", color="#86efac", style="rounded")
        s.node("teclado", "Teclado o programa\nde prueba", fillcolor="#dcfce7")
        s.node("esp", "ESP32 propio\nvalida PIN", fillcolor="#dcfce7")
        s.node("salida", "LED / servo\nresultado de acceso", fillcolor="#dcfce7")
        s.edges([("teclado", "esp"), ("esp", "salida")])
    d.node("metricas", "CSV: intentos, tiempo,\nestados y logs", fillcolor="#fef3c7")
    d.node("panel", "Gráficas e informe", fillcolor="#f3e8ff")
    d.edge("motor", "metricas")
    d.edge("esp", "metricas", label="eventos")
    d.edge("metricas", "panel")
    return d


def proceso_offline() -> graphviz.Digraph:
    d = nuevo("02 · Método del experimento offline", "TB")
    pasos = [
        ("a", "1. Definir categorías\ny semilla reproducible"),
        ("b", "2. Crear claves ficticias\ny hashes propios"),
        ("c", "3. Fijar máximo de candidatos\ny tiempo"),
        ("d", "4. Probar fuerza bruta,\ndiccionario, máscaras y reglas"),
        ("e", "5. Guardar intentos, tiempo\ny resultado de cada caso"),
        ("f", "6. Comparar resultados\ny declarar límites"),
    ]
    for numero, (clave, texto) in enumerate(pasos):
        color = "#dbeafe" if numero < 3 else "#fef3c7"
        d.node(clave, texto, fillcolor=color)
    d.edges([(pasos[i][0], pasos[i + 1][0]) for i in range(len(pasos) - 1)])
    return d


def patron_humano() -> graphviz.Digraph:
    d = nuevo("03 · Efecto de un patrón humano", "TB")
    d.node("clave", "Ejemplo ficticio:\nLuna2026!", fillcolor="#fef3c7")
    d.node("general", "Ruta A: combinaciones generales\n(acotadas para la demo)", fillcolor="#dbeafe")
    d.node("patron", "Ruta B: priorizar\npalabra + año + símbolo", fillcolor="#dcfce7")
    d.node("medir", "Comparar candidatos probados\ny tiempo observado", fillcolor="#f3e8ff")
    d.edge("clave", "general", label="sin patrón")
    d.edge("clave", "patron", label="con patrón")
    d.edge("general", "medir")
    d.edge("patron", "medir")
    return d


def estados_esp32() -> graphviz.Digraph:
    d = nuevo("04 · Estados del acceso ESP32", "LR")
    d.node("listo", "Disponible", fillcolor="#dcfce7")
    d.node("espera", "Espera tras fallo", fillcolor="#fef3c7")
    d.node("bloqueo", "Bloqueo temporal", fillcolor="#fee2e2")
    d.node("acceso", "Acceso concedido", fillcolor="#dbeafe")
    d.edge("listo", "acceso", label="PIN correcto")
    d.edge("listo", "espera", label="PIN incorrecto")
    d.edge("espera", "listo", label="termina espera")
    d.edge("espera", "bloqueo", label="umbral alcanzado")
    d.edge("bloqueo", "listo", label="termina bloqueo")
    d.edge("acceso", "listo", label="fin de sesión")
    return d


def despliegue() -> graphviz.Digraph:
    d = nuevo("05 · Equipos y conexión opcional")
    with d.subgraph(name="cluster_universidad") as s:
        s.attr(label="Universidad", color="#93c5fd", style="rounded")
        s.node("laptop", "Laptop\ndashboard y presentación", fillcolor="#dbeafe")
        s.node("esp32", "ESP32\ndemo física local", fillcolor="#dbeafe")
        s.edge("esp32", "laptop", label="eventos")
    with d.subgraph(name="cluster_casa") as s:
        s.attr(label="Casa", color="#fdba74", style="rounded")
        s.node("pc", "PC i7 + RTX 4060\nexperimentos", fillcolor="#ffedd5")
        s.node("resultados", "Resultados CSV", fillcolor="#ffedd5")
        s.edge("pc", "resultados")
    d.node("vpn", "VPN privada\nSSH para administración", fillcolor="#dcfce7")
    d.edge("laptop", "vpn", style="dashed", label="opcional")
    d.edge("vpn", "pc", style="dashed")
    d.edge("resultados", "laptop", style="dotted", label="copiar o sincronizar")
    return d


DIAGRAMAS = {
    "01_arquitectura": arquitectura,
    "02_proceso_offline": proceso_offline,
    "03_patron_humano": patron_humano,
    "04_estados_esp32": estados_esp32,
    "05_despliegue": despliegue,
}


def generar_diagramas(carpeta: Path = DEFAULT_OUTPUT) -> Path:
    carpeta.mkdir(parents=True, exist_ok=True)
    hay_dot = shutil.which("dot") is not None
    for nombre, fabrica in DIAGRAMAS.items():
        diagrama = fabrica()
        fuente = Path(diagrama.save(filename=f"{nombre}.dot", directory=str(carpeta)))
        if hay_dot:
            for formato in ("svg", "png"):
                destino = fuente.with_suffix(f".{formato}")
                graphviz.render("dot", formato, str(fuente), outfile=str(destino))
            print(f"{nombre}: DOT, SVG y PNG")
        else:
            print(f"{nombre}: DOT (instala Graphviz y verifica 'dot -V' para SVG/PNG)")
    return carpeta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(f"Diagramas: {generar_diagramas(args.salida)}")
