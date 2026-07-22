# MÓDULO 4: Gestión de Memoria

## 4.1 Estimación de Memoria por Segmento (Página = 4 KB)

| PID | Proceso Hospitalario | Texto (KB) | Datos (KB) | Heap (KB) | Stack (KB) | Total Requerido | Páginas Necesarias ($\lceil\text{Total}/4\rceil$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **P1** | Trauma Shock (Cesárea) | 8 | 4 | 16 | 8 | **36 KB** | **9 páginas**[cite: 11] |
| **P2** | Telemetría UCIN | 12 | 8 | 32 | 4 | **56 KB** | **14 páginas**[cite: 11] |
| **P3** | Registro de Triaje | 16 | 12 | 8 | 12 | **48 KB** | **12 páginas**[cite: 11] |
| **P4** | Consulta Ambulatoria | 20 | 16 | 64 | 16 | **116 KB** | **29 páginas**[cite: 11] |
| **P5** | Despacho de Farmacia | 16 | 8 | 12 | 8 | **44 KB** | **11 páginas**[cite: 11] |
| **P6** | Reporte MINSA | 32 | 24 | 128 | 32 | **216 KB** | **54 páginas**[cite: 11] |

---

## 4.2 Simulador de Paginación Simple en Python

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
        for frame in list(self.page_tables[pid].values()):
            self.physical_memory[frame] = None
        del self.page_tables[pid]
        self.internal_frag_by_proc.pop(pid, 0)
        return True
```[cite: 11]

---

## 4.3 Análisis de Fragmentación Resultante

* **Fragmentación Externa (0% Garantizado):** La asignación por marcos idénticos de 4 KB permite mapear páginas no contiguas en RAM, eliminando totalmente la fragmentación externa[cite: 11].
* **Fragmentación Interna:** Ocurre únicamente en la última página del bloque si la solicitud no es múltiplo de 4 KB:
  $$IF = \text{Tamaño de Página} - (\text{Tamaño de Proceso} \pmod{\text{Tamaño de Página}})$$
[cite: 11]
