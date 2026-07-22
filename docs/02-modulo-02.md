# MÓDULO 2: Gestión de Procesos y Planificación

## 2.1 Modelado de Procesos de Misión Crítica

| PID | Nombre del Proceso | Prioridad Inicial | Ráfaga CPU ($BT$) | Tipo de Carga | Descripción |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **P1** | `Cesárea_Emergency` | 1 (Máxima) | 4 ms | CPU-bound | Trauma Shock y soporte de vida[cite: 11]. |
| **P2** | `Telemetria_UCIN` | 2 (Alta) | 3 ms | I/O-bound | Sensores biométricos de incubadoras[cite: 11]. |
| **P3** | `Triaje_Obstetrico` | 3 (Media-Alta)| 5 ms | Interactive / I/O | Registro manual de datos de ingreso[cite: 11]. |
| **P4** | `Consulta_Ambulatoria`| 4 (Media) | 6 ms | Interactive | Citas de ginecología y pediatría[cite: 11]. |
| **P5** | `Despacho_Farmacia` | 5 (Baja-Media)| 8 ms | I/O-bound | Verificación e inventario de stock[cite: 11]. |
| **P6** | `Reporte_MINSA` | 6 (Mínima) | 12 ms | Batch / CPU-bound | Consolidado estadístico en segundo plano[cite: 11]. |

---

## 2.2 Escenario de Carga de Trabajo (10 Procesos Escalonados)

| PID | Subrutina / Función Hospitalaria | Tiempo Llegada ($AT$) | Ráfaga CPU ($BT$) | Prioridad Inicial |
| :---: | :--- | :---: | :---: | :---: |
| **P1** | Trauma Shock (Cesárea Crítica) | 0 ms | 4 ms | 1[cite: 11] |
| **P2** | Telemetría UCIN (Trama Neonatal 1) | 1 ms | 3 ms | 2[cite: 11] |
| **P3** | Registro Triaje (Paciente Ingresando)| 2 ms | 5 ms | 3[cite: 11] |
| **P4** | Consulta Ambulatoria (Actualización) | 3 ms | 6 ms | 4[cite: 11] |
| **P5** | Farmacia (Despacho Analgésicos) | 4 ms | 8 ms | 5[cite: 11] |
| **P6** | Reporte MINSA (Ejecución de Fondo) | 6 ms | 12 ms | 6[cite: 11] |
| **P7** | Telemetría UCIN (Trama Neonatal 2) | 8 ms | 3 ms | 2[cite: 11] |
| **P8** | Trauma Shock (Emergencia Pediátrica)| 10 ms | 5 ms | 1[cite: 11] |
| **P9** | Admisión (Validación de Identidad) | 12 ms | 4 ms | 3[cite: 11] |
| **P10**| Consulta Médica (Seguimiento) | 15 ms | 6 ms | 4[cite: 11] |

---

## 2.3 Métricas Obtenidas por Algoritmo de Planificación

### 1. FCFS (No Desalojable)
* **Gantt:** P1 [0-4] -> P2 [4-7] -> P3 [7-12] -> P4 [12-18] -> P5 [18-26] -> P6 [26-38] -> P7 [38-41] -> P8 [41-46] -> P9 [46-50] -> P10 [50-56][cite: 11].
* **Métricas:** $\overline{WT} = \mathbf{20.1\text{ ms}}$, $\overline{TAT} = \mathbf{26.7\text{ ms}}$[cite: 11].
* **Análisis Crítico:** P7 (UCIN) llega a los 8 ms pero debe esperar 30 ms atrapado detrás de P6 (Reporte MINSA)[cite: 11].

### 2. Prioridades con Aging (Desalojable)
* **Mecanismo:** Incrementa prioridad en 1 unidad por cada 5 ms de espera en cola[cite: 11].
* **Métricas:** $\overline{WT} = \mathbf{15.1\text{ ms}}$, $\overline{TAT} = \mathbf{22.7\text{ ms}}$[cite: 11].
* **Análisis Crítico:** Los hilos P7 y P8 ingresan de inmediato eliminando la latencia en urgencias[cite: 11].

### 3. Round Robin ($Q = 4\text{ ms}$)
* **Métricas:** $\overline{WT} = \mathbf{21.9\text{ ms}}$, $\overline{TAT} = \mathbf{30.5\text{ ms}}$[cite: 11].
* **Análisis Crítico:** Ofrece buena respuesta interactiva pero penaliza los hilos de emergencias al darles el mismo trato que a tareas secundarias[cite: 11].

---

## 2.4 Matriz Comparativa

| Algoritmo | WT Global | TAT Global | Máximo Jitter Telemetría | Resiliencia ante Sobrecarga |
| :--- | :---: | :---: | :---: | :--- |
| **FCFS** | 20.1 ms | 26.7 ms | Crítico ($> 30\text{ ms}$) | Baja (Efecto Convoy)[cite: 11]. |
| **Prioridades + Aging** | **15.1 ms** | **22.7 ms** | **Óptimo ($< 1\text{ ms}$)** | **Alta (Aislamiento de la UCIN)**[cite: 11]. |
| **Round Robin ($Q=4$)** | 21.9 ms | 30.5 ms | Moderado ($\sim 11\text{ ms}$) | Regular (Sobrecarga Context Switch)[cite: 11]. |
