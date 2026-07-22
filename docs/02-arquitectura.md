# MÓDULO 1: ARQUITECTURA Y TIPO DE SISTEMA OPERATIVO

### 1.1.2. Justificación Técnica de la Elección de un Sistema Operativo Híbrido / Tiempo Real (RTOS)
Para mitigar los riesgos de impredecibilidad temporal, el diseño del sistema SIMGESRC se fundamenta sobre un Sistema Operativo Híbrido con capacidades de Tiempo Real (RTOS). Esta decisión se justifica mediante tres criterios de ingeniería de sistemas de misión crítica:

1. **Latencia Determinista (Bounded Latency):** A diferencia de los sistemas operativos comerciales orientados al rendimiento promedio (*throughput*), un RTOS garantiza que el tiempo máximo de respuesta (*worst-case execution time* - WCET) ante una interrupción de hardware o software esté rígidamente acotado. En el contexto de la UCIN, la recepción de una ráfaga de signos vitales anómalos debe activar un cambio de contexto en el procesador en un intervalo de microsegundos ($\mu s$), asegurando que la notificación visual y auditiva en la central de monitoreo ocurra de manera inmediata e invariable.
2. **Manejo Estricto de Prioridades y Desalojo (Preemption):** El kernel elegido soporta planificación por prioridades con desalojo completo (*fully preemptible kernel*). Si la CPU se encuentra ejecutando un proceso de baja prioridad, como la generación de un reporte epidemiológico del MINSA, y se recibe una interrupción de Trauma Shock, el planificador (*scheduler*) suspende inmediatamente el proceso administrativo, guarda su bloque de control de proceso (PCB) y transfiere los ciclos de ejecución al proceso de emergencia. Esto elimina la latencia de despacho aleatoria.
3. **Soporte Masivo para Concurrencia Híbrida:** El sistema operativo debe coexistir con flujos de trabajo dispares: procesos I/O-bound interactivos (ingreso manual en el triaje) y procesos de flujo continuo de datos de sensores de red. La arquitectura híbrida combina un programador de tiempo compartido para el módulo administrativo con un despachador de tiempo real de alta prioridad para la telemetría, aislando ambos entornos de ejecución para evitar que la sobrecarga transaccional de la consulta externa degrade el rendimiento de los módulos críticos de monitoreo vital.

---

### 1.1.3. Tabla Comparativa de Esquemas de Sistemas Operativos Descartados
A continuación, se analizan y descartan formalmente dos alternativas arquitectónicas evaluadas para la implementación de SIMGESRC:

| Criterio Técnico | Alternativa 1: SO por Lotes Puro (Batch Processing) | Alternativa 2: SO de Tiempo Compartido Estándar (Escritorio / Servidor Convencional) | Solución Propuesta: SO Híbrido / Tiempo Real (RTOS) |
| :--- | :--- | :--- | :--- |
| **Mecanismo de Planificación** | Secuencial sin desalojo (FIFO masivo). | Planificadores basados en justicia de tiempo (*Completely Fair Scheduler* - CFS). | Planificación por Prioridades Estrictas con Desalojo Completo e Interrupciones Indexadas. |
| **Comportamiento ante Emergencias** | Inviable. La emergencia espera a que terminen los lotes previos en ejecución. | Impredecible. El proceso de emergencia puede ser postergado por algoritmos que priorizan la equidad de la CPU. | Inmediato. El kernel detiene cualquier proceso activo de menor jerarquía para despachar la alerta. |
| **Procesamiento de Telemetría (UCIN)** | Nulo. No maneja flujos interactivos continuos ni señales por segundo. | Degradación del rendimiento. Alto overhead por cambios de contexto masivos y fluctuaciones en la latencia (*jitter*). | Determinista. Asignación periódica fija garantizada cada 1,000 ms sin pérdida de paquetes. |
| **Justificación del Descarte Técnico** | **RECHAZADO:** Diseñado para alta eficiencia en tareas repetitivas de fondo (nóminas, backups). Su latencia infinita causaría el fallecimiento de pacientes críticos al no responder a interrupciones en tiempo real. | **RECHAZADO:** Aunque tolera 150 usuarios, prioriza la experiencia del usuario de escritorio. El algoritmo busca que todos los hilos avancen equitativamente, lo que introduce retrasos probabilísticos inaceptables en alertas médicas. | **ACEPTADO:** El aislamiento de entornos asegura la transaccionalidad de los 150 usuarios y blinda el determinismo de la telemetría neonatológica. |

