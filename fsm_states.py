

class CarDoorLockFSM:
    def __init__(self):
        self.state = "UNLOCKED"
        # Example FSM and state (replace with your actual logic)
        self.fsm = {
            ("LOCKED", "unlock"): "UNLOCKED",
            ("UNLOCKED", "lock"): "LOCKED",
            # ... add other transitions ...
        }
        self.current_state = "UNLOCKED"

    def update(self, key, brake, gear):
        # Example logic (replace with your actual FSM logic)
        if key and brake and gear in ("D", "R"):
            self.state = "LOCKED"
        else:
            self.state = "UNLOCKED"
        return self.state

# Expose FSM and state for simulator
fsm = {
    ("LOCKED", "unlock"): "UNLOCKED",
    ("UNLOCKED", "lock"): "LOCKED",
    # ... add other transitions ...
}
current_state = "UNLOCKED"
