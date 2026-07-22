# MÓDULO 3: Sincronización y Concurrencia

## 3.1 Identificación de Secciones Críticas

1. **Sección Crítica 1: Quirófano de Emergencia (Mutex)**
   * **Recurso:** Sala de operaciones para cesáreas de urgencia[cite: 11].
   * **Conflicto:** Múltiples cirujanos programando cirugías concurrentes[cite: 11].
   * **Solución:** Mutex (*Binary Lock*) exclusivo[cite: 11].

2. **Sección Crítica 2: Banco de Sangre (Semáforo)**
   * **Recurso:** Stock limitado de paquetes de sangre Factor O- (ej. 3 unidades)[cite: 11].
   * **Conflicto:** Solicitudes síncronas paralelas desde distintas áreas provocan lecturas/escrituras sucias[cite: 11].
   * **Solución:** Semáforo Contador (*Counting Semaphore*)[cite: 11].

---

## 3.2 Simulador de Concurrencia en Python

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

def solicitar_sangre_con_sincronizacion(id_solicitante):
    log("Esperando autorización del Banco de Sangre...")
    recursos.semaforo_sangre.acquire()
    recursos.stock_sangre_con_sincro -= 1
    log(f"🟢 [AUTORIZADO] Retiró 1 unidad de sangre de forma segura. Stock restante: {recursos.stock_sangre_con_sincro}")
    time.sleep(0.6)
    recursos.stock_sangre_con_sincro += 1
    log(f"💥 Retorno de contenedor / Stock restablecido. Stock disponible: {recursos.stock_sangre_con_sincro}")
    recursos.semaforo_sangre.release()
```[cite: 11]

---

## 3.3 Análisis de Resultados

* **Estado Sin Sincronización:** Ocurren colisiones de programación en el quirófano e inconsistencias con valores negativos en el inventario de sangre debido a condiciones de carrera (*race conditions*)[cite: 11].
* **Estado Con Sincronización:** El Mutex asegura la exclusión mutua absoluta en el quirófano y el Semáforo Contador limita de manera exacta el acceso concurrente al stock de sangre disponible[cite: 11].

---

## 3.4 Modelado y Prevención de Deadlocks

* **Escenario de Deadlock:** Médico A retiene la Sala de Ecografía (R1) y pide el Transductor Pediátrico (R2); Médico B retiene R2 y solicita R1[cite: 11].
* **Estrategia de Prevención:** **Ordenamiento Global de Recursos**. Obliga a todo hilo a solicitar recursos exclusivamente en orden ascendente por su ID numérico, eliminando la condición de espera circular de Coffman[cite: 11].
