# Diagramas del proyecto

Los diagramas están escritos en Mermaid para que se vean directamente en GitHub y puedan editarse sin instalar programas de dibujo.

También hay [imágenes SVG generadas con los scripts de Python](GALERIA.md) listas para ver y descargar.

## 1. Visión general: cómo se conectan las partes

```mermaid
flowchart LR
    subgraph A[Laboratorio offline]
        D[Contraseñas ficticias] --> H[Hashes de prueba]
        H --> E[Experimentos de búsqueda]
        E --> M[Métricas]
    end
    subgraph B[Demostración online]
        T[Teclado o programa de prueba] --> P[ESP32 propio]
        P --> C[Indicador de acceso]
        P --> L[Eventos]
    end
    M --> V[Dashboard e informe]
    L --> V
```

El laboratorio permite estudiar la **predictibilidad** de una contraseña. El ESP32 permite observar cómo una interfaz de acceso responde a intentos repetidos. El dashboard reúne los resultados sin confundir ambos tipos de prueba.

## 2. Flujo del experimento con contraseñas

```mermaid
flowchart TD
    A[Definir categorías y semilla] --> B[Generar contraseñas sintéticas]
    B --> C[Crear hashes de prueba]
    C --> D[Definir límites de tiempo y candidatos]
    D --> E{Estrategia}
    E --> F[Fuerza bruta acotada]
    E --> G[Diccionario sintético]
    E --> H[Máscaras]
    E --> I[Reglas de modificación]
    F --> J[Guardar intentos, tiempo y resultado]
    G --> J
    H --> J
    I --> J
    J --> K[Comparar por tipo de contraseña]
```

Cada estrategia debe usar el mismo conjunto de prueba y límites declarados. Si una prueba no termina, se reporta como **no recuperada dentro del límite**, no como imposible de recuperar.

## 3. Cómo un patrón cambia el orden de búsqueda

```mermaid
flowchart LR
    X[Contraseña ficticia: Nombre2026!] --> Q{Información disponible}
    Q -->|Sin patrón conocido| B[Buscar combinaciones generales]
    Q -->|Patrón conocido| R[Priorizar nombre + año + símbolo]
    B --> C[Medir candidatos probados]
    R --> C
    C --> D[Comparar tiempo e intentos observados]
```

Este esquema **no afirma de antemano** un tiempo concreto: explica por qué cambia la prioridad de los candidatos. La conclusión cuantitativa saldrá de las mediciones.

## 4. Componentes del prototipo físico

```mermaid
flowchart LR
    K[Teclado numérico] --> E[ESP32]
    E --> V[Validador de PIN de prueba]
    V --> A[LED o servo]
    V --> R[Registro de intentos]
    V --> F[Control de espera y bloqueo]
    R --> W[Dashboard local]
    F --> W
```

El LED permite una primera versión simple; el servo y la pantalla pueden añadirse después. El PIN y las pruebas pertenecen exclusivamente al prototipo.

## 5. Estados de la autenticación protegida

```mermaid
stateDiagram-v2
    [*] --> Disponible
    Disponible --> Acceso: PIN correcto
    Disponible --> Espera: PIN incorrecto
    Espera --> Disponible: termina la espera
    Espera --> Bloqueado: se alcanza el umbral
    Bloqueado --> Disponible: termina el bloqueo
    Acceso --> Disponible: termina la sesión
```

En el modo inicial, el dispositivo pasa de un PIN incorrecto a otro intento sin espera. En el modo protegido, se registran el fallo, el retraso y el bloqueo. Los parámetros exactos se fijarán antes de medir y se mostrarán en el informe.

## 6. Secuencia de la demostración en clase

```mermaid
sequenceDiagram
    actor Expositor
    participant Control as Programa de prueba
    participant ESP as ESP32
    participant Panel as Dashboard
    Expositor->>ESP: Activa modo inicial
    Control->>ESP: Envía secuencia acotada de PINes
    ESP->>Panel: Registra respuestas y tiempos
    Panel-->>Expositor: Muestra resultado inicial
    Expositor->>ESP: Activa modo protegido
    Control->>ESP: Repite la misma secuencia
    ESP->>Panel: Registra esperas y bloqueos
    Panel-->>Expositor: Compara ambos modos
```

Se repite la misma secuencia para que la diferencia observable se deba al cambio de configuración del dispositivo.

## 7. Ubicación de los equipos y conexión opcional

```mermaid
flowchart LR
    subgraph U[Universidad]
        L[Laptop: presentación y dashboard]
        E[ESP32: demostración local]
    end
    subgraph C[Casa]
        PC[PC i7-12700K + RTX 4060]
        X[Experimentos y resultados]
        PC --> X
    end
    X -. Sincronización opcional .-> L
    E --> L
```

El proyecto puede presentarse con resultados preparados y la demo ESP32 local. La ejecución remota de nuevos experimentos durante la exposición es opcional y se incorporaría solo después de probar conectividad y permisos.

## 8. Qué defensa actúa en cada escenario

```mermaid
flowchart TD
    A[Intentos contra una interfaz online] --> B[Límites, espera, bloqueo y monitoreo]
    C[Copia de hashes obtenida en un escenario offline] --> D[Hashing de contraseñas con salt y costo adecuado]
    B --> E[Reduce intentos aceptados por la interfaz]
    D --> F[Eleva el costo de cada candidato probado]
```

Esta distinción es central para la exposición: limitar el ESP32 no cambia el costo de probar hashes fuera del dispositivo. Para el almacenamiento se evaluará un algoritmo diseñado para contraseñas, como Argon2id.
