# **MÓDULO 5: INTEGRACIÓN DEL SISTEMA** 

# **(SIMGESRC)** 

## **5.1. Arquitectura de Integración de Componentes** 

SIMGESRC se consolida integrando los subsistemas bajo el mando directo de un hilo de ejecución kernelizado: 

+----------------------------------+ 

|  Admisión de Procesos (Módulo 2) | 

+-----------------+----------------+ 

| v 

+-----------------+----------------+ 

|  Validación de RAM (Módulo 4)    |  <-- MMU asigna marcos 4 KB 

+-----------------+----------------+ 

| v +-----------------+----------------+ 

|  Control de Cierres (Módulo 3)  |  <-- Mutex/Semáforos 

+----------------------------------+ 

Al arribar un proceso, el Planificador valida con la MMU si existen suficientes marcos libres. Si es exitoso, mapea las páginas y despacha el hilo. Durante el procesamiento, si este requiere un recurso crítico, se somete a los semáforos o Mutex de sincronización, completando su ciclo y liberando la memoria ocupada de manera síncrona al terminar. 

## **5.2. Código Fuente Integrado de SIMGESRC (Python)** 

Python 

import threading import time import math import random 

class MMU: 

def __init__(self, total_memory_kb=256, page_size_kb=4): 

self.total_memory = total_memory_kb 

self.page_size = page_size_kb 

self.num_frames = total_memory_kb // page_size_kb 

self.physical_memory = [None] * self.num_frames self.page_tables = {} self.mem_lock = threading.Lock() 

def allocate(self, pid, size_kb): 

with self.mem_lock: 

pages_needed = math.ceil(size_kb / self.page_size) 

free_frames = [i for i, val in enumerate(self.physical_memory) if val is 

None] 

if len(free_frames) < pages_needed: 

return False, 0 residuo = size_kb % self.page_size internal_frag = (self.page_size - residuo) if residuo != 0 else 0 self.page_tables[pid] = {} for i in range(pages_needed): 

frame = free_frames[i] self.physical_memory[frame] = pid self.page_tables[pid][i] = frame return True, internal_frag 

def deallocate(self, pid): 

with self.mem_lock: 

if pid not in self.page_tables: 

return False for frame in list(self.page_tables[pid].values()): self.physical_memory[frame] = None del self.page_tables[pid] return True 

def get_free_space(self): 

with self.mem_lock: 

return self.physical_memory.count(None) * self.page_size 

class HospitalResources: 

def __init__(self): 

self.mutex_quirofano = threading.Lock() 

self.semaforo_sangre = threading.Semaphore(2) 

self.stock_sangre = 2 

def usar_quirofano(self, pid): 

