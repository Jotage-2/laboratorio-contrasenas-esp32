# Informe breve del proyecto

## 1. Título propuesto

**Análisis experimental de contraseñas predecibles y defensas de autenticación mediante un prototipo ESP32**

## 2. Problema y pregunta

Las personas suelen construir contraseñas con información familiar: nombres, años, palabras comunes y símbolos al final. Una contraseña puede cumplir reglas de longitud y variedad de caracteres, pero conservar una estructura fácil de anticipar. Además, un sistema de acceso que admite intentos ilimitados permite probar candidatos repetidamente.

**Pregunta:** ¿Cómo influyen los patrones humanos en el esfuerzo de búsqueda de contraseñas y cuánto cambia una demostración de acceso cuando se introducen límites de intentos y registros?

## 3. Objetivo

Diseñar un laboratorio reproducible que compare estrategias de búsqueda sobre contraseñas ficticias y un prototipo físico que muestre mecanismos de protección ante intentos repetidos.

## 4. Componentes

### Laboratorio de contraseñas

- **Datos:** contraseñas sintéticas con categorías definidas antes de la prueba. No se usarán credenciales reales.
- **Almacenamiento de prueba:** hashes generados para el experimento. SHA-256 directo sirve como caso de estudio de almacenamiento débil; Argon2id permite estudiar un mecanismo diseñado para contraseñas.
- **Estrategias:** fuerza bruta acotada, diccionario sintético, máscaras y reglas de modificación.
- **Métricas:** intentos, tiempo, candidatos por segundo, porcentaje recuperado y configuración del equipo.
- **Hardware:** PC con i7-12700K y RTX 4060 si la comparación CPU/GPU aporta a la pregunta. La laptop universitaria puede utilizarse como equipo de visualización o segundo escenario, sujeto a autorización y disponibilidad.

### Prototipo ESP32

- ESP32, teclado numérico, LED o servo como indicador de acceso; pantalla opcional.
- **Modo inicial:** PIN de prueba e intentos sin límite.
- **Modo protegido:** retrasos o límites, bloqueo temporal y registro de eventos.
- Se repetirá una **secuencia controlada y acotada** de intentos en ambos modos para comparar su efecto.

### Visualización

Un dashboard sencillo mostrará los resultados de las pruebas offline y la línea de tiempo de los intentos al ESP32. Debe dejar claro que son experimentos distintos: la GPU acelera pruebas locales sobre hashes; el límite de intentos actúa sobre el dispositivo de acceso.

## 5. Método de evaluación

1. Definir categorías y generar el dataset con una semilla reproducible.
2. Definir antes de ejecutar el tiempo máximo, el número de candidatos y el criterio de éxito de cada estrategia.
3. Correr las pruebas y guardar configuración, logs y resultados. Repetir mediciones cuando haya variación relevante.
4. Comparar estrategias en condiciones equivalentes y señalar dónde las comparaciones no son directamente equivalentes.
5. Ejecutar la misma secuencia de PINes sobre el ESP32 en ambos modos.
6. Presentar resultados reales en tablas y gráficas; documentar fallos, límites y recomendaciones.

**Hipótesis de trabajo:** los patrones humanos pueden reducir los candidatos que se prueban antes de acertar, y las restricciones de intentos pueden aumentar el tiempo necesario para probar una secuencia en una interfaz online. Las magnitudes se determinarán experimentalmente.

## 6. Alcance y prioridades

| Prioridad | Entrega |
|---|---|
| Imprescindible | Dataset sintético, comparación de estrategias, métricas, ESP32 con dos modos y evidencias |
| Recomendable | Dashboard y comparación entre un hash rápido y Argon2id |
| Opcional | Medición CPU/GPU, pantalla o servo, alertas y acceso remoto a la PC de casa |

La ejecución remota desde la universidad es útil para la presentación, pero agrega dependencia de Internet, red y disponibilidad de la PC. Por ello se planifica después de tener la demostración local funcionando.

## 7. Riesgos de implementación

| Riesgo | Medida práctica |
|---|---|
| El hardware no está listo para la exposición | Preparar un indicador LED y un video corto de respaldo |
| Comparaciones injustas entre estrategias | Fijar dataset, límites, hardware y configuración; registrar diferencias |
| La GPU no aporta a todos los algoritmos por igual | Reportar los resultados por algoritmo y evitar generalizaciones |
| Fallo de Internet o PC remota | Ejecutar dashboard y demostración localmente |
| El alcance crece demasiado | Mantener primero una versión funcional pequeña |

## 8. Entregables

1. Código del generador, ejecutor de experimentos y firmware ESP32.
2. Dataset sintético, configuración, resultados y registros reproducibles.
3. Dashboard o conjunto de gráficas explicadas.
4. Informe técnico con arquitectura, método, resultados, límites, riesgos y recomendaciones.
5. Presentación y demostración funcional.

## 9. Referencias para el diseño

- [OWASP: Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP: Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
