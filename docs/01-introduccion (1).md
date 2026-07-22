# UNIVERSIDAD PERUANA LOS ANDES
## Facultad de Ingeniería – Ingeniería de Sistemas y Computación
**Sistemas Operativos – Cód. 33218A | VII Ciclo | UPLA 2026-I**  
**PLAN DE TRABAJO – ENTREGABLE E1**  
*«SIMGESRC: Sistema de Gestión de Recursos Computacionales»*

---

### Datos Generales
- **Escenario elegido:** Escenario A – Hospital Regional
- **Organización de referencia:** Docente Materno Infantil El Carmen
- **Docente:** Msc. Jaime Antonio Huaytalla Pariona
- **Fecha de entrega:** Semana 13 – Sesión 2

---

### 1. Integrantes y distribución de módulos

| Integrante | Módulo asignado |
| :--- | :--- |
| Soto Barriento Valentin B | Módulo 1 – Arquitectura y Tipo de SO |
| Soto Barriento Valentin B | Módulo 2 – Gestión de Procesos y Planificación |
| Soto Barriento Valentin B | Módulo 3 – Sincronización y Concurrencia |
| Soto Barriento Valentin B | Módulo 4 – Gestión de Memoria |
| Soto Barriento Valentin B | Módulo 5 – Integración, Análisis y Propuesta de Mejora (trabajo conjunto) |

---

### 2. Cronograma de trabajo (Semanas 13-16)

| Semana | Sesión | Actividades |
| :---: | :---: | :--- |
| 13 | Sesión 1 | Conformación del grupo, elección del escenario (Hospital Regional) y levantamiento inicial de información del proceso de atención hospitalaria. |
| 13 | Sesión 2 | Entrega de E1 (Plan de trabajo). Inicio del Módulo 1: justificación del tipo de SO y arquitectura hardware propuesta. |
| 14 | Sesión 1 | Finalización del Módulo 1 (diagrama de arquitectura). Inicio del Módulo 2: modelado de procesos del sistema hospitalario y carga de trabajo. |
| 14 | Sesión 2 | Implementación del simulador de scheduling (FCFS, SJF, Prioridades). Entrega de E2 (Avance parcial: Módulos 1 y 2). |
| 15 | Sesión 1 | Módulo 3: identificación de secciones críticas y desarrollo de sincronización con mutex/semáforos (asignación de salas y equipos). |
| 15 | Sesión 2 | Módulo 4: simulador de asignación de memoria y cálculo de fragmentación. Tutoría virtual de 30 min con el docente. |
| 16 | Sesión 1 | Módulo 5: integración del sistema, análisis de bottlenecks y propuesta de mejora. Entrega de E3 (Informe técnico final) y E4 (Repositorio GitHub). |
| 16 | Sesión 2 | Entrega de E5: exposición (15 min) + preguntas (5 min) y demo en vivo del sistema integrado. |

---

### 1.1. Descripción del Escenario y Justificación del Tipo de Sistema Operativo

#### 1.1.1. Descripción del Contexto Organizacional y Problemática Operativa
El Hospital Regional Docente Materno Infantil El Carmen de Huancayo es una institución de salud de alta especialización encargada de la atención gineco-obstétrica y pediátrica en la región Junín. La naturaleza crítica de este nosocomio implica que la gestión de colas y la asignación de recursos computacionales impacten directamente en la supervivencia de los pacientes (neonatos en estado crítico y madres gestantes con embarazos de alto riesgo).

Actualmente, las interfaces de admisión, triaje y emergencias experimentan colapsos sistemáticos durante las horas pico (08:00 a.m. a 12:00 p.m.). La concurrencia de aproximadamente 150 usuarios simultáneos (personal médico, enfermeros, farmacéuticos y administrativos) genera una carga de trabajo de entre 40 y 50 solicitudes de procesos por minuto. A esta carga transaccional se añade el flujo ininterrumpido de telemetría médica proveniente de la Unidad de Cuidados Intensivos Neonatales (UCIN), donde decenas de incubadoras transmiten señales biométricas de signos vitales cada 1,000 ms.

La falta de un subsistema de planificación con latencia determinista provoca que las solicitudes críticas de Trauma Shock o las alertas de paros cardiorrespiratorios neonatales compitan en igualdad de condiciones de CPU con tareas administrativas secundarias. Esto genera bloqueos indeterminados en el hilo de ejecución, retrasos en la actualización de historias clínicas y el riesgo inaceptable de que una alerta de telemetría médica se descarte o procese tarde debido a la inanición de hilos computacionales.
