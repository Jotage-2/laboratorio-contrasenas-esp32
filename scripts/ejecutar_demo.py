"""Ejecuta en orden las cinco etapas reproducibles del prototipo Python."""

from __future__ import annotations

from comparar_estrategias import comparar
from crear_graficas import crear_graficas
from generar_dataset import generar_dataset
from generar_diagramas import generar_diagramas
from simular_esp32 import simular


def main() -> None:
    print("1/5 · Crear dataset sintético")
    generar_dataset()
    print("2/5 · Comparar estrategias acotadas")
    comparar()
    print("3/5 · Simular acceso ESP32")
    simular()
    print("4/5 · Graficar resultados")
    crear_graficas()
    print("5/5 · Generar diagramas")
    generar_diagramas()
    print("Listo. Abre la carpeta generated/ para ver CSV, SVG y PNG.")


if __name__ == "__main__":
    main()
