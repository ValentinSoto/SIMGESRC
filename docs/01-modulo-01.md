# MÓDULO 1: Arquitectura y Tipo de Sistema Operativo

## 1.1 Descripción del Escenario Real y Volumetría

El proyecto toma como escenario de aplicación real al **Hospital Regional El Carmen de Huancayo** (Junín, Perú), un establecimiento de salud de Nivel II-2 que atiende emergencias, consultas externas y procedimientos quirúrgicos de alta complejidad en la Macroregión Centro.

### Volumetría Cuantificada
* **Atención Diaria:** ~1,200 pacientes/día distribuidos en 28 especialidades médicas.
* **Transacciones en Horas Pico (08:00 - 12:00 hrs):** ~18,000 transacciones/hora (consultas de historias clínicas, emisión de recetas, órdenes de laboratorio e ingreso de datos de triaje).
* **Concurrencia de Dispositivos:** 120 terminales médicas (PC) en consultorios + 45 dispositivos de telemetría de signos vitales (monitores de cabecera en UCI/SOP) y estaciones de transmisión de imágenes PACS/RIS.
* **Restricciones de Latencia:** 
  * *Triaje y Emergencias:* Tiempos de respuesta requeridos < 50 ms.
  * *Consultas Interactivas:* Tiempo de respuesta < 1.5 s.
  * *Procesamiento de Imágenes:* Procesamiento en segundo plano (*background*) sin afectar operaciones interactivas.

---

## 1.2 Justificación del Tipo de Sistema Operativo

Se justifica la selección de un **Sistema Operativo Híbrido en Tiempo Real y Tiempo Compartido (RTOS / Time-Sharing Hybrid OS)**.

### Criterios Técnicos de Selección (>= 3 Criterios)
1. **Determinismo y Latencia Acotada:** Los eventos provenientes de la UCI y Triaje requieren un kernel con expulsión (*preemptive kernel*) que garantice tiempos de respuesta acotados en microsegundos para evitar la pérdida de eventos críticos de vida o muerte.
2. **Multitarea Interactiva con Prioridades Dinámicas:** Permite atender simultáneamente a decenas de médicos consultando registros clínicos (interactivo) sin que la CPU sea acaparada por reportes nocturnos o renderizado de tomografías.
3. **Aislamiento de Memoria y Resiliencia:** Prevención de *kernel panics* o caídas del sistema completo si un controlador de un equipo médico especializado presenta una falla de software.

### Comparativa con Alternativas Descartadas

| Criterio Técnico | SO Seleccionado (Híbrido RTOS / Time-Sharing) | Alternativa Descartada 1: SO Batch Puro | Alternativa Descartada 2: RTOS Puro |
| :--- | :--- | :--- | :--- |
| **Razones de Descarte** | **ELEGIDO** | Incompatible con la interactividad médica. Imposibilita la atención inmediata en emergencias. | Ineficiente para gestionar grandes bases de datos transaccionales e interfaces gráficas complejas. |
| **Latencia de Interrupción** | < 10 µs | Indefinida (Horas/Minutos) | < 2 µs |
| **Uso de Memoria** | Moderado / Servidor | Bajo | Extremadamente bajo |
| **Soporte BD / GUI** | Completo (POSIX Compliant) | Nulo / Lote | Muy Limitado |

---

## 1.3 Propuesta de Arquitectura Hardware

Se plantea la siguiente configuración de hardware dimensionada para la volumetría del hospital:

* **Procesador (CPU):** 2x Intel Xeon Gold 6338 (Total 64 núcleos / 128 hilos @ 2.0GHz, Turbo 3.2GHz).
  * *Justificación:* Permite aislar núcleos físicos para hilos de tiempo real (UCI/SOP) y dedicar los núcleos restantes a hilos de procesamiento transaccional (Base de Datos / Web).
* **Memoria RAM:** 256 GB DDR4 ECC Registered (3200 MHz).
  * *Justificación:* Soporta tablas de paginación extensas, asignación de buffer cache en RAM para 18,000 transacciones/hora y memoria reservada para el almacenamiento de imágenes médicas en tránsito.
* **Almacenamiento:** Array NVMe SSD RAID 10 de 3.2 TB (Velocidad de Lectura: 6,800 MB/s, Escritura: 5,000 MB/s).
  * *Justificación:* Elimina cuellos de botella en operaciones I/O-Bound asociadas a la lectura y escritura concurrente de archivos de historias clínicas e imágenes DICOM.
* **Tarjeta de Red:** Interfaz Doble de 10 GbE SFP+ en modo *Bonding* / LACP.

### Comparativa de Costo / Rendimiento del Hardware
* **Inversión Estimada:** ~$14,500 USD.
* **Beneficio Técnico:** Garantiza un *throughput* continuo superior a 500 operaciones/segundo manteniendo la utilización global de la CPU por debajo del 65% durante picos de carga.

---

## 1.4 Justificación de la Arquitectura del Kernel

Se selecciona una arquitectura de **Microkernel Modificado (Híbrido estilo Linux Kernel PREEMPT_RT)**.

* **Componentes en Espacio de Kernel (*Kernel Space*):** Planificador (*Scheduler*), Gestión Básica de Memoria (MMU) y Manejador de Interrupciones Hardware.
* **Componentes en Espacio de Usuario (*User Space*):** Drivers de dispositivos médicos, Sistema de Archivos (ext4) y Pila de Protocolos de Red (TCP/IP).
* **SO Real de Referencia:** **Ubuntu Server 22.04 LTS con Parche PREEMPT_RT Real-Time Kernel**.

---

## 1.5 Diagrama de Arquitectura del Sistema

```text
+-----------------------------------------------------------------------------------+
|                                 ESPACIO DE USUARIO                                |
|  [Terminal Triaje]        [Monitor Telemetría UCI]        [Estación PACS/RIS]     |
|          |                            |                            |              |
|   +--------------+             +--------------+             +------------------+  |
|   | Interfaz GUI |             | Daemon Sync  |             | PostgreSQL / DICOM| |
|   +--------------+             +--------------+             +------------------+  |
+----------|----------------------------|----------------------------|--------------+
           | System Calls               | Mutex Locks                | Alloc / Free
+----------v----------------------------v----------------------------v--------------+
|                                 ESPACIO DE KERNEL                                 |
|  +-----------------------------------------------------------------------------+  |
|  |                 CORE SIMGESRC MICROKERNEL (PREEMPT_RT)                      |  |
|  |                                                                             |  |
|  |   +--------------------+    +--------------------+    +------------------+  |  |
|  |   | CPU Scheduler      |    | MMU Memory Manager |    | Sync Engine      |  |  |
|  |   | (RT / Round Robin) |    | (Paginación 64KB)  |    | (Mutex / Sem)    |  |  |
|  |   +--------------------+    +--------------------+    +------------------+  |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
