# **MÓDULO 1: ARQUITECTURA Y TIPO DE SISTEMA OPERATIVO** 

## **1.1. Descripción del Escenario y Justificación del Tipo de Sistema Operativo** 

### **_1.1.1. Descripción del Contexto Organizacional y Problemática Operativa_** 

El Hospital Regional Docente Materno Infantil El Carmen de Huancayo es una institución de salud de alta especialización encargada de la atención ginecoobstétrica y pediátrica en la región Junín. La naturaleza crítica de este nosocomio implica que la gestión de colas y la asignación de recursos computacionales impacten directamente en la supervivencia de los pacientes (neonatos en estado crítico y madres gestantes con embarazos de alto riesgo). 

Actualmente, las interfaces de admisión, triaje y emergencias experimentan colapsos sistemáticos durante las horas pico (08:00 a.m. a 12:00 p.m.). La concurrencia de aproximadamente 150 usuarios simultáneos (personal médico, enfermeros, farmacéuticos y administrativos) genera una carga de trabajo de entre 40 y 50 solicitudes de procesos por minuto. A esta carga transaccional se añade el flujo ininterrumpido de telemetría médica proveniente de la Unidad de Cuidados Intensivos Neonatales (UCIN), donde decenas de incubadoras transmiten señales biométricas de signos vitales cada 1,000 ms. 

La falta de un subsistema de planificación con latencia determinista provoca que las solicitudes críticas de Trauma Shock o las alertas de paros cardiorrespiratorios neonatales compitan en igualdad de condiciones de CPU con tareas administrativas secundarias. Esto genera bloqueos indeterminados en el hilo de ejecución, retrasos en la actualización de historias clínicas y el riesgo inaceptable de que una alerta de telemetría médica se descarte o procese tarde debido a la inanición de hilos computacionales. 

### **_1.1.2. Justificación Técnica de la Elección de un Sistema Operativo Híbrido / Tiempo Real (RTOS)_** 

Para mitigar los riesgos de impredecibilidad temporal, el diseño del sistema **SIMGESRC** se fundamenta sobre un Sistema Operativo Híbrido con capacidades de Tiempo Real (RTOS). Esta decisión se justifica mediante tres criterios de ingeniería de sistemas de misión crítica: 

1. **Latencia Determinista (Bounded Latency):** A diferencia de los sistemas operativos comerciales orientados al rendimiento promedio ( _throughput_ ), un RTOS garantiza que el tiempo máximo de respuesta ( _worst-case execution time_ - WCET) ante una interrupción de hardware o software esté rígidamente acotado. En el contexto de la UCIN, la recepción de una ráfaga de signos vitales anómalos debe activar un cambio de contexto en el procesador en un intervalo de microsegundos ($\mu s$), asegurando que la notificación visual y auditiva en la central de monitoreo ocurra de manera inmediata e invariable. 

2. **Manejo Estricto de Prioridades y Desalojo (** **_Preemption_ ):** El kernel elegido soporta planificación por prioridades con desalojo completo ( _fully preemptible kernel_ ). Si la CPU se encuentra ejecutando un proceso de baja prioridad, como la generación de un reporte epidemiológico del MINSA, y se recibe una interrupción de Trauma Shock, el planificador ( _scheduler_ ) suspende inmediatamente el proceso administrativo, guarda su bloque de control de proceso (PCB) y transfiere los ciclos de ejecución al proceso de emergencia. Esto elimina la latencia de despacho aleatoria. 

3. **Soporte Masivo para Concurrencia Híbrida:** El sistema operativo debe _I/O-bound_ interactivos 

coexistir con flujos de trabajo dispares: procesos (ingreso manual en el triaje) y procesos de flujo continuo de datos de sensores de red. La arquitectura híbrida combina un programador de tiempo compartido para el módulo administrativo con un despachador de tiempo real de alta prioridad para la telemetría, aislando ambos entornos de ejecución para evitar que la sobrecarga transaccional de la consulta externa degrade el rendimiento de los módulos críticos de monitoreo vital. 

### **_1.1.3. Tabla Comparativa de Esquemas de Sistemas Operativos Descartados_** 

A continuación, se analizan y descartan formalmente dos alternativas arquitectónicas evaluadas para la implementación de SIMGESRC: 

