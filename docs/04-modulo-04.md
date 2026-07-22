# **MÓDULO 4: GESTIÓN DE MEMORIA** 

## **4.1. Estimación de Memoria por Segmento para los Procesos Hospitalarios** 

Se establece un tamaño de **Página / Marco (Frame) de $4\text{ KB}$** ($4096\text{ bytes}$). 

### **_Tabla 4.1: Estimación Cuantitativa de Huella de Memoria ($KB$)_** 

|**PI**<br>**D**|**Proceso**<br>**Hospitala**<br>**rio**|**Segme**<br>**nto**<br>**Texto**<br>**(KB)**|**Segme**<br>**nto**<br>**Datos**<br>**(KB)**|**Segme**<br>**nto**<br>**Heap**<br>**(KB)**|**Segme**<br>**nto**<br>**Stack**<br>**(KB)**|**Tamaño**<br>**Total**<br>**Requeri**<br>**do (KB)**|**Páginas**<br>**Necesari**<br>**as**<br>**(Techo**<br>**Total/4**<br>**⌈**<br>**)⌉**|
|---|---|---|---|---|---|---|---|
|**P**<br>**1**|Trauma<br>Shock<br>(Cesárea)|8|4|16|8|**36**|9<br>páginas|
|**P**<br>**2**|Telemetrí<br>a UCIN|12|8|32|4|**56**|14<br>páginas|
|**P**<br>**3**|Registro<br>de Triaje|16|12|8|12|**48**|12<br>páginas|
|**P**<br>**4**|Consulta<br>Ambulato<br>ria|20|16|64|16|**116**|29<br>páginas|
|**P**<br>**5**|Despacho<br>de<br>Farmacia|16|8|12|8|**44**|11<br>páginas|
|**P**|Reporte|32|24|128|32|**216**|54|



|**6**<br>MINSA|páginas|
|---|---|



## **4.2. Simulador de Paginación Simple en Python** 

Python 

import math 

class PagingMemorySimulator: 

def __init__(self, total_memory_kb=256, page_size_kb=4): 

self.total_memory = total_memory_kb 

self.page_size = page_size_kb 

self.num_frames = total_memory_kb // page_size_kb self.physical_memory = [None] * self.num_frames 

self.page_tables = {} self.internal_frag_by_proc = {} 

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

self.physical_memory[assigned_frame] = pid self.page_tables[pid][i] = assigned_frame 

return True 

def free(self, pid): if pid not in self.page_tables: return False 

frames_to_free = list(self.page_tables[pid].values()) 

for frame in frames_to_free: self.physical_memory[frame] = None del self.page_tables[pid] self.internal_frag_by_proc.pop(pid, 0) return True 

## **4.3. Análisis de Fragmentación Resultante** 

- **Fragmentación Externa (0% Garantizado):** Al segmentar el direccionamiento físico en marcos idénticos de $4\text{ KB}$, el Kernel puede asignar cualquier marco libre disponible para completar las páginas de un proceso, sin importar que estén dispersos espacialmente. Esto elimina de raíz la fragmentación externa. 

- **Fragmentación Interna (Última Página):** Al usarse asignación de tamaño rígido, se puede perder espacio únicamente en la última página del bloque si el tamaño del proceso no es un múltiplo exacto de $4\text{ KB}$. La fragmentación interna ($IF$) para un proceso se calcula mediante: 

$$IF = \text{Tamaño de Página} - (\text{Tamaño del Proceso} \pmod{\text{Tamaño de Página}})$$ 

Esta mínima pérdida localizada en un número acotado de procesos es insignificante frente a los beneficios de evitar la fragmentación externa en el sistema hospitalario. 
