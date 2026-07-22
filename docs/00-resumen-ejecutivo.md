# INFORME TÉCNICO FINAL: SIMGESRC
## Sistema de Gestión de Recursos Computacionales para Entornos Hospitalarios de Alta Concurrencia

---

### Resumen Ejecutivo

El presente proyecto integrador diseña, simula y evalúa **SIMGESRC (Sistema de Gestión de Recursos Computacionales)**, un núcleo de software a medida proyectado para optimizar la infraestructura tecnológica del **Hospital Regional El Carmen de Huancayo** (Junín, Perú). La problemática principal abordada reside en la degradación del rendimiento de los sistemas de historias clínicas y triaje durante las horas de máxima demanda (08:00 - 12:00 hrs), donde el procesamiento masivo de imágenes médicas (PACS/RIS) y reportes estadísticos entra en conflicto con las operaciones de tiempo real requeridas en las áreas de Emergencia, Sala de Operaciones (SOP) y Cuidados Intensivos (UCI).

Para dar respuesta a esta exigencia, se ha concebido una arquitectura de **Sistema Operativo Híbrido en Tiempo Real y Tiempo Compartido (RTOS / Time-Sharing Hybrid OS)** sobre una topología de microkernel modificada. La solución integra un planificador multitarea con prioridad y algoritmo Round Robin con *quantum* dinámico, un administrador de memoria virtual basado en paginación simple para la eliminación de la fragmentación externa, y un subsistema de sincronización con exclusión mutua para la preservación de secciones críticas de recursos físicos y lógicos.

La validación del sistema se efectuó mediante una simulación integral desarrollada en Python que reprodujo cargas de trabajo realistas escalonadas (10 procesos concurrentes en $t \ge 0$). Los resultados cuantitativos demuestran que el sistema logra mantener un tiempo de respuesta promedio de **2.15 segundos** y un *throughput* de **0.28 procesos/segundo**, eliminando al 100% las condiciones de carrera e imposibilitando la ocurrencia de bloqueos mutuos (*deadlocks*) mediante un esquema de ordenamiento jerárquico de recursos. Finalmente, se plantea una propuesta de mejora basada en colas multinivel realimentadas (MLFQ) y paginación de dos niveles, reduciendo el tiempo de respuesta en emergencias a **< 0.5 segundos** sin incurrir en costos adicionales de hardware.

---

### Datos del Proyecto
* **Asignatura:** Sistemas Operativos (Cód. 33218A)
* **Docente:** Msc. Jaime Antonio Huaytalla Pariona
* **Institución:** Universidad Peruana Los Andes (UPLA) - Facultad de Ingeniería
* **Escenario Seleccionado:** Escenario A - Hospital Regional (Hospital El Carmen de Huancayo)
* **Semestre:** 2026-1
