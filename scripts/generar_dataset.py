"""Crea un conjunto pequeño y reproducible de credenciales FICTICIAS.

SHA-256 directo se usa aquí como caso didáctico de hash rápido; no es una
recomendación para almacenar contraseñas reales.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "generated" / "dataset.csv"

# Son ejemplos inventados; no se toman de usuarios, filtraciones o servicios.
CASOS = (
    ("C01", "palabra_comun", "sol", "Palabra corta y frecuente"),
    ("C02", "patron_humano", "Luna2026!", "Nombre ficticio + año + símbolo"),
    ("C03", "patron_humano", "Roca2025#", "Palabra ficticia + año + símbolo"),
    ("C04", "patron_humano", "Milo2024!", "Nombre ficticio + año + símbolo"),
    ("C05", "sin_patron_humano", "v7Q2", "Cadena corta sin el patrón anterior"),
)


def sha256_hex(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def generar_dataset(salida: Path = DEFAULT_OUTPUT) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=["id", "categoria", "clave_ficticia", "hash_sha256", "explicacion"],
        )
        escritor.writeheader()
        for identificador, categoria, clave, explicacion in CASOS:
            escritor.writerow(
                {
                    "id": identificador,
                    "categoria": categoria,
                    "clave_ficticia": clave,
                    "hash_sha256": sha256_hex(clave),
                    "explicacion": explicacion,
                }
            )
    return salida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(f"Dataset ficticio: {generar_dataset(args.salida)}")
