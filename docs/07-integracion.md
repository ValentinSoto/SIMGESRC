# MÓDULO 5: INTEGRACIÓN DEL SISTEMA (SIMGESRC)

### 5.1. Arquitectura de Integración de Componentes

```text
                 +----------------------------------+
                 |  Admisión de Procesos (Módulo 2) |
                 +-----------------+----------------+
                                   |
                                   v
                 +-----------------+----------------+
                 |  Validación de RAM (Módulo 4)    |  <-- MMU asigna marcos 4 KB
                 +-----------------+----------------+
                                   |
                                   v
                 +-----------------+----------------+
                 |  Control de Cierres (Módulo 3)  |  <-- Mutex/Semáforos
                 +----------------------------------+
```

---

### 5.2. Código Fuente Integrado de SIMGESRC (Python)

```python
import threading
import time
import math
import random

class MMU:
    def __init__(self, total_memory_kb=256, page_size_kb=4):
        self.total_memory = total_memory_kb
        self.page_size = page_size_kb
        self.num_frames = total_memory_kb // page_size_kb
        self.physical_memory = [None] * self.num_frames
        self.page_tables = {}
        self.mem_lock = threading.Lock()

    def allocate(self, pid, size_kb):
        with self.mem_lock:
            pages_needed = math.ceil(size_kb / self.page_size)
            free_frames = [i for i, val in enumerate(self.physical_memory) if val is None]
            if len(free_frames) < pages_needed:
                return False, 0
            residuo = size_kb % self.page_size
            internal_frag = (self.page_size - residuo) if residuo != 0 else 0
            self.page_tables[pid] = {}
            for i in range(pages_needed):
                frame = free_frames[i]
                self.physical_memory[frame] = pid
                self.page_tables[pid][i] = frame
            return True, internal_frag

    def deallocate(self, pid):
        with self.mem_lock:
            if pid not in self.page_tables:
                return False
            for frame in list(self.page_tables[pid].values()):
                self.physical_memory[frame] = None
            del self.page_tables[pid]
            return True

    def get_free_space(self):
        with self.mem_lock:
            return self.physical_memory.count(None) * self.page_size

class HospitalResources:
    def __init__(self):
        self.mutex_quirofano = threading.Lock()
        self.semaforo_sangre = threading.Semaphore(2)
        self.stock_sangre = 2

    def usar_quirofano(self, pid):
        print(f"🔒 [SYNCHRONIZATION] {pid} intentando bloquear Quirófano Central...")
        self.mutex_quirofano.acquire()
        print(f"🏥 [CRITICAL SECTION] {pid} ha tomado control EXCLUSIVO del Quirófano.")
        time.sleep(0.4)
        print(f"🔓 [SYNCHRONIZATION] {pid} finalizó cirugía y liberó el Quirófano.")
        self.mutex_quirofano.release()

    def solicitar_sangre(self, pid):
        print(f"💉 [SYNCHRONIZATION] {pid} solicitando paquete O- al Banco de Sangre...")
        self.semaforo_sangre.acquire()
        self.stock_sangre -= 1
        print(f"🩸 [CRITICAL SECTION] {pid} retiró sangre con éxito. Stock restante en Banco: {self.stock_sangre}")
        time.sleep(0.3)
        self.stock_sangre += 1
        print(f"🔄 [SYNCHRONIZATION] {pid} liberó/repuso contenedor de sangre. Stock disponible: {self.stock_sangre}")
        self.semaforo_sangre.release()

class SIMGESRC_Kernel:
    def __init__(self):
        self.mmu = MMU()
        self.recursos = HospitalResources()
        self.print_lock = threading.Lock()

    def safe_print(self, msg):
        with self.print_lock:
            print(msg)

    def ejecutar_proceso_hospitalario(self, pid, size_kb, burst_time, prioridad, tipo_recurso=None):
        self.safe_print(f"🚀 [KERNEL] Arribando {pid} al sistema. Peso: {size_kb}KB, Burst: {burst_time}ms, Prioridad: {prioridad}")
        success, frag = self.mmu.allocate(pid, size_kb)
        if not success:
            self.safe_print(f"❌ [MEMORY OUT] {pid} RECHAZADO por falta de espacio en la RAM. Requerido: {size_kb}KB. Espacio libre actual: {self.mmu.get_free_space()}KB")
            return
        
        self.safe_print(f"✅ [MEMORY ALLOC] {pid} cargado en RAM. Fragmentación interna: {frag}KB. Espacio libre restante: {self.mmu.get_free_space()}KB")
        time.sleep(burst_time * 0.05)
        
        if tipo_recurso == "QUIROFANO":
            self.recursos.usar_quirofano(pid)
        elif tipo_recurso == "SANGRE":
            self.recursos.solicitar_sangre(pid)
            
        self.mmu.deallocate(pid)
        self.safe_print(f"♻️  [KERNEL FREE] {pid} ha concluido su ciclo de vida. Memoria física devuelta de forma segura.")

if __name__ == "__main__":
    kernel = SIMGESRC_Kernel()
    lote_procesos = [
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P1_TraumaShock", 36, 4, 1, "QUIROFANO")),
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P2_Telemetria_UCIN", 56, 3, 2, None)),
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P3_Emergencia_Obstetrica", 48, 5, 1, "SANGRE")),
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P4_Cirugia_Pediatrica", 116, 6, 3, "QUIROFANO")),
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P5_Urgencia_Neonatal", 44, 8, 2, "SANGRE")),
        threading.Thread(target=kernel.ejecutar_proceso_hospitalario, args=("P6_Reporte_MINSA", 120, 12, 6, None))
    ]
    
    for hilo in lote_procesos:
        hilo.start()
        time.sleep(0.1)
        
    for hilo in lote_procesos:
        hilo.join()
```

---

### 5.3. Verificación de Resultados de la Simulación Integrada
- **Prevención Completa del Desborde de Memoria:** Si no hay suficiente espacio en la RAM, la MMU intercepta de inmediato la petición con `❌ [MEMORY OUT]`.
- **Mitigación Eficiente de Condiciones de Carrera:** `Mutex` asegura que solo una cirugía utilice el quirófano a la vez.
- **Funcionamiento de Semáforos:** La entrega de unidades del Banco de Sangre se regula dinámicamente según el contador inicial.

---

### 5.4. Conclusiones Generales del Proyecto
1. **Arquitectura:** La microarquitectura de kernel híbrido con soporte RTOS es fundamental para garantizar latencia determinista en la UCIN.
2. **Concurrencia:** Los mecanismos de exclusión mutua mediante Mutex y semáforos previenen la corrupción de datos y colisiones operativas.
3. **Memoria:** La paginación simple de 4 KB garantiza 0% de fragmentación externa, con un costo mínimo e inofensivo de fragmentación interna.

---

### 5.5. Declaración de Uso de Inteligencia Artificial
- **Porcentaje de asistencia de IA:** ~15% en el soporte de sintaxis para librerías nativas de Python (`threading`, `math`, `random`).
- **Análisis y Justificación:** 100% autoría y desarrollo analítico original de los integrantes.
