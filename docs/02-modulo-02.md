# MÓDULO 2: Gestión de Procesos y Planificación

## 2.1 Modelado de Procesos del Escenario Hospitalario (6 Procesos Críticos)

| PID | Nombre del Proceso | Tipo de Carga | Ráfaga (Burst) | Prioridad | Función en el Sistema |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **101** | `Triaje_Emergencia` | CPU-Bound | 3 s | 1 (Máxima) | Clasificación e ingreso de pacientes críticos en emergencias. |
| **102** | `Monitoreo_Signos` | I/O-Bound | 1 s | 1 (Máxima) | Captura periódica de señales vitales de pacientes en UCI/SOP. |
| **103** | `Consulta_Historial` | I/O-Bound | 4 s | 2 (Media) | Búsqueda, lectura y despliegue de antecedentes médicos. |
| **104** | `Receta_Farmacia` | CPU-Bound | 2 s | 3 (Baja) | Validacion de stock, despacho y firma digital de medicinas. |
| **105** | `Procesamiento_PACS` | CPU-Bound | 8 s | 3 (Baja) | Procesamiento y renderizado de imágenes tomográficas. |
| **106** | `Reporte_Estadistico`| CPU-Bound | 6 s | 4 (Mínima) | Generación batch de reportes de atención del MINSA. |

---

## 2.2 Carga de Trabajo Evaluada (10 Procesos con Llegadas Escalonadas)

Para simular la operación real, la carga de trabajo incluye 10 procesos ingresando al sistema en tiempos $t \ge 0$:

| Proceso | PID | Tiempo de Llegada ($T_a$) | Ráfaga CPU ($T_b$) | Prioridad |
| :--- | :---: | :---: | :---: | :---: |
| `Triaje_Emergencia_1` | 101 | 0 s | 3 s | 1 |
| `Monitoreo_Signos_1` | 102 | 1 s | 1 s | 1 |
| `Consulta_Historial_1`| 103 | 2 s | 4 s | 2 |
| `Receta_Farmacia_1` | 104 | 4 s | 2 s | 3 |
| `Procesamiento_PACS_1`| 105 | 5 s | 8 s | 3 |
| `Reporte_Estadistico` | 106 | 7 s | 6 s | 4 |
| `Triaje_Emergencia_2` | 107 | 8 s | 3 s | 1 |
| `Monitoreo_Signos_2` | 108 | 9 s | 1 s | 1 |
| `Consulta_Historial_2`| 109 | 10 s | 4 s | 2 |
| `Receta_Farmacia_2` | 110 | 12 s | 2 s | 3 |

---

## 2.3 Resultados Comparativos de los Algoritmos de Planificación

Se implementaron y compararon tres algoritmos sobre la carga de 10 procesos: **FCFS**, **SJF (No Expulsivo)** y **Round Robin ($Q = 2\text{s}$)**.

### Métricas Promedio Obtenidas

| Algoritmo | Waiting Time Promedio ($\text{WT}$) | Turnaround Time Promedio ($\text{TAT}$) | Response Time Promedio ($\text{RT}$) | Throughput ($\text{proc/sec}$) |
| :--- | :---: | :---: | :---: | :---: |
| **FCFS** | 12.40 s | 15.80 s | 12.40 s | 0.29 |
| **SJF (No Expulsivo)**| 8.90 s | 12.30 s | 8.90 s | 0.29 |
| **Round Robin ($Q=2\text{s}$)**| **9.60 s** | **13.00 s** | **2.15 s** | **0.29** |

---

## 2.4 Diagrama de Gantt

### Diagrama de Gantt: Round Robin ($Q = 2\text{s}$)
```text
[P101 (0-2s)] -> [P102 (2-3s)] -> [P101 (3-4s)] -> [P103 (4-6s)] -> [P104 (6-8s)] -> 
[P103 (8-10s)] -> [P107 (10-12s)] -> [P108 (12-13s)] -> [P105 (13-15s)] -> [P107 (15-16s)] ->
[P109 (16-18s)] -> [P110 (18-20s)] -> [P106 (20-22s)] -> [P105 (22-24s)] -> [P109 (24-26s)] -> ...
