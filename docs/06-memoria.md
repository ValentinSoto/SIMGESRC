# MÓDULO 4: GESTIÓN DE MEMORIA

### 4.1. Estimación de Memoria por Segmento para los Procesos Hospitalarios
Tamaño de Página / Marco (Frame): $4\text{ KB}$ ($4096\text{ bytes}$).

#### Tabla 4.1: Estimación Cuantitativa de Huella de Memoria (KB)

| PID | Proceso Hospitalario | Texto (KB) | Datos (KB) | Heap (KB) | Stack (KB) | Total (KB) | Páginas (⌈Total/4⌉) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **P1** | Trauma Shock (Cesárea) | 8 | 4 | 16 | 8 | **36** | 9 páginas |
| **P2** | Telemetría UCIN | 12 | 8 | 32 | 4 | **56** | 14 páginas |
| **P3** | Registro de Triaje | 16 | 12 | 8 | 12 | **48** | 12 páginas |
| **P4** | Consulta Ambulatoria | 20 | 16 | 64 | 16 | **116** | 29 páginas |
| **P5** | Despacho de Farmacia | 16 | 8 | 12 | 8 | **44** | 11 páginas |
| **P6** | Reporte MINSA | 32 | 24 | 128 | 32 | **216** | 54 páginas |

---

### 4.2. Simulador de Paginación Simple en Python

```python
import math

class PagingMemorySimulator:
    def __init__(self, total_memory_kb=256, page_size_kb=4):
        self.total_memory = total_memory_kb
        self.page_size = page_size_kb
        self.num_frames = total_memory_kb // page_size_kb
        self.physical_memory = [None] * self.num_frames
        self.page_tables = {}
        self.internal_frag_by_proc = {}

    def get_free_frames(self):
        return [i for i, val in enumerate(self.physical_memory) if val is None]

    def alloc(self, pid, size_kb):
        pages_needed = math.ceil(size_kb / self.page_size)
        free_frames = self.get_free_frames()
        if len(free_frames) < pages_needed:
            return False
        
        residuo = size_kb % self.page_size
        internal_frag = (self.page_size - residuo) if residuo != 0 else 0
        self.internal_frag_by_proc[pid] = internal_frag
        
        self.page_tables[pid] = {}
        for i in range(pages_needed):
            assigned_frame = free_frames[i]
            self.physical_memory[assigned_frame] = pid
            self.page_tables[pid][i] = assigned_frame
        return True

    def free(self, pid):
        if pid not in self.page_tables:
            return False
        frames_to_free = list(self.page_tables[pid].values())
        for frame in frames_to_free:
            self.physical_memory[frame] = None
        del self.page_tables[pid]
        self.internal_frag_by_proc.pop(pid, 0)
        return True
```

---

### 4.3. Análisis de Fragmentación Resultante
- **Fragmentación Externa:** **0% Garantizado** gracias al esquema de paginación por marcos fijos.
- **Fragmentación Interna:** Ocurre solo en la última página de cada proceso.
  $$IF = \text{Tamaño de Página} - (\text{Tamaño del Proceso} \pmod{\text{Tamaño de Página}})$$
