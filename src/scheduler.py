from collections import deque

class Process:
    def __init__(self, pid, name, burst_time, priority=1):
        self.pid = pid
        self.name = name
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.priority = priority

class Scheduler:
    def __init__(self, algorithm="FCFS"):
        self.algorithm = algorithm
        self.ready_queue = deque()

    def add_process(self, process):
        self.ready_queue.append(process)
        print(f"[SCHEDULER] Proceso {process.name} (PID: {process.pid}) añadido a la cola.")

    def run(self):
        print(f"[SCHEDULER] Ejecutando algoritmo: {self.algorithm}")
        while self.ready_queue:
            proc = self.ready_queue.popleft()
            print(f"[SCHEDULER] Ejecutando PID {proc.pid} ({proc.name})...")
