from kernel import Kernel
from scheduler import Scheduler, Process
from memory import MemoryManager
from synchronization import Mutex

def main():
    scheduler = Scheduler(algorithm="FCFS")
    memory = MemoryManager(total_memory=512)
    sync = Mutex(name="ResourceLock")

    kernel = Kernel(scheduler, memory, sync)
    kernel.boot()

    # Ejemplo de prueba básica
    p1 = Process(pid=1, name="Proceso_A", burst_time=5)
    memory.allocate(p1.pid, 128)
    scheduler.add_process(p1)
    
    sync.acquire(p1.pid)
    scheduler.run()
    sync.release(p1.pid)
    memory.deallocate(p1.pid)

    kernel.shutdown()

if __name__ == "__main__":
    main()