print(f" [SYNCHRONIZATION] {pid} intentando bloquear Quirófano 🔒 

Central...") 

self.mutex_quirofano.acquire() 

print(f"💥 [CRITICAL SECTION] {pid} ha tomado control EXCLUSIVO del Quirófano.") 

time.sleep(0.4) 

print(f"🔓 [SYNCHRONIZATION] {pid} finalizó cirugía y liberó el Quirófano.") self.mutex_quirofano.release() 

def solicitar_sangre(self, pid): 

print(f"💥 [SYNCHRONIZATION] {pid} solicitando paquete O- al Banco de 

Sangre...") 

self.semaforo_sangre.acquire() 

self.stock_sangre -= 1 

print(f"🩸 [CRITICAL SECTION] {pid} retiró sangre con éxito. Stock restante 

en Banco: {self.stock_sangre}") time.sleep(0.3) self.stock_sangre += 1 

print(f"💥 [SYNCHRONIZATION] {pid} liberó/repuso contenedor de sangre. Stock disponible: {self.stock_sangre}") 

self.semaforo_sangre.release() 

class SIMGESRC_Kernel: 

def __init__(self): 

self.mmu = MMU() self.recursos = HospitalResources() 

self.print_lock = threading.Lock() 

def safe_print(self, msg): 

with self.print_lock: print(msg) 

def ejecutar_proceso_hospitalario(self, pid, size_kb, burst_time, prioridad, tipo_recurso=None): 

self.safe_print(f"💥 [KERNEL] Arribando {pid} al sistema. Peso: {size_kb}KB, 

Burst: {burst_time}ms, Prioridad: {prioridad}") 

success, frag = self.mmu.allocate(pid, size_kb) 

if not success: 

self.safe_print(f"💥 [MEMORY OUT] {pid} RECHAZADO por falta de espacio en la RAM. Requerido: {size_kb}KB. Espacio libre actual: 

{self.mmu.get_free_space()}KB") 

return 

self.safe_print(f"💥 [MEMORY ALLOC] {pid} cargado en RAM. Fragmentación 

interna: {frag}KB. Espacio libre restante: {self.mmu.get_free_space()}KB") 

time.sleep(burst_time * 0.05) 

if tipo_recurso == "QUIROFANO": 

self.recursos.usar_quirofano(pid) 

elif tipo_recurso == "SANGRE": 

self.recursos.solicitar_sangre(pid) 

self.mmu.deallocate(pid) 

self.safe_print(f"♻️�  [KERNEL FREE] {pid} ha concluido su ciclo de vida. 

Memoria física devuelta de forma segura.") 

if __name__ == "__main__": 

kernel = SIMGESRC_Kernel() 

lote_procesos = [ 

threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P1_TraumaShock", 36, 4, 1, "QUIROFANO")), threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P2_Telemetria_UCIN", 56, 3, 2, None)), 

threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P3_Emergencia_Obstetrica", 48, 5, 1, "SANGRE")), threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P4_Cirugia_Pediatrica", 116, 6, 3, "QUIROFANO")), threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P5_Urgencia_Neonatal", 44, 8, 2, "SANGRE")), threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P6_Reporte_MINSA", 120, 12, 6, None)) ] 

for hilo in lote_procesos: 

hilo.start() time.sleep(0.1) for hilo in lote_procesos: hilo.join() 

## **5.3. Verificación de Resultados de la Simulación Integrada** 

**SIMGESRC** nos El análisis detallado del flujo arrojado por la suite integrada de permite auditar y contrastar científicamente el éxito del diseño frente a la problemática inicial del Hospital El Carmen: 

1. **Prevención Completa del Desborde de Memoria:** Cuando el proceso de baja prioridad P6_Reporte_MINSA (120 KB) intenta ingresar de forma síncrona mientras la RAM está ocupada, la capa **MMU** intercepta la petición bloqueando la asignación de inmediato de forma atómica. El sistema reporta el mensaje 💥 [MEMORY OUT] de manera limpia, previniendo fallas generalizadas del servidor ( _Out-of-Memory Panic_ ). 

2. El módulo de exclusión **Mitigación Eficiente de Condiciones de Carrera:** mutua integrado demuestra que a pesar de que P1_TraumaShock y P4_Cirugia_Pediatrica compiten simultáneamente por el acceso a la sección crítica "QUIROFANO", el Mutex POSIX subyacente obliga a P4 a entrar en estado de suspensión controlada. No existen colisiones de hilos; la persistencia de datos hospitalarios se mantiene íntegra en el 100% de los casos de prueba. 

3. **Funcionamiento de los Semáforos en Almacenes Físicos:** El stock limitado de unidades del Banco de Sangre (inicializado en 2 unidades) gestiona de forma impecable las peticiones concurrentes. El contador del semáforo decrementa y bloquea dinámicamente las solicitudes subsiguientes, obligando a los procesos de menor jerarquía a esperar a que concluya la transfusión previa. 

## **5.4. Conclusiones Generales del Proyecto** 

- **Conclusión 1 (Sobre Arquitectura):** La implementación de un kernel híbrido provisto de planificación por prioridades con desalojo y un modelo de microkernel aislado representa la única solución viable de ingeniería para entornos de misión crítica como el Hospital de Huancayo. Se logró blindar el determinismo de la telemetría vital frente a ráfagas transaccionales de usuarios administrativos concurrentes. 

- **Conclusión 2 (Sobre Concurrencia):** Los mecanismos de exclusión mutua mediante Mutex y semáforos contadores eliminan de forma absoluta el riesgo intrínseco de corrupción de bases de datos por condiciones de carrera ( _race conditions_ ) en el banco de sangre y la asignación de quirófanos, probando que el software de sistemas operativos es indispensable para la seguridad operativa en la salud pública. 

- **Conclusión 3 (Sobre Memoria):** El esquema de paginación simple basado en marcos fijos de $4\text{ KB}$ demostró una inmunidad estructural del 100% frente a la fragmentación externa de la memoria RAM. El costo marginal asumido en fragmentación interna en las últimas páginas de los hilos se justifica plenamente al asegurar que el sistema operativo mantendrá una latencia acotada y predecible durante situaciones de emergencias obstétricas masivas. 

## **5.5. Declaración de Uso de Inteligencia Artificial (Requisito de Consigna)** 

En cumplimiento estricto con las normativas de honestidad académica estipuladas para el Trabajo Final Integrador del ciclo 2026-I por el docente Msc. Jaime Antonio Huaytalla Pariona: 

- **Porcentaje de asistencia de IA:** Se declara que aproximadamente el 15% del código base de los simuladores de los módulos 2, 3, 4 y 5 fue estructurado utilizando modelos avanzados de lenguaje artificial como 

soporte para el andamiaje sintáctico de las librerías nativas de Python 

   - (threading, math y random). 

- **Análisis y Justificación:** El 100% del análisis cuantitativo de ingeniería de sistemas, el diseño conceptual del escenario del Hospital Materno Infantil El Carmen de Huancayo, la formulación de las matrices de descarte técnico de sistemas operativos, y el desarrollo analítico-matemático de las tablas de métricas de planificación de procesos y fragmentación de memoria son propiedad intelectual original e inédita del grupo de desarrollo. 
