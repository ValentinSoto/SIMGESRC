# MÓDULO 2: GESTIÓN DE PROCESOS Y PLANIFICACIÓN (Continuación)

### 2.3. Desarrollo Lógico y Matemático de los Algoritmos de Planificación

Fórmulas estándar empleadas:
$$\text{Turnaround Time (TAT)} = \text{Tiempo de Finalización (CT)} - \text{Tiempo de Llegada (AT)}$$
$$\text{Waiting Time (WT)} = \text{Turnaround Time (TAT)} - \text{Ráfaga de CPU (BT)}$$
$$\text{Response Time (RT)} = \text{Tiempo de Primera Atención (ST)} - \text{Tiempo de Llegada (AT)}$$

---

#### 2.3.1. Algoritmo 1: First-Come, First-Served (FCFS - No Desalojable)
- **Gantt Textual:** P1: $[0-4]$, P2: $[4-7]$, P3: $[7-12]$, P4: $[12-18]$, P5: $[18-26]$, P6: $[26-38]$, P7: $[38-41]$, P8: $[41-46]$, P9: $[46-50]$, P10: $[50-56]$ ms.

| PID | AT | BT | CT | TAT | WT | RT |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| P1 | 0 | 4 | 4 | 4 | 0 | 0 |
| P2 | 1 | 3 | 7 | 6 | 3 | 3 |
| P3 | 2 | 5 | 12 | 10 | 5 | 5 |
| P4 | 3 | 6 | 18 | 15 | 9 | 9 |
| P5 | 4 | 8 | 26 | 22 | 14 | 14 |
| P6 | 6 | 12 | 38 | 32 | 20 | 20 |
| P7 | 8 | 3 | 41 | 33 | 30 | 30 |
| P8 | 10 | 5 | 46 | 36 | 31 | 31 |
| P9 | 12 | 4 | 50 | 38 | 34 | 34 |
| P10 | 15 | 6 | 56 | 41 | 35 | 35 |

- **$\\overline{WT}$:** $201 / 10 = \mathbf{20.1\text{ ms}}$ | **$\\overline{TAT}$:** $267 / 10 = \mathbf{26.7\text{ ms}}$
- **Análisis Crítico:** P7 (telemetría UCIN) espera 30 ms por culpa de P6 (reporte MINSA), violando el determinismo requerido.

---

#### 2.3.2. Algoritmo 2: Planificación por Prioridades con Envejecimiento (Aging - Desalojable)
Mecanismo de Aging: Disminuye la prioridad en 1 por cada 5 ms de espera.

| PID | AT | BT | CT | TAT | WT | RT |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| P1 | 0 | 4 | 4 | 4 | 0 | 0 |
| P2 | 1 | 3 | 7 | 6 | 3 | 3 |
| P3 | 2 | 5 | 20 | 18 | 13 | 5 |
| P4 | 3 | 6 | 30 | 27 | 21 | 20 |
| P5 | 4 | 8 | 44 | 40 | 32 | 30 |
| P6 | 6 | 12 | 56 | 50 | 38 | 44 |
| P7 | 8 | 3 | 11 | 3 | 0 | 0 |
| P8 | 10 | 5 | 16 | 6 | 1 | 1 |
| P9 | 12 | 4 | 24 | 12 | 8 | 20 |
| P10 | 15 | 6 | 36 | 21 | 15 | 30 |

- **$\\overline{WT}$:** $151 / 10 = \mathbf{15.1\text{ ms}}$ | **$\\overline{TAT}$:** $227 / 10 = \mathbf{22.7\text{ ms}}$
- **Análisis Crítico:** P7 y P8 ingresan casi inmediatamente, garantizando baja latencia.

---

#### 2.3.3. Algoritmo 3: Round Robin con Quantum Variable (RR - Desalojable por Tiempo, $Q = 4\text{ ms}$)

| PID | AT | BT | CT | TAT | WT | RT |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| P1 | 0 | 4 | 4 | 4 | 0 | 0 |
| P2 | 1 | 3 | 7 | 6 | 3 | 3 |
| P3 | 2 | 5 | 31 | 29 | 24 | 5 |
| P4 | 3 | 6 | 37 | 34 | 28 | 8 |
| P5 | 4 | 8 | 49 | 45 | 37 | 11 |
| P6 | 6 | 12 | 56 | 50 | 38 | 16 |
| P7 | 8 | 3 | 22 | 14 | 11 | 11 |
| P8 | 10 | 5 | 42 | 32 | 27 | 16 |
| P9 | 12 | 4 | 35 | 23 | 19 | 23 |
| P10 | 15 | 6 | 53 | 38 | 32 | 30 |

- **$\\overline{WT}$:** $219 / 10 = \mathbf{21.9\text{ ms}}$ | **$\\overline{TAT}$:** $305 / 10 = \mathbf{30.5\text{ ms}}$

---

### 2.4. Comparación y Selección de la Arquitectura de Planificación

#### Tabla 2.2: Matriz Comparativa Descriptiva de Rendimiento

| Algoritmo Evaluado | WT Global | TAT Global | Máximo Jitter en Telemetría | Resiliencia ante Sobrecarga |
| :--- | :---: | :---: | :---: | :--- |
| **FCFS** | 20.1 ms | 26.7 ms | Crítico ($> 30\text{ ms}$) | Baja (Efecto Convoy severo). |
| **Prioridades + Aging** | **15.1 ms** | **22.7 ms** | **Óptimo ($< 1\text{ ms}$)** | **Alta (Aislamiento de la UCIN).** |
| **Round Robin ($Q=4$)** | 21.9 ms | 30.5 ms | Moderado ($\\sim 11\text{ ms}$) | Regular (Sobrecarga por Context Switch). |

**Decisión de Ingeniería:** Esquema híbrido basado en **Colas Multinivel con Retroalimentación (MLFQ)**.