||**Alternativa 1:**|**Alternativa 2: SO de**|**Solución**|
|---|---|---|---|
|**Criterio Técnico**|**SO por Lotes**<br>**Puro (Batch**<br>**Processing)**|**Tiempo Compartido**<br>**Estándar (Escritorio /**<br>**Servidor Convencional)**|**Propuesta: SO**<br>**Híbrido / Tiempo**<br>**Real (RTOS)**|
|**Mecanismo de**<br>**Planifcación**|Secuencial sin<br>desalojo (FIFO<br>masivo).|Planifcadores basados en<br>justicia de tiempo<br>(_Completely Fair_<br>_Scheduler_- CFS).|Planifcación por<br>Prioridades<br>Estrictas con<br>Desalojo<br>Completo e<br>Interrupciones<br>Indexadas.|
|**Comportamiento**<br>**ante**<br>**Emergencias**|Inviable. La<br>emergencia<br>espera a que<br>terminen los<br>lotes previos en<br>ejecución.|Impredecible. El proceso<br>de emergencia puede ser<br>postergado por algoritmos<br>que priorizan la equidad de<br>la CPU.|Inmediato. El<br>kernel detiene<br>cualquier proceso<br>activo de menor<br>jerarquía para<br>despachar la<br>alerta.|
|**Procesamiento**<br>**de Telemetría**<br>**(UCIN)**|Nulo. No maneja<br>fujos<br>interactivos<br>continuos ni<br>señales por<br>segundo.|Degradación del<br>rendimiento. Alto overhead<br>por cambios de contexto<br>masivos y fuctuaciones en<br>la latencia (_jitter_).|Determinista.<br>Asignación<br>periódica fja<br>garantizada cada<br>1,000 ms sin<br>pérdida de<br>paquetes.|
|**Justifcación del**<br>**Descarte**<br>**Técnico**|**RECHAZADO:**<br>Diseñado para<br>alta efciencia en<br>tareas<br>repetitivas de<br>fondo (nóminas,<br>backups). Su<br>latencia infnita<br>causaría el<br>fallecimiento de<br>pacientes<br>críticos al no<br>responder a<br>interrupciones<br>en tiempo real.|**RECHAZADO:**Aunque<br>tolera 150 usuarios,<br>prioriza la experiencia del<br>usuario de escritorio. El<br>algoritmo busca que todos<br>los hilos avancen<br>equitativamente, lo que<br>introduce retrasos<br>probabilísticos<br>inaceptables en alertas<br>médicas.|**ACEPTADO:**El<br>aislamiento de<br>entornos asegura<br>la<br>transaccionalidad<br>de los 150<br>usuarios y blinda<br>el determinismo<br>de la telemetría<br>neonatológica.|



## **1.2. Arquitectura Hardware Propuesta** 

### **_1.2.1. Dimensionamiento Cuantitativo e Infraestructura del Servidor Central_** 

El servidor central del sistema **SIMGESRC** debe ser configurado para soportar los picos transaccionales y el flujo constante de telemetría sin riesgo de saturación. La propuesta de hardware se detalla de la siguiente manera: 

- **Procesador (CPU):** Se requiere una arquitectura multiprocesador simétrica (SMP) con un procesador de **16 núcleos físicos (32 hilos lógicos)** con una frecuencia base de 3.0 GHz. 

   - _Justificación Cuantitativa:_ El cálculo del paralelismo se realiza dividiendo los hilos en dominios de ejecución: 4 núcleos físicos se dedican exclusivamente a través de afinidad de CPU ( _CPU affinity_ ) al procesamiento y despaquetizado de las tramas UDP/IP de la telemetría de la UCIN (procesando las ráfagas por segundo de los monitores biométricos); 8 núcleos físicos gestionan la lógica transaccional de los 150 usuarios concurrentes en horas pico (estimando que las 50 solicitudes por minuto requieren procesamiento paralelo inmediato); 4 núcleos físicos se reservan para el sistema de base de datos distribuidos e interfaces con el MINSA. 

- **Memoria RAM: 128 GB DDR5 ECC (Error Correcting Code)** a 4800 MHz. 

   - _Justificación Cuantitativa:_ Las tramas de telemetría ocupan poca memoria en búfer, pero las imágenes médicas (ecografías de alta resolución, tomografías pediátricas y radiografías obstétricas) cargadas por los médicos concurrentes requieren un promedio de 250 MB por paciente en memoria activa. Sosteniendo 50 consultas activas con acceso simultáneo a imágenes, se consumen $50 \times 250 \text{ MB} = 12.5 \text{ GB}$. La base de datos relacional indexada en memoria para respuestas de historias clínicas en menos de 100 ms requiere un _pool_ de 64 GB. El espacio restante (51.5 GB) se asigna para los búferes de intercambio de red, el espacio del sistema operativo y la prevención de fallos por falta de memoria ( _Out-Of-Memory_ - OOM). El uso de tecnología ECC es innegociable para corregir la corrupción de bits en la RAM inducida por interferencias electromagnéticas de los equipos médicos. 

- **Subsistema de Almacenamiento:** Arreglo **RAID 10 compuesto por 4 unidades SSD NVMe PCIe 4.0 de 2 TB cada una** . 

   - _Justificación Cuantitativa:_ El almacenamiento requiere una alta tolerancia a fallos combinada con baja latencia de escritura. RAID 10 proporciona una velocidad de lectura de doble canal y duplicación de datos ( _mirroring_ ) exacta en caliente. Si un disco falla críticamente durante una operación quirúrgica, el sistema continúa operando al 100% sin pérdida de datos de los pacientes. 

- **Subsistema de Red:** Doble tarjeta de red (NIC) de **10 GbE configurada en modo** **_Link Aggregation_ (LACP / Active-Active Bonding)** y conectada a switches redundantes de grado hospitalario. 

### **_1.2.2. Métricas de Rendimiento Esperadas y Análisis de Capacidad_** 

- **Capacidad de Operaciones de E/S (IOPS):** El arreglo NVMe en RAID 10 garantiza un mínimo de **300,000 IOPS en escritura aleatoria** , lo que permite registrar concurrentemente las fluctuaciones biométricas, recetas médicas e inicios de sesión sin cuellos de botella en el disco. 

- **Throughput de Red Sostenido:** El enlace agregado proporciona hasta **20 Gbps de ancho de banda teórico** . El procesamiento de las tramas biométricas de las incubadoras consume apenas ~15 Mbps (tramas livianas continuas), dejando el remanente libre para la transferencia fluida de archivos DICOM de imágenes médicas a las terminales de los especialistas. 

## **1.3. Arquitectura del Kernel y Diagrama de Flujo** 

### **_1.3.1. Justificación de la Arquitectura del Kernel y Modos de Ejecución_** 

Se opta por la implementación de un **Kernel de Tiempo Real Basado en Arquitectura Microkernel con Parche de Prioridades** . En este diseño, los componentes tradicionales del sistema operativo (sistemas de archivos, controladores de red y drivers de hardware médico) se ejecutan fuera del espacio privilegiado, operando en el **Modo Usuario** como servidores independientes. En el **Modo Kernel (Modo Privilegiado)** , solo permanecen las funciones mínimas indispensables: la planificación de hilos ( _scheduling_ ), la gestión de interrupciones de hardware y la comunicación entre procesos (IPC - _Inter-Process Communication_ ). 

Esta separación es fundamental por las siguientes razones: 

- **Aislamiento de Fallos y Tolerancia de Controladores:** Si la terminal de admisión o el controlador de red del ecógrafo sufren un desbordamiento de búfer o un fallo crítico de software, el error queda confinado en su espacio de direcciones de Modo Usuario. El servicio se reinicia de manera 

aislada mediante un proceso supervisor en milisegundos. El kernel principal nunca se cuelga ( _kernel panic_ ), garantizando que las pantallas de soporte vital de la UCIN sigan recibiendo energía computacional y datos biométricos de manera ininterrumpida. 

- **Mitigación de la Inversión de Prioridades:** El kernel incorpora el protocolo de **Herencia de Prioridades (Priority Inheritance Protocol)** . Si un hilo de baja prioridad (ej. impresión de ticket de farmacia) bloquea un semáforo de base de datos que el hilo de telemetría de la UCIN requiere con urgencia, el kernel eleva temporalmente la prioridad del hilo de farmacia al mismo nivel que la telemetría, forzándolo a liberar el recurso inmediatamente y evitando bloqueos indefinidos. 

### **_1.3.2. Descripción Textual del Flujo de Datos Arquitectónico_** 

El tránsito de la información dentro del ecosistema **SIMGESRC** sigue una trayectoria estrictamente jerarquizada y gobernada por el reloj del planificador del kernel: 

1. **Captura y Generación de Datos de Red:** Los sensores físicos de los monitores de signos vitales neonatales generan interrupciones periódicas cada 1,000 ms. El chip de la tarjeta de red (NIC) recibe los paquetes UDP correspondientes y dispara una interrupción de hardware (IRQ) directamente al procesador. 

2. **Procesamiento en Modo Kernel:** El planificador intercepta la IRQ en Modo 

Kernel. Al reconocer que el identificador del hilo de destino pertenece a la subrutina de telemetría crítica de la UCIN, el _scheduler_ aplica un desalojo ( _preemption_ ) inmediato sobre cualquier proceso activo de la consulta externa o administración. 

3. **Paso de Mensajes por IPC:** El Kernel transfiere los datos empaquetados desde los búferes de red del sistema hacia el espacio de memoria del módulo de análisis de alertas médicas a través de un mecanismo de memoria compartida protegida en Modo Usuario. 

4. **Visualización en Tiempo Real:** El hilo de la aplicación central de la UCIN lee los datos limpios y actualiza la pantalla del panel de enfermería en un tiempo determinista inferior a 5 milisegundos desde que el dato golpeó la tarjeta de red del servidor central, asegurando un monitoreo libre de desfases de tiempo. Por debajo de esta prioridad, las terminales de triaje y admisión acceden de forma intercalada a la CPU mediante ventanas de tiempo compartido.
