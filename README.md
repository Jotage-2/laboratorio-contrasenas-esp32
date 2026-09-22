# Laboratorio de contraseñas predecibles y defensas de autenticación

Proyecto universitario de ciberseguridad con dos demostraciones conectadas: un **análisis de contraseñas ficticias** y una **cerradura de prueba con ESP32**. El objetivo es explicar por qué una contraseña larga puede ser predecible y qué medidas protegen una interfaz de acceso.

> Estado: propuesta de proyecto. Las cifras y capturas de resultados se incorporarán después de ejecutar los experimentos; este repositorio no presenta mediciones inventadas.

## Lectura rápida

- [Informe breve: objetivo, método, alcance y entregables](INFORME.md)
- [Ocho diagramas explicados](DIAGRAMAS.md)
- [Galería: diagramas e imágenes creadas por Python](GALERIA.md)
- [Procesos y formato de los datos, paso a paso](PROCESOS.md)
- [Librerías, instalación y comandos](INSTALACION.md)

## Idea central

1. Generar contraseñas **sintéticas**: algunas aleatorias, otras basadas en palabras y otras en patrones como `Nombre + Año + Símbolo`.
2. Comparar estrategias de búsqueda, con límites de tiempo y el mismo conjunto de prueba, sobre hashes creados por el equipo.
3. Mostrar en un ESP32 propio la diferencia entre un acceso sin límite de intentos y otro con espera, bloqueo temporal y registro de eventos.
4. Presentar métricas reales, explicar las limitaciones y proponer defensas.

## Qué aporta cada demostración

| Parte | Pregunta que responde | Resultado visible |
|---|---|---|
| Laboratorio de hashes | ¿Cuánto ayuda conocer un patrón humano? | Intentos, tiempo y tasa de recuperación por estrategia |
| ESP32 | ¿Qué ocurre si el dispositivo permite intentos repetidos? | Accesos aceptados o rechazados, espera, bloqueo y eventos |
| Dashboard | ¿Cómo se comparan los escenarios? | Gráficas y línea de tiempo de la demostración |

**Distinción clave:** limitar intentos protege una interfaz de autenticación. Si una base de hashes se filtra, la defensa depende también de cómo se almacenaron las contraseñas; un algoritmo de derivación como Argon2id es más apropiado que SHA-256 directo para ese fin. Véanse las guías de [autenticación](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) y [almacenamiento de contraseñas](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) de OWASP.

## Demostración prevista

La exposición comienza con dos contraseñas de ejemplo, una aleatoria y otra con patrón humano. El equipo enseña qué estrategia prueba primero cada una y cuánto tardó **en el entorno medido**. Luego muestra una cerradura ESP32 en modo inicial y repite la misma secuencia de intentos con las defensas activadas. El dashboard reúne los resultados y los eventos del dispositivo.

Todas las cuentas, contraseñas, hashes y dispositivos usados en las pruebas pertenecerán al laboratorio del proyecto.

## Prototipo Python incluido

Los scripts de `scripts/` permiten ejecutar ya una demostración reproducible: crean cinco casos ficticios, comparan cuatro estrategias con un máximo de candidatos, simulan el control de acceso del ESP32 y generan imágenes de diagramas y gráficas. Las gráficas incluidas en la galería son **resultados de esa demostración sintética**. No son resultados de una RTX 4060 ni de un ESP32 físico.

```powershell
python -m pip install -r requirements.txt
python scripts/ejecutar_demo.py
```

Para los SVG/PNG de Graphviz también hace falta instalar el programa `dot`; consulta [INSTALACION.md](INSTALACION.md).
