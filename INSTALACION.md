# Instalación y ejecución de los scripts

## Requisitos

- Python 3.10 o posterior.
- Para **gráficas de resultados**: Matplotlib.
- Para **diagramas en SVG/PNG**: el paquete Python `graphviz` **y** el programa Graphviz instalado en el sistema. Son dos instalaciones distintas.
- Los scripts de generación de datos, comparación y simulación usan solo la biblioteca estándar de Python.

Los diagramas Mermaid de [DIAGRAMAS.md](DIAGRAMAS.md) ya se ven en GitHub sin instalar nada. Graphviz se usa para generar **archivos de imagen** descargables a partir de Python.

## Windows: preparar el entorno

Abre PowerShell en la carpeta del repositorio:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell no permite activar el entorno, puedes ejecutar directamente `.\.venv\Scripts\python.exe` en lugar de `python` en los comandos siguientes. No es necesario cambiar una política de seguridad de todo el sistema.

## Instalar Graphviz para las imágenes de diagramas

Descarga el instalador oficial para Windows en [graphviz.org/download](https://graphviz.org/download/). Durante la instalación, agrega la carpeta `bin` de Graphviz al `PATH` si el instalador ofrece esa opción. Abre una terminal nueva y comprueba:

```powershell
dot -V
python -c "import graphviz; print(graphviz.__version__)"
```

`import graphviz` comprueba el paquete Python; `dot -V` comprueba el programa que dibuja los diagramas. Si falla solo `dot -V`, revisa el `PATH` y reinicia la terminal. El script guardará los archivos `.dot` aunque falte el programa Graphviz; los SVG/PNG requieren `dot`.

## Ejecutar todo

Desde la raíz del repositorio:

```powershell
python scripts/ejecutar_demo.py
```

El comando crea `generated/` con dataset, resultados CSV, eventos de la simulación, diagramas y gráficas. Esa carpeta se ignora en Git para que no se confundan archivos de ejemplo con mediciones definitivas.

## Ejecutar cada etapa por separado

```powershell
python scripts/generar_dataset.py
python scripts/comparar_estrategias.py
python scripts/simular_esp32.py
python scripts/crear_graficas.py
python scripts/generar_diagramas.py
```

La comparación usa por defecto **un máximo de 50 000 candidatos por estrategia y contraseña**. Se puede cambiar para el propio dataset de laboratorio:

```powershell
python scripts/comparar_estrategias.py --max-intentos 100000
```

El simulador del ESP32 **no se conecta a un dispositivo real**: modela sus estados y escribe eventos para planificar la futura implementación del firmware. Tampoco hay un servicio SSH, VPN ni backend remoto en esta versión.

## Qué genera cada script

| Script | Entrada | Salida |
|---|---|---|
| `generar_dataset.py` | Casos sintéticos definidos en el código | `generated/dataset.csv` |
| `comparar_estrategias.py` | Dataset | `generated/resultados_estrategias.csv` |
| `simular_esp32.py` | Secuencia ficticia de PINes | `generated/eventos_esp32.csv` |
| `crear_graficas.py` | Ambos CSV de resultados | Gráficas SVG y PNG |
| `generar_diagramas.py` | Arquitectura definida en Python | Cinco diagramas `.dot`, SVG y PNG |
| `ejecutar_demo.py` | Ninguna | Ejecuta las cinco etapas anteriores |

## Fuentes de instalación

- [Instalación oficial de Matplotlib](https://matplotlib.org/stable/install/index.html)
- [Documentación del paquete Python Graphviz](https://graphviz.readthedocs.io/en/stable/)
- [Descarga oficial del programa Graphviz](https://graphviz.org/download/)
