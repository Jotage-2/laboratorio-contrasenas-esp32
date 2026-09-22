# Procesos implementados y cómo leer sus resultados

Este documento explica lo que **sí hace el prototipo Python actual** y lo que queda pendiente para el proyecto completo.

## 1. Creación de los casos ficticios

`scripts/generar_dataset.py` escribe `generated/dataset.csv`. Cada fila tiene identificador, categoría, clave inventada, hash SHA-256 y explicación. La clave aparece en el archivo para poder comprobar el ejercicio manualmente. No uses este formato para almacenar credenciales reales.

Los cinco ejemplos incluyen una palabra corta, tres cadenas con el patrón `Palabra + Año + Símbolo` y una cadena corta sin ese patrón. El conjunto es deliberadamente pequeño: muestra cómo funciona el proceso, **no permite estimar tasas de éxito para contraseñas reales**.

SHA-256 directo se usa como ejemplo de hash rápido y de almacenamiento débil. La comparación con Argon2id se propone como una fase futura; el prototipo todavía no la ejecuta.

## 2. Comparación de estrategias

`scripts/comparar_estrategias.py` lee únicamente el dataset creado arriba y aplica cuatro generadores de candidatos:

| Estrategia | Orden de candidatos en este prototipo | Qué enseña |
|---|---|---|
| Fuerza bruta acotada | Minúsculas y dígitos, longitudes 1 a 4 | Crecimiento del espacio de combinaciones y efecto del límite |
| Diccionario | Seis palabras ficticias fijas | Una palabra frecuente puede aparecer pronto |
| Máscaras | Palabra capitalizada + año + símbolo | Una estructura conocida concentra candidatos útiles |
| Reglas | Palabra base, capitalización y sufijos | Las mutaciones cambian el orden de búsqueda |

Para cada par de caso y estrategia, el programa compara el SHA-256 de cada candidato con el hash ficticio. Se detiene si encuentra una coincidencia o llega a `--max-intentos` (50 000 por defecto). Guarda `id`, `categoria`, `estrategia`, `encontrado`, `intentos`, `segundos`, `max_intentos` y `estado` en `generated/resultados_estrategias.csv`.

**Interpretación:** «no recuperada dentro del límite» significa que ese generador no la encontró con esos candidatos y ese tope. No significa que la clave sea segura. Los generadores tienen espacios y órdenes diferentes, diseñados para explicar conceptos; sus resultados no constituyen una comparación estadística representativa. Los tiempos de ejecuciones tan pequeñas también son sensibles al equipo y a otros procesos.

## 3. Simulación de la autenticación ESP32

`scripts/simular_esp32.py` ejecuta la misma secuencia de PINes ficticios en dos modos. Usa un **reloj virtual**: el segundo 35 no implica esperar 35 segundos al ejecutar el script.

| Modo inicial | Modo protegido |
|---|---|
| Cada intento se valida inmediatamente | Tras cada fallo se exige un segundo virtual de espera; tras tres fallos se activa un bloqueo temporal de 30 segundos virtuales |
| El cuarto PIN correcto concede acceso | El cuarto PIN se rechaza porque llega durante el bloqueo |
| No representa una defensa ante intentos repetidos | Los eventos registran fallos, bloqueo y acceso posterior |

La secuencia y los parámetros están declarados al inicio del script. La salida `generated/eventos_esp32.csv` registra tiempo virtual, modo, PIN ficticio, resultado, siguiente momento permitido y estado del bloqueo. Es **una simulación de lógica**, no firmware ni comunicación con un ESP32 real. En la implementación física habrá que comprobar relojes, reinicios, persistencia del estado y la conexión con el dashboard.

## 4. Gráficas basadas en los CSV

`scripts/crear_graficas.py` usa Matplotlib para guardar SVG y PNG de:

1. Casos recuperados dentro del límite por estrategia.
2. Candidatos probados en las recuperaciones exitosas.
3. Secuencia de estados del ESP32 simulado.

El script lee los CSV producidos por las etapas anteriores. Si faltan, se detiene con un error explicativo. No coloca tiempos o cantidades inventadas en las imágenes.

## 5. Diagramas de diseño generados con Graphviz

`scripts/generar_diagramas.py` crea seis archivos `.dot` y, si `dot` está instalado, las versiones SVG y PNG:

1. Arquitectura general de laboratorio, ESP32, métricas y dashboard.
2. Pasos del experimento offline.
3. Dos rutas de búsqueda para una contraseña con patrón humano.
4. Estados previstos para el modo protegido del ESP32.
5. Ubicación de equipos y conexión VPN/SSH opcional.
6. Separación entre las defensas de una prueba offline y una interfaz online.

Los diagramas muestran **la arquitectura propuesta**. El bloque VPN/SSH no es un servicio instalado por estos scripts; el bloque Argon2id señala una ampliación aún pendiente.

## 6. Cómo se une todo

`scripts/ejecutar_demo.py` llama las cinco etapas en orden. Sus archivos de salida se guardan en `generated/`, que Git ignora. Así, la propuesta, el código y los ejemplos visuales están disponibles en GitHub, mientras las ejecuciones nuevas quedan locales hasta que se revisen y se decida incorporarlas.
