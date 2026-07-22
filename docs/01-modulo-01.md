# MÓDULO 1: Arquitectura y Tipo de Sistema Operativo

## 1.1 Descripción del Escenario Real y Volumetría

El proyecto toma como escenario de aplicación real al **Hospital Regional Docente Materno Infantil El Carmen de Huancayo** (Junín, Perú), una institución de salud de alta especialización ginecoobstétrica y pediátrica[cite: 11].

### Volumetría Cuantificada
* **Concurrencia en Horas Pico (08:00 a.m. - 12:00 p.m.):** ~150 usuarios simultáneos (personal médico, enfermeros, farmacéuticos y administrativos)[cite: 11].
* **Carga Transaccional:** Entre 40 y 50 solicitudes de procesos por minuto[cite: 11].
* **Flujo de Telemetría (UCIN):** Transmisión continua de datos biométricos desde incubadoras en la Unidad de Cuidados Intensivos Neonatales cada 1,000 ms[cite: 11].
* **Restricción de Latencia:** Requerimiento de latencia determinista acotada ($\mu s$) para alertas de paros cardiorrespiratorios neonatales y Trauma Shock[cite: 11].

---

## 1.2 Justificación del Tipo de Sistema Operativo

Se justifica la selección de un **Sistema Operativo Híbrido con capacidades de Tiempo Real (RTOS)**[cite: 11].

### Criterios Técnicos de Selección
1. **Latencia Determinista (*Bounded Latency*):** Garantiza que el peor tiempo de ejecución (*WCET*) ante interrupciones de hardware biométrico esté rígidamente acotado en microsegundos[cite: 11].
2. **Manejo Estricto de Prioridades y Desalojo (*Preemption*):** El kernel suspende inmediatamente procesos de baja prioridad (ej. reportes epidemiológicos) ante alertas de Trauma Shock o UCIN[cite: 11].
3. **Soporte Masivo para Concurrencia Híbrida:** Coexistencia aislada entre flujos *I/O-bound* interactivos (triaje) y flujos continuos de datos de sensores[cite: 11].

### Comparativa con Alternativas Descartadas

| Criterio Técnico | Alternativa 1: SO por Lotes Puro (Batch) | Alternativa 2: Tiempo Compartido Estándar | Solución Propuesta: SO Híbrido / RTOS |
| :--- | :--- | :--- | :--- |
| **Mecanismo de Planificación** | Secuencial sin desalojo (FIFO)[cite: 11]. | Basado en justicia de tiempo (CFS)[cite: 11]. | Prioridades Estrictas con Desalojo Completo e Interrupciones Indexadas[cite: 11]. |
| **Comportamiento ante Emergencias** | Inviable. Espera a que terminen los lotes previos[cite: 11]. | Impredecible. Postergación por equidad de CPU[cite: 11]. | Inmediato. El kernel detiene procesos de menor jerarquía[cite: 11]. |
| **Procesamiento UCIN** | Nulo[cite: 11]. | Degradación por *overhead* y *jitter*[cite: 11]. | Determinista. Asignación periódica fija cada 1,000 ms[cite: 11]. |
| **Justificación del Descarte** | **RECHAZADO:** Latencia infinita inaceptable para emergencias[cite: 11]. | **RECHAZADO:** Introduce retrasos probabilísticos[cite: 11]. | **ACEPTADO:** Aísla entornos y blinda la telemetría[cite: 11]. |

---

## 1.3 Propuesta de Arquitectura Hardware

* **Procesador (CPU):** Multiprocesador simétrico (SMP) de 16 núcleos físicos (32 hilos) @ 3.0 GHz[cite: 11].
  * *Distribución de Núcleos:* 4 núcleos aislados para telemetría UCIN via afinidad de CPU, 8 núcleos para 150 usuarios concurrentes y 4 núcleos para BD distribuida e interfaz MINSA[cite: 11].
* **Memoria RAM:** 128 GB DDR5 ECC (4800 MHz)[cite: 11].
  * *Distribución:* $50 \times 250\text{ MB} = 12.5\text{ GB}$ para imágenes activas; $64\text{ GB}$ para *pool* de BD relacional; $51.5\text{ GB}$ para búferes de red y SO[cite: 11].
* **Almacenamiento:** Arreglo RAID 10 con 4 unidades SSD NVMe PCIe 4.0 de 2 TB (300,000 IOPS escritura aleatoria)[cite: 11].
* **Subsistema de Red:** Doble NIC 10 GbE en *Link Aggregation* (LACP / Active-Active Bonding) hasta 20 Gbps[cite: 11].

---

## 1.4 Arquitectura del Kernel

Se opta por un **Microkernel de Tiempo Real con Parche de Prioridades**[cite: 11].
* **Modo Usuario:** Drivers de hardware médico, controladores de red y sistemas de archivos operan aislados[cite: 11].
* **Modo Kernel:** Solo permanecen funciones mínimas: *scheduling*, interrupciones de hardware e IPC[cite: 11].
* **Protocolo de Herencia de Prioridades (*Priority Inheritance*):** Eleva temporalmente la prioridad de hilos secundarios si bloquean recursos requeridos por hilos de tiempo real, evitando inversiones de prioridad[cite: 11].

---

## 1.5 Diagrama de Arquitectura

```text
+-----------------------------------------------------------------------------------+
|                                 MODO USUARIO                                      |
|  [Terminal Admission/Triaje]    [Monitores UCIN (1000ms)]    [Estación Ecografía]  |
|               |                             |                             |       |
|        +--------------+              +--------------+              +------------+ |
|        | Driver Red   |              | App Telemetría|             | Base Datos | |
|        +--------------+              +--------------+              +------------+ |
+---------------+-----------------------------+-----------------------------+-------+
                | IPC                         | IPC                         | Alloc
+---------------+-----------------------------+-----------------------------+-------+
                |                             |                             |       |
|  +-----------------------------------------------------------------------------+  |
|  |                CORE SIMGESRC MICROKERNEL (PREEMPT_RT)                       |  |
|  |                                                                             |  |
|  |   +--------------------+    +--------------------+    +------------------+  |  |
|  |   | CPU Scheduler      |    | MMU Memory Manager |    | Sync Engine      |  |  |
|  |   | (RT / Preemption)  |    | (Paginación 4KB)   |    | (Mutex / Sem)    |  |  |
|  |   +--------------------+    +--------------------+    +------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
|                                  MODO KERNEL                                      |
+-----------------------------------------------------------------------------------+
