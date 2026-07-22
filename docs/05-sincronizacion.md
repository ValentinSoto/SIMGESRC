# MÓDULO 3: SINCRONIZACIÓN Y CONCURRENCIA

### 3.1. Identificación y Justificación de las Secciones Críticas

1. **Quirófano de Emergencia (Sección Crítica 1 - Mutex):**
   - **Recurso:** Sala de Operaciones para Cesáreas de Urgencia.
   - **Solución:** `Mutex` (Exclusión Mutua Binary Lock).
2. **Banco de Sangre - Unidades de Factor O- (Sección Crítica 2 - Semáforo):**
   - **Recurso:** Stock de unidades de sangre (3 unidades disponibles).
   - **Solución:** `Counting Semaphore` inicializado en 3.

---

### 3.2. Implementación de Código en Python (Simulador de Concurrencia)

```python
import threading
import time
import random

class HospitalResources:
    def __init__(self):
        self.quirofano_ocupado = False
        self.mutex_quirofano = threading.Lock()
        self.stock_sangre_sin_sincro = 3
        self.stock_sangre_con_sincro = 3
        self.semaforo_sangre = threading.Semaphore(3)

recursos = HospitalResources()
print_lock = threading.Lock()

def log(mensaje):
    with print_lock:
        print(f"[{threading.current_thread().name}] {mensaje}")

def solicitar_quirofano_sin_sincronizacion(id_cirujano):
    log("Inicia solicitud de Quirófano (SIN MUTEX)...")
    if not recursos.quirofano_ocupado:
        time.sleep(random.uniform(0.1, 0.3)) 
        recursos.quirofano_ocupado = True
        log("💥 ¡COLISIÓN! Entró al Quirófano. Estado: ¡Ocupado simultáneamente!")
        time.sleep(0.5)
        recursos.quirofano_ocupado = False
        log("Salió del Quirófano.")
    else:
        log("Encontró el quirófano ocupado y esperará.")

def solicitar_quirofano_con_sincronizacion(id_cirujano):
    log("Inicia solicitud de Quirófano (CON MUTEX)...")
    recursos.mutex_quirofano.acquire()
    try:
        log("🔒 Quirófano adquirido de forma EXCLUSIVA. Iniciando cesárea...")
        recursos.quirofano_ocupado = True
        time.sleep(0.5)
        log("🔓 Cirugía finalizada con éxito. Liberando quirófano.")
        recursos.quirofano_ocupado = False
    finally:
        recursos.mutex_quirofano.release()

def solicitar_sangre_sin_sincronizacion(id_solicitante):
    if recursos.stock_sangre_sin_sincro > 0:
        time.sleep(random.uniform(0.1, 0.2))
        recursos.stock_sangre_sin_sincro -= 1
        log(f"💉 Retiró 1 unidad de sangre. Stock restante SIN SINCRO: {recursos.stock_sangre_sin_sincro}")
    else:
        log("❌ Intento de retiro fallido: Stock en 0.")

def solicitar_sangre_con_sincronizacion(id_solicitante):
    log("Esperando autorización del Banco de Sangre...")
    recursos.semaforo_sangre.acquire()
    recursos.stock_sangre_con_sincro -= 1
    log(f"🟢 [AUTORIZADO] Retiró 1 unidad de sangre de forma segura. Stock restante: {recursos.stock_sangre_con_sincro}")
    time.sleep(0.6)
    recursos.stock_sangre_con_sincro += 1
    log(f"🔄 Retorno de contenedor / Stock restablecido. Stock disponible: {recursos.stock_sangre_con_sincro}")
    recursos.semaforo_sangre.release()
```

---

### 3.3. Análisis del Comportamiento con y sin Sincronización
- **Sin Sincronización:** Ocurren condiciones de carrera (*race conditions*), colisiones en el uso del quirófano y stock negativo en el banco de sangre.
- **Con Sincronización:** Se garantiza la exclusión mutua estricta con Mutex y la gestión contable atómica con Semáforos.

---

### 3.4. Modelado y Prevención de Deadlocks (Bloqueos Mutuos)
- **Estrategia de Prevención:** **Ordenamiento Global de Recursos**. Todos los hilos deben solicitar recursos en orden numérico ascendente estricto para eliminar la espera circular.
