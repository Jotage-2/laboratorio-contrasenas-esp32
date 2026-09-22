"""Simula el control de acceso de un ESP32, sin conectar hardware real.

El reloj es virtual: no hay esperas reales ni envíos a una red. La misma
secuencia de PINes ficticios se ejecuta en dos configuraciones.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "generated" / "eventos_esp32.csv"
PIN_FICTICIO = "2005"
SECUENCIA = ((0, "1234"), (1, "0000"), (2, "2004"), (3, "2005"), (35, "2005"))


@dataclass
class ControlAcceso:
    modo: str
    fallos: int = 0
    disponible_desde: int = 0
    bloqueado_hasta: int = 0
    espera_segundos: int = 1
    umbral: int = 3
    bloqueo_segundos: int = 30

    def intentar(self, segundo: int, pin: str) -> dict:
        """Procesa exactamente un intento y devuelve un evento registrable."""
        if self.modo == "protegido" and segundo < self.bloqueado_hasta:
            resultado = "bloqueado"
        elif self.modo == "protegido" and segundo < self.disponible_desde:
            resultado = "en_espera"
        elif pin == PIN_FICTICIO:
            self.fallos = 0
            resultado = "acceso_concedido"
        else:
            self.fallos += 1
            resultado = "pin_incorrecto"
            if self.modo == "protegido":
                self.disponible_desde = segundo + self.espera_segundos
                if self.fallos >= self.umbral:
                    self.bloqueado_hasta = segundo + self.bloqueo_segundos
                    self.fallos = 0
                    resultado = "bloqueo_activado"
        return {
            "modo": self.modo,
            "segundo_virtual": segundo,
            "intento": pin,
            "resultado": resultado,
            "fallos_acumulados": self.fallos,
            "disponible_desde": self.disponible_desde,
            "bloqueado_hasta": self.bloqueado_hasta,
        }


def simular(salida: Path = DEFAULT_OUTPUT) -> Path:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=[
                "modo", "segundo_virtual", "intento", "resultado",
                "fallos_acumulados", "disponible_desde", "bloqueado_hasta",
            ],
        )
        escritor.writeheader()
        for modo in ("inicial", "protegido"):
            control = ControlAcceso(modo)
            for segundo, pin in SECUENCIA:
                evento = control.intentar(segundo, pin)
                escritor.writerow(evento)
                print(f"{modo:10} t={segundo:>2}s PIN={pin} -> {evento['resultado']}")
    return salida


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(f"Eventos simulados: {simular(args.salida)}")
