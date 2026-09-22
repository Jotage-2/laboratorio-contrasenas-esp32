# Guía para explicar el proyecto al equipo

## La idea en 45 segundos

> Queremos estudiar dos problemas relacionados con la autenticación. Primero, algunas contraseñas parecen complejas, pero se construyen con patrones previsibles como una palabra, un año y un símbolo. Vamos a crear contraseñas ficticias y comparar cuántos candidatos prueban distintas estrategias antes de encontrar cada una. Segundo, vamos a construir una cerradura de prueba con ESP32 para mostrar qué ocurre cuando una interfaz permite intentos repetidos y cómo cambian las cosas al añadir espera, bloqueo y registros. Al final mostraremos los datos en gráficas y explicaremos las defensas que corresponden a cada escenario.

## Qué debe entender cada integrante

| Parte | Qué recibe | Qué hace | Qué entrega |
|---|---|---|---|
| Datos de prueba | Categorías definidas por el equipo | Genera claves inventadas y sus hashes | Dataset reproducible |
| Experimento offline | Hashes **propios** y cuatro estrategias | Prueba candidatos con un límite declarado | Intentos, tiempo y estado por caso |
| Prototipo ESP32 | PIN de prueba e intentos enviados al dispositivo | Autoriza o rechaza; aplica defensas según el modo | Estado de acceso y eventos |
| Visualización | CSV y eventos | Crea tablas y gráficas | Evidencia para exposición e informe |

**Importante:** el hash no se «desencripta». El laboratorio calcula el hash de cada candidato y compara el resultado con el hash de prueba. El ESP32 representa otra situación: intentos enviados a una interfaz online.

## Qué existe hoy y qué falta construir

| Ya está en este repositorio | Pendiente para el proyecto físico |
|---|---|
| Propuesta, diagramas Mermaid e imágenes SVG | Comprar o reunir ESP32, teclado e indicador |
| Scripts para datos ficticios y búsqueda acotada | Programar el firmware y probar los dos modos reales |
| Simulador Python de los estados del ESP32 | Conectar eventos reales del dispositivo al dashboard |
| Gráficas generadas con una demo sintética | Medir el hardware elegido y documentar resultados nuevos |
| Diagrama de conexión desde la universidad | Configurar VPN/SSH solo si se decide usar la PC de casa en vivo |

La comparación CPU/GPU, Argon2id, el firmware físico y el acceso remoto son ampliaciones. Los diagramas que los muestran explican **dónde encajarían**, no indican que ya estén implementados.

## Orden sugerido para una explicación de 6 a 8 minutos

1. **Problema (1 min):** mostrar una clave ficticia con patrón humano y preguntar si su longitud basta para considerarla fuerte.
2. **Arquitectura (1 min):** usar el [diagrama general](GALERIA.md#arquitectura-general) para señalar laboratorio, ESP32 y dashboard.
3. **Experimento offline (1–2 min):** explicar que todas las claves son inventadas, qué candidatos genera cada estrategia y cómo se cuentan intentos.
4. **Demostración online (1–2 min):** repetir la misma secuencia de PINes en modo inicial y protegido. Señalar en el registro cuándo se activa el bloqueo.
5. **Resultados y límites (1 min):** mostrar las gráficas de ejemplo como prueba de funcionamiento del software. Cuando existan resultados finales, sustituirlas por mediciones del proyecto.
6. **Conclusión (1 min):** vincular cada riesgo con su defensa y reconocer qué parte todavía falta implementar.

## Dos diferencias que conviene explicar con cuidado

### Patrón humano frente a longitud

Una cadena como `Luna2026!` tiene letras, números y símbolo. Sin embargo, si el formato `Palabra + Año + Símbolo` se conoce, una estrategia puede priorizar candidatos de esa forma. El prototipo enseña el **efecto del orden de búsqueda en cinco casos inventados**. No permite afirmar un tiempo universal para todas las contraseñas.

### Prueba offline frente a prueba online

| Escenario | Qué se prueba | Defensa relevante |
|---|---|---|
| Offline | Candidatos contra un hash de prueba ya disponible | Almacenar contraseñas con un algoritmo adecuado, como Argon2id, con salt y costo configurado |
| Online | PINes enviados a la interfaz del ESP32 | Limitar intentos, esperar, bloquear temporalmente y registrar eventos |

El límite de intentos del ESP32 **no protege por sí mismo** una copia de hashes que ya está fuera del dispositivo. El nuevo [diagrama de los dos escenarios](GALERIA.md#dos-escenarios-y-sus-defensas) está pensado para dejar esta diferencia clara ante el equipo y el profesor.

## Reparto de trabajo posible

No depende de un número exacto de integrantes. Una persona puede cubrir más de un módulo, o un módulo puede compartirse:

- **Experimentos:** dataset, estrategias, límites y lectura de resultados.
- **Dispositivo:** ESP32, teclado, indicador, modos y registro de eventos.
- **Visualización:** CSV, gráficas y explicación de cada figura.
- **Integración y documentación:** conectar piezas, controlar versiones, preparar la demo y el informe.

Antes de dividir el trabajo, acuerden un formato único de evento (`tiempo`, `modo`, `resultado`) y quién mantiene la versión de demostración que se usará en clase.

## Decisiones para conversar con el profesor

1. ¿Acepta un tema propio centrado en contraseñas predecibles y autenticación IoT?
2. ¿Qué profundidad espera en la implementación física del ESP32?
3. ¿Es necesario medir CPU/GPU o basta una comparación de estrategias y defensas?
4. ¿Se permite usar una PC doméstica de forma remota durante la presentación? Si no, la demo local sigue siendo viable.
5. ¿Qué evidencias concretas exige: logs, código, capturas, métricas, informe y video?

## Antes de presentar

- Ejecutar `python scripts/ejecutar_demo.py` y revisar los CSV y gráficas generados.
- Etiquetar todas las gráficas como **demo sintética** hasta reemplazarlas por mediciones finales.
- Probar el ESP32 real varias veces y tener un video corto como respaldo.
- Llevar los diagramas y el dashboard disponibles localmente por si falla Internet.
- Acordar quién explica cada módulo y quién responde preguntas sobre las limitaciones.
