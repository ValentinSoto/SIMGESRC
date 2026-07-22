class Kernel:
    def __init__(self, scheduler, memory_manager, sync_manager):
        self.scheduler = scheduler
        self.memory_manager = memory_manager
        self.sync_manager = sync_manager
        self.is_running = False

    def boot(self):
        self.is_running = True
        print("[KERNEL] Sistema SIMGESRC iniciado correctamente.")

    def shutdown(self):
        self.is_running = False
        print("[KERNEL] Apagando el sistema...")