---

### 1.2. Arquitectura Hardware Propuesta

#### 1.2.1. Dimensionamiento Cuantitativo e Infraestructura del Servidor Central
El servidor central del sistema SIMGESRC debe ser configurado para soportar los picos transaccionales y el flujo constante de telemetría sin riesgo de saturación. La propuesta de hardware se detalla de la siguiente manera:

- **Procesador (CPU):** Se requiere una arquitectura multiprocesador simétrica (SMP) con un procesador de 16 núcleos físicos (32 hilos lógicos) con una frecuencia base de 3.0 GHz.
  - *Justificación Cuantitativa:* El cálculo del paralelismo se realiza dividiendo los hilos en dominios de ejecución: 4 núcleos físicos se dedican exclusivamente a través de afinidad de CPU (*CPU affinity*) al procesamiento y despaquetizado de las tramas UDP/IP de la telemetría de la UCIN; 8 núcleos físicos gestionan la lógica transaccional de los 150 usuarios concurrentes en horas pico; 4 núcleos físicos se reservan para el sistema de base de datos distribuidos e interfaces con el MINSA.
- **Memoria RAM:** 128 GB DDR5 ECC (*Error Correcting Code*) a 4800 MHz.
  - *Justificación Cuantitativa:* Las tramas de telemetría ocupan poca memoria en búfer, pero las imágenes médicas (ecografías, tomografías y radiografías) cargadas por los médicos requieren un promedio de 250 MB por paciente en memoria activa ($50 \times 250 \text{ MB} = 12.5 \text{ GB}$). La base de datos relacional indexada en memoria para historias clínicas requiere un pool de 64 GB. El espacio restante (51.5 GB) se asigna para búferes de red, el SO y la prevención de fallos OOM. El uso de ECC corrige corrupción de bits por interferencias electromagnéticas.
- **Subsistema de Almacenamiento:** Arreglo RAID 10 compuesto por 4 unidades SSD NVMe PCIe 4.0 de 2 TB cada una.
  - *Justificación Cuantitativa:* RAID 10 proporciona lectura de doble canal y duplicación de datos (*mirroring*) exacta en caliente.
- **Subsistema de Red:** Doble tarjeta de red (NIC) de 10 GbE configurada en modo Link Aggregation (LACP / Active-Active Bonding) conectada a switches redundantes.

#### 1.2.2. Métricas de Rendimiento Esperadas y Análisis de Capacidad
- **Capacidad de Operaciones de E/S (IOPS):** El arreglo NVMe en RAID 10 garantiza un mínimo de 300,000 IOPS en escritura aleatoria.
- **Throughput de Red Sostenido:** El enlace agregado proporciona hasta 20 Gbps de ancho de banda teórico (~15 Mbps consumidos por telemetría).

---

### 1.3. Arquitectura del Kernel y Diagrama de Flujo

#### 1.3.1. Justificación de la Arquitectura del Kernel y Modos de Ejecución
Se opta por la implementación de un **Kernel de Tiempo Real Basado en Arquitectura Microkernel con Parche de Prioridades**. Los componentes tradicionales (sistemas de archivos, controladores de red, drivers) operan en **Modo Usuario**. En **Modo Kernel** solo permanecen la planificación (*scheduling*), gestión de interrupciones de hardware e IPC.

- **Aislamiento de Fallos:** Si un controlador de red sufre un fallo, queda confinado en Modo Usuario y se reinicia libremente sin colgar el kernel (*kernel panic*).
- **Mitigación de la Inversión de Prioridades:** Incorpora el *Priority Inheritance Protocol* para elevar temporalmente la prioridad de hilos bloqueantes.

#### 1.3.2. Descripción Textual del Flujo de Datos Arquitectónico
1. **Captura y Generación de Datos de Red:** Sensores biométricos envían tramas UDP cada 1,000 ms -> La NIC dispara una IRQ al procesador.
2. **Procesamiento en Modo Kernel:** El planificador intercepta la IRQ y aplica un desalojo (*preemption*) inmediato para el hilo de telemetría de la UCIN.
3. **Paso de Mensajes por IPC:** El kernel transfiere datos mediante memoria compartida protegida en Modo Usuario.
4. **Visualización en Tiempo Real:** El panel de enfermería se actualiza en un tiempo determinista $< 5 \text{ ms}$.
