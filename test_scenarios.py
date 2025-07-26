from fsm_states import CarDoorLockFSM


scenarios = [
    {"event": "lock", "reason": "Car shifted to Drive"},
    {"event": "unlock", "reason": "Car shifted to Park"},
    # ...add more scenarios as needed...
]

def run_tests():
    fsm = CarDoorLockFSM
    fsm.update("key", "brake", "gear")  # Example initial state

    test_cases = [
        {"key": True, "brake": True, "gear": "D"},
        {"key": False, "brake": False, "gear": "P"},
        {"key": True, "brake": False, "gear": "R"},
        {"key": True, "brake": True, "gear": "N"},
        {"key": False, "brake": False, "gear": "D"},
    ]

    print("🚗 Running test scenarios for Smart Door Lock FSM...\n")
    for i, case in enumerate(test_cases):
        result = fsm.get_state(case["key"], case["brake"], case["gear"])
        print(f"Test Case {i+1}: Key={case['key']}, Brake={case['brake']}, Gear={case['gear']} → Door: {result}")

if __name__ == "__main__":
    run_tests()
