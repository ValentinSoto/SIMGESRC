class MemoryManager:
    def __init__(self, total_memory=1024, page_size=64):
        self.total_memory = total_memory
        self.page_size = page_size
        self.allocated_memory = 0
        self.pages = {}

    def allocate(self, process_id, size):
        if self.allocated_memory + size <= self.total_memory:
            self.allocated_memory += size
            self.pages[process_id] = size
            print(f"[MEMORY] Asignados {size} KB al PID {process_id}.")
            return True
        print(f"[MEMORY] Error: Memoria insuficiente para PID {process_id}.")
        return False

    def deallocate(self, process_id):
        if process_id in self.pages:
            size = self.pages.pop(process_id)
            self.allocated_memory -= size
            print(f"[MEMORY] Liberados {size} KB del PID {process_id}.")
