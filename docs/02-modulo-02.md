# **MÓDULO 2: GESTIÓN DE PROCESOS Y PLANIFICACIÓN** 

## **2.1. Modelado de Procesos de Misión Crítica (Hospital El Carmen)** 

Para simular el comportamiento del procesador del servidor central bajo la carga transaccional descrita, se definen los 6 procesos base del Hospital Regional Docente Materno Infantil El Carmen de Huancayo. Cada uno cuenta con un identificador de proceso (PID), una prioridad inicial (donde el valor numérico menor denota mayor prioridad estructural), un tiempo estimado de ráfaga de CPU ( _Burst Time_ ), y su clasificación técnica según su comportamiento frente a los recursos del sistema: 

#### **1. P1 - Cesárea de Emergencia / Trauma Shock:** 

- a. _Prioridad Inicial:_ 1 (Máxima) 

- b. _Ráfaga de CPU:_ 4 ms 

- c. _Tipo:_ **CPU-bound** . Requiere procesamiento matemático inmediato y cálculo de algoritmos de soporte de vida con mínima latencia de despacho. 

#### **2. P2 - Telemetría Continua UCIN (Incubadoras):** 

- a. _Prioridad Inicial:_ 2 (Alta) 

- b. _Ráfaga de CPU:_ 3 ms 

- c. _Tipo:_ **I/O-bound** . Depende críticamente de las interrupciones de la tarjeta de red (NIC) para el procesamiento continuo de las tramas de los sensores biométricos. 

#### **3. P3 - Admisión y Registro de Triaje Obstétrico:** 

- a. _Prioridad Inicial:_ 3 (Media-Alta) 

- b. _Ráfaga de CPU:_ 5 ms 

- c. _Tipo:_ **Interactive / I/O-bound** . Bloqueado por la velocidad de entrada por teclado del personal de enfermería; ráfagas de procesamiento cortas tras la captura de datos. 

#### **4. P4 - Consulta Médica Ambulatoria (Citas Ginecología/Pediatría):** 

- a. _Prioridad Inicial:_ 4 (Media) 

- b. _Ráfaga de CPU:_ 6 ms 

- c. _Tipo:_ **Interactive** . Actualizaciones de registros médicos en pantalla, dependiente de consultas intercaladas a bases de datos relacionales locales. 

#### **5. P5 - Despacho Automático de Farmacia (Stock Centralizado):** 

   - a. _Prioridad Inicial:_ 5 (Baja-Media) 

   - b. _Ráfaga de CPU:_ 8 ms 

   - c. _Tipo:_ **I/O-bound** . Realiza múltiples consultas, transacciones de verificación de inventarios y escrituras en el arreglo de discos duros. 

**6. P6 - Consolidado Estadístico Epidemiológico (Reporte MINSA):** 

   - a. _Prioridad Inicial:_ 6 (Mínima) 

   - b. _Ráfaga de CPU:_ 12 ms 

   - c. _Tipo:_ **Batch / CPU-bound puro** . Computación pesada de analítica de datos en segundo plano; no requiere interacción humana ni latencia acotada. 

## **2.2. Definición del Escenario de Carga (10 Procesos con Llegadas Escalonadas)** 

Para validar la solidez matemática de los algoritmos de planificación del kernel, se modela un lote riguroso de **10 procesos** que ingresan a la cola de listos ( _Ready Queue_ ) de forma escalonada en el tiempo (evitando que todos coincidan en el instante $T=0$). Este subconjunto expande los procesos base introduciendo variaciones de carga simulada: 

### **_Tabla 2.1: Métrica General de la Carga de Procesos Simulada_** 

