# MÓDULO 2: GESTIÓN DE PROCESOS Y PLANIFICACIÓN

### 2.1. Modelado de Procesos de Misión Crítica (Hospital El Carmen)
Se definen los 6 procesos base del Hospital Regional Docente Materno Infantil El Carmen de Huancayo:

1. **P1 - Cesárea de Emergencia / Trauma Shock:**
   - **Prioridad Inicial:** 1 (Máxima)
   - **Ráfaga de CPU (Burst Time):** 4 ms
   - **Tipo:** CPU-bound. Procesamiento matemático inmediato y algoritmos de soporte de vida.
2. **P2 - Telemetría Continua UCIN (Incubadoras):**
   - **Prioridad Inicial:** 2 (Alta)
   - **Ráfaga de CPU (Burst Time):** 3 ms
   - **Tipo:** I/O-bound. Depende de interrupciones de la NIC para tramas de sensores biométricos.
3. **P3 - Admisión y Registro de Triaje Obstétrico:**
   - **Prioridad Inicial:** 3 (Media-Alta)
   - **Ráfaga de CPU (Burst Time):** 5 ms
   - **Tipo:** Interactive / I/O-bound. Dependiente de entrada por teclado.
4. **P4 - Consulta Médica Ambulatoria (Citas Ginecología/Pediatría):**
   - **Prioridad Inicial:** 4 (Media)
   - **Ráfaga de CPU (Burst Time):** 6 ms
   - **Tipo:** Interactive. Actualizaciones de registros médicos e historias clínicas.
5. **P5 - Despacho Automático de Farmacia (Stock Centralizado):**
   - **Prioridad Inicial:** 5 (Baja-Media)
   - **Ráfaga de CPU (Burst Time):** 8 ms
   - **Tipo:** I/O-bound. Consultas, verificación de inventario y escrituras en disco.
6. **P6 - Consolidado Estadístico Epidemiológico (Reporte MINSA):**
   - **Prioridad Inicial:** 6 (Mínima)
   - **Ráfaga de CPU (Burst Time):** 12 ms
   - **Tipo:** Batch / CPU-bound puro. Analítica de datos pesada en segundo plano.

---

### 2.2. Definición del Escenario de Carga (10 Procesos con Llegadas Escalonadas)

#### Tabla 2.1: Métrica General de la Carga de Procesos Simulada

| PID | Nombre de la Subrutina / Función Hospitalaria | Tiempo de Llegada (AT - ms) | Ráfaga de CPU (BT - ms) | Prioridad Numérica Inicial |
| :---: | :--- | :---: | :---: | :---: |
| **P1** | Trauma Shock (Cesárea Crítica) | 0 | 4 | 1 |
| **P2** | Telemetría UCIN (Trama Neonatal 1) | 1 | 3 | 2 |
| **P3** | Registro Triaje (Paciente Ingresando) | 2 | 5 | 3 |
| **P4** | Consulta Ambulatoria (Actualización) | 3 | 6 | 4 |
| **P5** | Farmacia (Despacho Analgésicos) | 4 | 8 | 5 |
| **P6** | Reporte MINSA (Ejecución de Fondo) | 6 | 12 | 6 |
| **P7** | Telemetría UCIN (Trama Neonatal 2) | 8 | 3 | 2 |
| **P8** | Trauma Shock (Emergencia Pediátrica) | 10 | 5 | 1 |
| **P9** | Admisión (Validación de Identidad) | 12 | 4 | 3 |
| **P10** | Consulta Médica (Seguimiento Obstétrico) | 15 | 6 | 4 |
