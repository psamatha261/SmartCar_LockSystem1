"""
Enhanced Smart Door Lock Simulator
Realistic simulation with varied timing patterns and comprehensive logging
"""

import time
import csv
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from fsm_states import SmartDoorLockFSM, TriggerType, SecurityLevel, LockState
from test_scenarios import scenarios, RealisticTestRunner

class EnhancedDoorLockSimulator:
    """Enhanced simulator with realistic patterns and comprehensive logging"""
    
    def __init__(self, log_file: str = "lock_log.csv"):
        self.log_file = log_file
        self.fsm = SmartDoorLockFSM()
        self.simulation_start_time = datetime.now()
        self.total_events = 0
        self.user_behavior_patterns = self._initialize_user_patterns()
        self.environmental_factors = self._initialize_environmental_factors()
        
        # Initialize CSV log file with headers
        self._initialize_log_file()
        
    def _initialize_log_file(self):
        """Initialize the CSV log file with proper headers"""
        try:
            with open(self.log_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timestamp", "action", "reason", "trigger_type", "user_id", 
                    "success", "battery_level", "temperature", "connectivity",
                    "failed_attempts", "state_before", "state_after"
                ])
        except Exception as e:
            print(f"Warning: Could not initialize log file: {e}")
    
    def _initialize_user_patterns(self) -> Dict[str, Dict]:
        """Initialize realistic user behavior patterns"""
        return {
            "admin": {
                "activity_level": "high",
                "preferred_methods": ["mobile_app", "keypad", "biometric"],
                "time_patterns": {
                    "morning": (7, 9),
                    "evening": (17, 22),
                    "weekend": (9, 23)
                },
                "security_conscious": True
            },
            "user1": {
                "activity_level": "medium",
                "preferred_methods": ["proximity", "mobile_app", "keypad"],
                "time_patterns": {
                    "morning": (7, 8),
                    "evening": (18, 20),
                    "weekend": (10, 22)
                },
                "security_conscious": False
            },
            "guest": {
                "activity_level": "low",
                "preferred_methods": ["keypad"],
                "time_patterns": {
                    "visit": (14, 18)
                },
                "security_conscious": False
            }
        }
    
    def _initialize_environmental_factors(self) -> Dict[str, Any]:
        """Initialize environmental simulation factors"""
        return {
            "weather_conditions": ["sunny", "rainy", "stormy", "cold"],
            "current_weather": "sunny",
            "network_stability": 0.95,  # 95% uptime
            "power_stability": 0.98,    # 98% uptime
            "sensor_reliability": 0.99, # 99% reliability
            "battery_drain_rate": 0.1,  # % per hour under normal conditions
            "temperature_variation": 2.0  # ±2°C variation
        }
    
    def log_enhanced_action(self, action: str, reason: str, trigger_type: TriggerType = TriggerType.SYSTEM, 
                          user_id: str = "", success: bool = True):
        """Enhanced logging with comprehensive data"""
        try:
            system_status = self.fsm.get_system_status()
            
            with open(self.log_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().isoformat(),
                    action,
                    reason,
                    trigger_type.value,
                    user_id,
                    success,
                    system_status['battery_level'],
                    system_status['temperature'],
                    system_status['connectivity'],
                    system_status['failed_attempts'],
                    system_status.get('previous_state', ''),
                    system_status['current_state']
                ])
            
            self.total_events += 1
            
        except Exception as e:
            print(f"Error logging action: {e}")
    
    def simulate_realistic_day(self, day_type: str = "weekday"):
        """Simulate a full day with realistic patterns"""
        print(f"🌅 Simulating Realistic {day_type.title()} Pattern")
        print("-" * 50)
        
        # Define time periods and typical activities
        if day_type == "weekday":
            time_periods = [
                {"period": "early_morning", "start": 6, "end": 8, "activity": "high"},
                {"period": "morning", "start": 8, "end": 12, "activity": "low"},
                {"period": "afternoon", "start": 12, "end": 17, "activity": "medium"},
                {"period": "evening", "start": 17, "end": 22, "activity": "high"},
                {"period": "night", "start": 22, "end": 24, "activity": "low"}
            ]
        else:  # weekend
            time_periods = [
                {"period": "morning", "start": 8, "end": 12, "activity": "medium"},
                {"period": "afternoon", "start": 12, "end": 18, "activity": "high"},
                {"period": "evening", "start": 18, "end": 23, "activity": "medium"},
                {"period": "night", "start": 23, "end": 24, "activity": "low"}
            ]
        
        for period in time_periods:
            print(f"\n***  {period['period'].title()} ({period['start']}:00-{period['end']}:00)")
            self._simulate_time_period(period)
            
            # Add realistic delays between periods
            time.sleep(random.uniform(1, 3))
    
    def _simulate_time_period(self, period: Dict[str, Any]):
        """Simulate activities during a specific time period"""
        activity_level = period['activity']
        
        # Determine number of events based on activity level
        if activity_level == "high":
            num_events = random.randint(3, 6)
        elif activity_level == "medium":
            num_events = random.randint(1, 3)
        else:  # low
            num_events = random.randint(0, 2)
        
        for _ in range(num_events):
            self._simulate_realistic_event(period['period'])
            
            # Variable delays between events
            delay = self._calculate_realistic_delay(activity_level)
            time.sleep(delay)
    
    def _simulate_realistic_event(self, time_period: str):
        """Simulate a single realistic event"""
        # Apply environmental factors
        self._apply_environmental_effects()
        
        # Choose event type based on time period and user patterns
        event_type = self._choose_event_type(time_period)
        user_id = self._choose_active_user(time_period)
        
        # Execute the event
        success, message = self._execute_realistic_event(event_type, user_id, time_period)
        
        # Log the event
        trigger_type = self._get_trigger_type_for_event(event_type)
        self.log_enhanced_action(
            action=f"{self.fsm.previous_state.value if self.fsm.previous_state else 'UNKNOWN'} → {self.fsm.current_state.value}",
            reason=f"{time_period} {event_type} by {user_id}",
            trigger_type=trigger_type,
            user_id=user_id,
            success=success
        )
        
        # Display result
        status_icon = "[OK]" if success else "*** "
        print(f"   {status_icon} {event_type} by {user_id}: {message}")
        print(f"      State: {self.fsm.current_state.value} | Battery: {self.fsm.battery_level:.1f}%")
    
    def _choose_event_type(self, time_period: str) -> str:
        """Choose realistic event type based on time period"""
        event_probabilities = {
            "early_morning": ["unlock", "disarm", "unlock", "lock"],
            "morning": ["lock", "arm", "unlock", "lock"],
            "afternoon": ["unlock", "lock", "guest_access"],
            "evening": ["unlock", "disarm", "lock", "unlock"],
            "night": ["lock", "arm", "lock"]
        }
        
        possible_events = event_probabilities.get(time_period, ["unlock", "lock"])
        return random.choice(possible_events)
    
    def _choose_active_user(self, time_period: str) -> str:
        """Choose which user is likely to be active"""
        # Weight users based on time period
        if time_period in ["early_morning", "morning", "evening"]:
            users = ["user1", "user1", "admin"]  # user1 more likely
        elif time_period == "afternoon":
            users = ["user1", "admin", "guest"]  # guest visits possible
        else:
            users = ["user1", "admin"]
        
        return random.choice(users)
    
    def _execute_realistic_event(self, event_type: str, user_id: str, time_period: str) -> tuple:
        """Execute a realistic event with proper trigger data"""
        # Choose method based on user preferences
        user_pattern = self.user_behavior_patterns.get(user_id, self.user_behavior_patterns["user1"])
        method = random.choice(user_pattern["preferred_methods"])
        
        # Prepare trigger data
        trigger_data = {"user_id": user_id}
        trigger_type = TriggerType.SYSTEM
        
        if method == "keypad":
            trigger_type = TriggerType.KEYPAD
            # Simulate occasional wrong codes
            if random.random() < 0.05:  # 5% chance of wrong code
                trigger_data["code"] = "wrong"
            else:
                codes = {"admin": "1234", "user1": "5678", "guest": "0000"}
                trigger_data["code"] = codes.get(user_id, "5678")
        
        elif method == "biometric":
            trigger_type = TriggerType.BIOMETRIC
            trigger_data["biometric_data"] = f"{user_id}_print"
        
        elif method == "mobile_app":
            trigger_type = TriggerType.MOBILE_APP
            trigger_data["command"] = event_type
        
        elif method == "proximity":
            trigger_type = TriggerType.PROXIMITY
        
        # Handle special event types
        if event_type == "guest_access":
            trigger_type = TriggerType.KEYPAD
            trigger_data = {"code": "0000"}
        
        elif event_type in ["arm", "disarm"]:
            trigger_type = TriggerType.MOBILE_APP
            trigger_data["command"] = event_type
        
        # Execute the trigger
        return self.fsm.process_trigger(trigger_type, trigger_data)
    
    def _get_trigger_type_for_event(self, event_type: str) -> TriggerType:
        """Get appropriate trigger type for logging"""
        mapping = {
            "unlock": TriggerType.KEYPAD,
            "lock": TriggerType.MOBILE_APP,
            "arm": TriggerType.MOBILE_APP,
            "disarm": TriggerType.MOBILE_APP,
            "guest_access": TriggerType.KEYPAD
        }
        return mapping.get(event_type, TriggerType.SYSTEM)
    
    def _calculate_realistic_delay(self, activity_level: str) -> float:
        """Calculate realistic delay between events"""
        base_delays = {
            "high": (0.5, 2.0),
            "medium": (1.0, 4.0),
            "low": (2.0, 8.0)
        }
        
        min_delay, max_delay = base_delays[activity_level]
        return random.uniform(min_delay, max_delay)
    
    def _apply_environmental_effects(self):
        """Apply environmental factors to the system"""
        # Weather effects on connectivity
        if self.environmental_factors["current_weather"] == "stormy":
            if random.random() < 0.1:  # 10% chance during storms
                self.fsm.connectivity_status = False
        else:
            self.fsm.connectivity_status = True
        
        # Random network issues
        if random.random() < (1 - self.environmental_factors["network_stability"]):
            self.fsm.connectivity_status = False
        
        # Battery drain simulation
        drain_rate = self.environmental_factors["battery_drain_rate"]
        if self.environmental_factors["current_weather"] == "cold":
            drain_rate *= 1.5  # Cold weather increases battery drain
        
        self.fsm.battery_level -= drain_rate / 60  # Per minute drain
        
        # Temperature variation
        temp_change = random.uniform(-0.1, 0.1)
        self.fsm.temperature += temp_change
        
        # Sensor reliability
        if random.random() < (1 - self.environmental_factors["sensor_reliability"]):
            # Simulate sensor glitch
            sensor_name = random.choice(list(self.fsm.sensors.keys()))
            self.fsm.sensors[sensor_name] = not self.fsm.sensors[sensor_name]
    
    def simulate_security_incidents(self):
        """Simulate various security incidents"""
        print("\n***  Simulating Security Incidents")
        print("-" * 40)
        
        incidents = [
            {
                "type": "failed_attempts",
                "description": "Multiple failed keypad attempts",
                "actions": [
                    (TriggerType.KEYPAD, {"code": "1111"}),
                    (TriggerType.KEYPAD, {"code": "2222"}),
                    (TriggerType.KEYPAD, {"code": "3333"}),
                ]
            },
            {
                "type": "tampering",
                "description": "Physical tampering detected",
                "actions": [
                    (TriggerType.SENSOR, {"sensor": "tamper_sensor", "value": True}),
                ]
            },
            {
                "type": "intrusion_while_armed",
                "description": "Motion detected while system armed",
                "actions": [
                    (TriggerType.MOBILE_APP, {"command": "arm", "user_id": "admin"}),
                    (TriggerType.SENSOR, {"sensor": "motion_sensor", "value": True}),
                ]
            }
        ]
        
        for incident in incidents:
            print(f"\n***   Incident: {incident['description']}")
            
            for trigger_type, trigger_data in incident["actions"]:
                success, message = self.fsm.process_trigger(trigger_type, trigger_data)
                
                self.log_enhanced_action(
                    action=f"{self.fsm.previous_state.value if self.fsm.previous_state else 'UNKNOWN'} → {self.fsm.current_state.value}",
                    reason=f"Security incident: {incident['type']}",
                    trigger_type=trigger_type,
                    user_id=trigger_data.get("user_id", "unknown"),
                    success=success
                )
                
                status = "[OK]" if success else "*** "
                print(f"   {status} {message}")
                print(f"   State: {self.fsm.current_state.value}")
                
                time.sleep(random.uniform(0.5, 2.0))
    
    def simulate_system_maintenance(self):
        """Simulate system maintenance scenarios"""
        print("\n***  Simulating System Maintenance")
        print("-" * 40)
        
        maintenance_events = [
            ("low_battery", "Battery level critically low"),
            ("maintenance", "Scheduled maintenance mode"),
            ("connectivity_lost", "Network connection issues"),
            ("battery_replaced", "Battery replacement completed"),
            ("exit_maintenance", "Maintenance completed"),
        ]
        
        for event, description in maintenance_events:
            print(f"\n***  {description}")
            
            success, message = self.fsm.process_trigger(TriggerType.SYSTEM, {"event": event})
            
            self.log_enhanced_action(
                action=f"{self.fsm.previous_state.value if self.fsm.previous_state else 'UNKNOWN'} → {self.fsm.current_state.value}",
                reason=description,
                trigger_type=TriggerType.SYSTEM,
                success=success
            )
            
            status = "[OK]" if success else "*** "
            print(f"   {status} {message}")
            print(f"   State: {self.fsm.current_state.value}")
            
            time.sleep(random.uniform(1, 3))
    
    def run_comprehensive_simulation(self):
        """Run a comprehensive simulation with all scenarios"""
        print("***  Starting Comprehensive Smart Door Lock Simulation")
        print("=" * 60)
        print(f"Start time: {self.simulation_start_time}")
        print(f"Initial state: {self.fsm.current_state.value}")
        print(f"Battery level: {self.fsm.battery_level}%")
        
        try:
            # Simulate different day patterns
            self.simulate_realistic_day("weekday")
            time.sleep(2)
            
            self.simulate_realistic_day("weekend")
            time.sleep(2)
            
            # Simulate security incidents
            self.simulate_security_incidents()
            time.sleep(2)
            
            # Simulate maintenance
            self.simulate_system_maintenance()
            
            # Final status
            print(f"\n***  Simulation Summary")
            print("-" * 30)
            print(f"Total events: {self.total_events}")
            print(f"Duration: {datetime.now() - self.simulation_start_time}")
            print(f"Final state: {self.fsm.current_state.value}")
            
            system_status = self.fsm.get_system_status()
            print(f"Battery level: {system_status['battery_level']}%")
            print(f"Failed attempts: {system_status['failed_attempts']}")
            print(f"Temperature: {system_status['temperature']}°C")
            
            print(f"\n[OK] Comprehensive simulation completed!")
            print(f"📝 Detailed logs saved to: {self.log_file}")
            
        except KeyboardInterrupt:
            print(f"\n⏹️  Simulation interrupted by user")
            print(f"Events completed: {self.total_events}")
        except Exception as e:
            print(f"\n***  Simulation error: {e}")

# Legacy function for backward compatibility
def run_simulation():
    """Legacy simulation function"""
    print("***  Smart Door Lock Simulation Started (Legacy Mode)")
    print("-" * 40)
    
    # Use basic scenarios for legacy compatibility
    for i, scenario in enumerate(scenarios[:5]):  # First 5 scenarios
        print(f"\n[INPUT] {scenario['event']} => {scenario['reason']}")
        time.sleep(1)
    
    print("\n[OK] Legacy simulation finished.")

if __name__ == "__main__":
    # Run enhanced simulation by default
    simulator = EnhancedDoorLockSimulator()
    simulator.run_comprehensive_simulation()