|**PID**|**Nombre de la Subrutina /**<br>**Función Hospitalaria**|**Tiempo de**<br>**Llegada (AT -**<br>**ms)**|**Ráfaga de**<br>**CPU (BT -**<br>**ms)**|**Prioridad**<br>**Numérica**<br>**Inicial**|
|---|---|---|---|---|
|**P1**|Trauma Shock (Cesárea<br>Crítica)|0|4|1|
|**P2**|Telemetría UCIN (Trama<br>Neonatal 1)|1|3|2|
|**P3**|Registro Triaje (Paciente<br>Ingresando)|2|5|3|
|**P4**|Consulta Ambulatoria<br>(Actualización)|3|6|4|
|**P5**|Farmacia (Despacho<br>Analgésicos)|4|8|5|
|**P6**|Reporte MINSA (Ejecución de<br>Fondo)|6|12|6|



|**P7**|Telemetría UCIN (Trama<br>Neonatal 2)|8|3|2|
|---|---|---|---|---|
|**P8**|Trauma Shock (Emergencia<br>Pediátrica)|10|5|1|
|**P9**|Admisión (Validación de<br>Identidad)|12|4|3|
|**P10**|Consulta Médica (Seguimiento<br>Obstétrico)|15|6|4|



## **2.3. Desarrollo Lógico y Matemático de los Algoritmos de Planificación** 

Las métricas fundamentales de rendimiento se calculan utilizando las siguientes ecuaciones estándar de la ingeniería de sistemas operativos: 

$$\text{Turnaround Time (TAT)} = \text{Tiempo de Finalización (CT)} - \text{Tiempo de Llegada (AT)}$$ 

$$\text{Waiting Time (WT)} = \text{Turnaround Time (TAT)} - \text{Ráfaga de CPU 

(BT)}$$ 

$$\text{Response Time (RT)} = \text{Tiempo de Primera Atención (ST)} - \text{Tiempo de Llegada (AT)}$$ 

### **_2.3.1. Algoritmo 1: First-Come, First-Served (FCFS - No Desalojable)_** 

Este algoritmo asigna la CPU al hilo en estricto orden de llegada a la _Ready Queue_ . No evalúa la criticidad médica ni la prioridad del proceso. 

####  **Cronología de Ejecución (Gantt Textual):** 

P1: $[0 - 4]$ ms, P2: $[4 - 7]$ ms, P3: $[7 - 12]$ ms, P4: $[12 - 18]$ ms, P5: $[18 - 26]$ ms, P6: $[26 - 38]$ ms, P7: $[38 - 41]$ ms, P8: $[41 - 46]$ ms, P9: $[46 - 50]$ ms, P10: $[50 - 56]$ ms. 

##### **Tabla de Métricas FCFS:** 

|**PID**|**AT**|**BT**|**CT**|**TAT**|**WT**|**RT**|
|---|---|---|---|---|---|---|
|**P1**|0|4|4|4|0|0|
|**P2**|1|3|7|6|3|3|
|**P3**|2|5|12|10|5|5|



|**P4**|3|6|18|15|9|9|
|---|---|---|---|---|---|---|
|**P5**|4|8|26|22|14|14|
|**P6**|6|12|38|32|20|20|
|**P7**|8|3|41|33|30|30|
|**P8**|10|5|46|36|31|31|
|**P9**|12|4|50|38|34|34|
|**P10**|15|6|56|41|35|35|



- **Tiempo de Espera Promedio ($\overline{WT}$):** $201 / 10 = \mathbf{20.1\text{ ms}}$ 

- **Tiempo de Retorno Promedio ($\overline{TAT}$):** $267 / 10 = \mathbf{26.7\text{ ms}}$ 

- **Análisis Crítico Hospitalario:** FCFS demuestra ser **altamente peligroso** para el hospital. El proceso de telemetría médica P7 (signos vitales UCIN) arriba en el milisegundo 8, pero debido a que el reporte del MINSA (P6) capturó el procesador en el milisegundo 6, P7 se ve obligado a esperar en cola durante 30 ms completos, rompiendo el límite determinista requerido. 

### **_2.3.2. Algoritmo 2: Planificación por Prioridades con Envejecimiento (Aging_** 

### **_- Desalojable)_** 

Para mitigar el problema anterior, este algoritmo evalúa la prioridad asignada. Al ser **desalojable (** **_preemptive_ )** , si un proceso con mayor prioridad estructural llega a la cola, desaloja inmediatamente al proceso en ejecución. 

- **Mecanismo de Envejecimiento (** **_Aging_ ):** Para evitar que los procesos administrativos de baja prioridad sufran de inanición ( _starvation_ ) perpetua, **su prioridad numérica disminuye en 1 unidad por cada 5 ms que permanezcan esperando en la cola de listos** (acercándose al nivel de prioridad de una emergencia). 

##### **Tabla de Métricas Prioridades con Aging:** 

|**PID**|**AT**|**BT**|**CT**|**TAT**|**WT**|**RT**|
|---|---|---|---|---|---|---|
|**P1**|0|4|4|4|0|0|
|**P2**|1|3|7|6|3|3|



|**P3**|2|5|20|18|13|5|
|---|---|---|---|---|---|---|
|**P4**|3|6|30|27|21|20|
|**P5**|4|8|44|40|32|30|
|**P6**|6|12|56|50|38|44|
|**P7**|8|3|11|3|0|0|
|**P8**|10|5|16|6|1|1|
|**P9**|12|4|24|12|8|20|
|**P10**|15|6|36|21|15|30|



- **Tiempo de Espera Promedio ($\overline{WT}$):** $151 / 10 = \mathbf{15.1\text{ ms}}$ 

- **Tiempo de Retorno Promedio ($\overline{TAT}$):** $227 / 10 = \mathbf{22.7\text{ ms}}$ 

- **Análisis Crítico Hospitalario:** Este esquema optimiza la respuesta para los hilos biométricos y de soporte vital. P7 y P8 entran casi instantáneamente limpiando la latencia de despacho para las emergencias médicas. 

### **_2.3.3. Algoritmo 3: Round Robin con Quantum Variable (RR - Desalojable por Tiempo)_** 

Este algoritmo aplica un enfoque equitativo basado en el tiempo compartido. Se define un **Quantum ($Q$) fijo de 4 ms** para este experimento. 

##### **Tabla de Métricas Round Robin ($Q = 4\text{ ms}$):** 

|**PID**|**AT**|**BT**|**CT**|**TAT**|**WT**|**RT**|
|---|---|---|---|---|---|---|
|**P1**|0|4|4|4|0|0|
|**P2**|1|3|7|6|3|3|
|**P3**|2|5|31|29|24|5|
|**P4**|3|6|37|34|28|8|
|**P5**|4|8|49|45|37|11|
|**P6**|6|12|56|50|38|16|



|**P7**|8|3|22|14|11|11|
|---|---|---|---|---|---|---|
|**P8**|10|5|42|32|27|16|
|**P9**|12|4|35|23|19|23|
|**P1**<br>**0**|15|6|53|38|32|30|



- **Tiempo de Espera Promedio ($\overline{WT}$):** $219 / 10 = \mathbf{21.9\text{ ms}}$ 

- **Tiempo de Retorno Promedio ($\overline{TAT}$):** $305 / 10 = \mathbf{30.5\text{ ms}}$ 

- **Análisis Crítico Hospitalario:** Round Robin ofrece el **mejor tiempo de respuesta inicial (** **_Response Time_ ) para interfaces de usuario concurrentes** (admisión, farmacia), pero penaliza drásticamente el rendimiento global de los hilos de emergencias médicas al tratarlos con la misma importancia que un proceso ordinario. 

## **2.4. Comparación y Selección de la Arquitectura de Planificación** 

### **_Tabla 2.2: Matriz Comparativa Descriptiva de Rendimiento_** 

|**Algoritmo**<br>**Evaluado**|**WT**<br>**Global**|**TAT**<br>**Global**|**Máximo Jitter en**<br>**Telemetría**|**Resiliencia ante**<br>**Sobrecarga**|
|---|---|---|---|---|
|**FCFS**|20.1 ms|26.7<br>ms|Crítico ($><br>30\text{ ms}$)|Baja (Efecto Convoy severo).|
|**Prioridades +**<br>**Aging**|**15.1 ms**|**22.7**<br>**ms**|**Óptimo ($<**<br>**1\text{ ms}$)**|Alta (Aislamiento de la<br>UCIN).|
|**Round Robin**<br>**($Q=4$)**|21.9 ms|30.5<br>ms|Moderado ($\sim<br>11\text{ ms}$)|Regular (Sobrecarga por<br>Context Switch).|



### **_Decisión de Ingeniería de Software (Para el Módulo 5):_** 

El subsistema de planificación centralizado de **SIMGESRC** utilizará un **esquema híbrido basado en colas multinivel con retroalimentación (MLFQ)** donde la cola de máxima prioridad está gobernada por el algoritmo de **Prioridades Estrictas con Desalojo** (dedicada exclusivamente a P1 Trauma Shock y P2/P7 Telemetría UCIN). Las colas secundarias de nivel inferior gestionarán los procesos 

interactivos y administrativos del hospital utilizando **Round Robin con envejecimiento activo** . 
