class Mutex:
    def __init__(self, name="DefaultMutex"):
        self.name = name
        self.locked = False
        self.owner = None

    def acquire(self, process_id):
        if not self.locked:
            self.locked = True
            self.owner = process_id
            print(f"[SYNC] Mutex '{self.name}' bloqueado por PID {process_id}.")
            return True
        print(f"[SYNC] Mutex '{self.name}' está ocupado. PID {process_id} en espera.")
        return False

    def release(self, process_id):
        if self.locked and self.owner == process_id:
            self.locked = False
            self.owner = None
            print(f"[SYNC] Mutex '{self.name}' liberado por PID {process_id}.")
            return True
        return False
