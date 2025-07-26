# door_lock_simulator.py

from fsm_states import fsm, current_state
from test_scenarios import scenarios
import time
import csv
from datetime import datetime

def log_action(action, reason):
    with open("lock_log.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), action, reason])

def run_simulation():
    global current_state
    print("🚗 Smart Door Lock Simulation Started")
    print("-" * 40)

    for scenario in scenarios:
        print(f"\n[INPUT] {scenario['event']} =>", end=" ")
        next_state = fsm.get((current_state, scenario["event"]))
        if next_state:
            reason = scenario.get("reason", "State change")
            log_action(f"{current_state} → {next_state}", reason)
            print(f"[STATE CHANGE] {current_state} → {next_state} | Reason: {reason}")
            current_state = next_state
        else:
            print(f"[NO CHANGE] Remains in {current_state}")
        time.sleep(1)

    print("\n✅ Simulation finished. Logs saved to lock_log.csv")

if __name__ == "__main__":
    run_simulation()

