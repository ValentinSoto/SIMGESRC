# **MÓDULO 3: SINCRONIZACIÓN Y CONCURRENCIA** 

## **3.1. Identificación y Justificación de las Secciones Críticas** 

En el sistema **SIMGESRC** , se han identificado dos recursos compartidos de alta criticidad que representan nuestras secciones críticas: 

#### **1. Quirófano de Emergencia (Sección Crítica 1 - Mutex):** 

- a. _Recurso:_ La Sala de Operaciones para Cesáreas de Urgencia. 

- b. _Conflicto:_ Múltiples cirujanos (hilos) intentan programar cirugías concurrentes en el mismo quirófano físico. Si dos hilos acceden en el mismo milisegundo, se podría registrar a dos pacientes distintos en el mismo espacio. 

- c. _Solución:_ Un **Mutex (Exclusión Mutua Binary Lock)** . Solo un 

   - médico puede poseer la "llave" del quirófano a la vez. 

#### **2. Banco de Sangre - Unidades de Factor O- (Sección Crítica 2 - Semáforo):** 

- a. _Recurso:_ Un stock limitado de unidades o paquetes de sangre (ej. 3 unidades disponibles). 

- b. Diferentes áreas solicitan de forma síncrona unidades de _Conflicto:_ sangre para transfusiones. Si múltiples hilos descuentan el inventario concurrentemente sin sincronización, ocurrirá una lectura/escritura sucia. 

- c. _Solución:_ Un **Semáforo Contador (Counting Semaphore)** inicializado con el número exacto de unidades disponibles. 

## **3.2. Implementación de Código en Python (Simulador de Concurrencia)** 

Python 

import threading import time import random 

class HospitalResources: 

def __init__(self): 

self.quirofano_ocupado = False self.mutex_quirofano = threading.Lock() self.stock_sangre_sin_sincro = 3 self.stock_sangre_con_sincro = 3 self.semaforo_sangre = threading.Semaphore(3) 

recursos = HospitalResources() print_lock = threading.Lock() 

def log(mensaje): 

with print_lock: 

print(f"[{threading.current_thread().name}] {mensaje}") 

def solicitar_quirofano_sin_sincronizacion(id_cirujano): 

- log("Inicia solicitud de Quirófano (SIN MUTEX)...") 

- if not recursos.quirofano_ocupado: 

- time.sleep(random.uniform(0.1, 0.3)) 

- recursos.quirofano_ocupado = True 

log("💥 ¡COLISIÓN! Entró al Quirófano. Estado: ¡Ocupado simultáneamente!") time.sleep(0.5) 

recursos.quirofano_ocupado = False 

log("Salió del Quirófano.") 

else: 

log("Encontró el quirófano ocupado y esperará.") 

def solicitar_quirofano_con_sincronizacion(id_cirujano): 

log("Inicia solicitud de Quirófano (CON MUTEX)...") 

recursos.mutex_quirofano.acquire() 

try: 

- log(" Quirófano adquirido de forma EXCLUSIVA. Iniciando cesárea...")🔒 

recursos.quirofano_ocupado = True 

time.sleep(0.5) 

log("🔓 Cirugía finalizada con éxito. Liberando quirófano.") 

recursos.quirofano_ocupado = False finally: 

recursos.mutex_quirofano.release() 

def solicitar_sangre_sin_sincronizacion(id_solicitante): 

- if recursos.stock_sangre_sin_sincro > 0: 

time.sleep(random.uniform(0.1, 0.2)) 

recursos.stock_sangre_sin_sincro -= 1 

log(f"💥 Retiró 1 unidad de sangre. Stock restante SIN SINCRO: 

{recursos.stock_sangre_sin_sincro}") 

else: 

log("💥 Intento de retiro fallido: Stock en 0.") 

def solicitar_sangre_con_sincronizacion(id_solicitante): 

- log("Esperando autorización del Banco de Sangre...") 

- recursos.semaforo_sangre.acquire() 

recursos.stock_sangre_con_sincro -= 1 

- log(f"🟢 [AUTORIZADO] Retiró 1 unidad de sangre de forma segura. Stock restante: {recursos.stock_sangre_con_sincro}") 

- time.sleep(0.6) 

recursos.stock_sangre_con_sincro += 1 

log(f"💥 Retorno de contenedor / Stock restablecido. Stock disponible: 

- {recursos.stock_sangre_con_sincro}") 

- recursos.semaforo_sangre.release() 

## **3.3. Análisis del Comportamiento con y sin Sincronización** 

- **Estado Sin Sincronización (Condición de Carrera):** Al ocurrir cambios de contexto involuntarios antes de reescribir la variable booleana quirofano_ocupado, múltiples hilos determinan que la sala está "libre" casi de manera simultánea, causando colisiones críticas de programación de quirófanos. En el banco de sangre, múltiples lecturas y decisiones concurrentes dejan el stock lógico en valores negativos inconsistentes. 

- **Estado Con Sincronización (Garantía de Exclusión):** Con el Mutex, el primer hilo en llegar bloquea el recurso. Los cirujanos restantes se suspenden voluntariamente y entran en una cola de espera bloqueada por el Kernel. El semáforo contador permite el acceso controlado a un número finito de unidades de sangre (en este caso, 3), mandando a los hilos sobrantes a un estado de bloqueo síncrono hasta la liberación del recurso. 

## **3.4. Modelado y Prevención de Deadlocks (Bloqueos Mutuos)** 

- **Escenario de Deadlock en el Hospital:** Ocurre cuando el Médico A tiene asignada la Sala de Ecografía (Recurso 1) y requiere el Transductor Pediátrico (Recurso 2), mientras que el Médico B retiene el Transductor Pediátrico (Recurso 2) y requiere la Sala de Ecografía (Recurso 1). Ambos se bloquean indefinidamente. 

- **Estrategia de Prevención de SIMGESRC:** Se implementa la técnica de **Ordenamiento Global de Recursos** . Al asignar un índice numérico estricto a cada recurso del hospital, la regla del Kernel obliga a todo hilo a adquirir múltiples recursos exclusivamente en orden ascendente (ej. siempre bloquear el Recurso 1 antes del Recurso 2). Esto rompe de manera absoluta la posibilidad de una espera circular (una de las 4 condiciones de Coffman). 
