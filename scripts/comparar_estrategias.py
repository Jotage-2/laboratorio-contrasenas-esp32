"""Compara búsquedas ACOTADAS sobre hashes sintéticos generados por el equipo.

No acepta URLs, usuarios ni hashes externos. El objetivo es medir el orden
de candidatos de cuatro estrategias didácticas, no recuperar credenciales.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import time
from pathlib import Path
from typing import Iterable

from generar_dataset import DEFAULT_OUTPUT as DEFAULT_DATASET
from generar_dataset import sha256_hex


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "generated" / "resultados_estrategias.csv"

PALABRAS = ("sol", "luna", "roca", "milo", "mar", "nube")
ANIOS = ("2024", "2025", "2026")
SIMBOLOS = ("!", "#")


def fuerza_bruta() -> Iterable[str]:
    """Espacio pequeño declarado: minúsculas y dígitos, longitudes 1 a 4."""
    alfabeto = "abcdefghijklmnopqrstuvwxyz0123456789"
    for longitud in range(1, 5):
        for caracteres in itertools.product(alfabeto, repeat=longitud):
            yield "".join(caracteres)


def diccionario() -> Iterable[str]:
    """Lista fija de palabras, sin datos de personas reales."""
    yield from PALABRAS


def mascaras() -> Iterable[str]:
    """Estructura conocida: Palabra capitalizada + año + símbolo."""
    for palabra, anio, simbolo in itertools.product(PALABRAS, ANIOS, SIMBOLOS):
        yield f"{palabra.capitalize()}{anio}{simbolo}"


def reglas() -> Iterable[str]:
    """Mutaciones deterministas de un diccionario base."""
    for palabra in PALABRAS:
        yield palabra
        yield palabra.capitalize()
        for anio in ANIOS:
            yield f"{palabra}{anio}"
            yield f"{palabra.capitalize()}{anio}"
            for simbolo in SIMBOLOS:
                yield f"{palabra.capitalize()}{anio}{simbolo}"


ESTRATEGIAS = {
    "fuerza_bruta": fuerza_bruta,
    "diccionario": diccionario,
    "mascaras": mascaras,
    "reglas": reglas,
}


def evaluar(hash_objetivo: str, generador: Iterable[str], max_intentos: int) -> dict:
    inicio = time.perf_counter()
    intentos = 0
    encontrado = False
    for candidato in itertools.islice(generador, max_intentos):
        intentos += 1
        if sha256_hex(candidato) == hash_objetivo:
            encontrado = True
            break
    return {
        "encontrado": encontrado,
        "intentos": intentos,
        "segundos": round(time.perf_counter() - inicio, 6),
        "estado": "recuperada" if encontrado else "no recuperada dentro del limite",
    }


def comparar(
    dataset: Path = DEFAULT_DATASET,
    salida: Path = DEFAULT_OUTPUT,
    max_intentos: int = 50_000,
) -> Path:
    if max_intentos < 1:
        raise ValueError("--max-intentos debe ser positivo")
    if not dataset.is_file():
        raise FileNotFoundError(f"Falta {dataset}; ejecuta generar_dataset.py primero")

    with dataset.open(newline="", encoding="utf-8") as archivo:
        casos = list(csv.DictReader(archivo))
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=[
                "id", "categoria", "estrategia", "encontrado", "intentos",
                "segundos", "max_intentos", "estado",
            ],
        )
        escritor.writeheader()
        for caso in casos:
            for nombre, fabrica in ESTRATEGIAS.items():
                medicion = evaluar(caso["hash_sha256"], fabrica(), max_intentos)
                escritor.writerow(
                    {
                        "id": caso["id"],
                        "categoria": caso["categoria"],
                        "estrategia": nombre,
                        "max_intentos": max_intentos,
                        **medicion,
                    }
                )
                print(
                    f"{caso['id']} {nombre:14} "
                    f"{medicion['estado']:31} intentos={medicion['intentos']}"
                )
    return salida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--salida", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-intentos", type=int, default=50_000)
    args = parser.parse_args()
    print(f"Resultados: {comparar(args.dataset, args.salida, args.max_intentos)}")
