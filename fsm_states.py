"""
Smart Door Lock Finite State Machine
Enhanced with realistic states, sensors, and security features
"""

import time
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import json

class LockState(Enum):
    """Enhanced lock states for realistic smart door lock"""
    UNLOCKED = "UNLOCKED"
    LOCKED = "LOCKED"
    ARMED = "ARMED"
    DISARMED = "DISARMED"
    TAMPERED = "TAMPERED"
    MAINTENANCE = "MAINTENANCE"
    LOW_BATTERY = "LOW_BATTERY"
    OFFLINE = "OFFLINE"
    EMERGENCY_UNLOCK = "EMERGENCY_UNLOCK"
    LOCKOUT = "LOCKOUT"
    GUEST_ACCESS = "GUEST_ACCESS"
    ADMIN_OVERRIDE = "ADMIN_OVERRIDE"

class TriggerType(Enum):
    """Types of triggers that can cause state changes"""
    KEYPAD = "keypad"
    BIOMETRIC = "biometric"
    PROXIMITY = "proximity"
    MOBILE_APP = "mobile_app"
    PHYSICAL_KEY = "physical_key"
    VOICE_COMMAND = "voice_command"
    SCHEDULE = "schedule"
    GEOFENCE = "geofence"
    EMERGENCY = "emergency"
    ADMIN = "admin"
    SYSTEM = "system"
    SENSOR = "sensor"

class SecurityLevel(Enum):
    """Security access levels"""
    GUEST = 1
    USER = 2
    ADMIN = 3
    EMERGENCY = 4

class SmartDoorLockFSM:
    """Enhanced Smart Door Lock Finite State Machine"""
    
    def __init__(self):
        self.current_state = LockState.DISARMED
        self.previous_state = None
        self.state_history = []
        
        # System status
        self.battery_level = 85.0
        self.temperature = 22.5
        self.connectivity_status = True
        self.last_maintenance = datetime.now() - timedelta(days=30)
        
        # Security features
        self.failed_attempts = 0
        self.max_failed_attempts = 3
        self.lockout_duration = timedelta(minutes=15)
        self.lockout_start_time = None
        self.intrusion_detected = False
        
        # User management
        self.authorized_users = {
            "admin": {"level": SecurityLevel.ADMIN, "code": "1234", "biometric": "admin_print"},
            "user1": {"level": SecurityLevel.USER, "code": "5678", "biometric": "user1_print"},
            "guest": {"level": SecurityLevel.GUEST, "code": "0000", "biometric": None, "expires": datetime.now() + timedelta(hours=24)}
        }
        
        # Sensors and environmental data
        self.sensors = {
            "door_sensor": True,  # True = closed, False = open
            "motion_sensor": False,
            "proximity_sensor": False,
            "tamper_sensor": False,
            "sound_sensor": 0.0,  # dB level
            "light_sensor": 50.0,  # lux
        }
        
        # Scheduling
        self.auto_lock_delay = timedelta(seconds=30)
        self.last_unlock_time = None
        self.scheduled_locks = []
        
        # Define state transition matrix
        self.transitions = self._build_transition_matrix()
        
        # Initialize state
        self._log_state_change(None, self.current_state, "System initialization")
    
    def _build_transition_matrix(self) -> Dict[Tuple[LockState, str], Tuple[LockState, str]]:
        """Build comprehensive state transition matrix"""
        return {
            # Normal operations
            (LockState.DISARMED, "lock"): (LockState.LOCKED, "Manual lock"),
            (LockState.DISARMED, "unlock"): (LockState.UNLOCKED, "Manual unlock"),
            (LockState.DISARMED, "arm"): (LockState.ARMED, "System armed"),
            (LockState.LOCKED, "unlock"): (LockState.UNLOCKED, "Manual unlock"),
            (LockState.UNLOCKED, "lock"): (LockState.LOCKED, "Manual lock"),
            (LockState.UNLOCKED, "auto_lock"): (LockState.LOCKED, "Auto-lock timeout"),
            (LockState.ARMED, "disarm"): (LockState.DISARMED, "System disarmed"),
            (LockState.ARMED, "intrusion"): (LockState.TAMPERED, "Intrusion detected"),
            
            # Security events
            (LockState.LOCKED, "tamper"): (LockState.TAMPERED, "Tampering detected"),
            (LockState.UNLOCKED, "tamper"): (LockState.TAMPERED, "Tampering detected"),
            (LockState.TAMPERED, "reset"): (LockState.LOCKED, "Security reset"),
            (LockState.LOCKOUT, "timeout"): (LockState.LOCKED, "Lockout period expired"),
            
            # Maintenance and system states
            (LockState.LOCKED, "maintenance"): (LockState.MAINTENANCE, "Maintenance mode"),
            (LockState.UNLOCKED, "maintenance"): (LockState.MAINTENANCE, "Maintenance mode"),
            (LockState.MAINTENANCE, "exit_maintenance"): (LockState.LOCKED, "Maintenance complete"),
            (LockState.LOCKED, "low_battery"): (LockState.LOW_BATTERY, "Battery low"),
            (LockState.LOW_BATTERY, "battery_replaced"): (LockState.LOCKED, "Battery replaced"),
            
            # Emergency and admin overrides
            (LockState.LOCKED, "emergency"): (LockState.EMERGENCY_UNLOCK, "Emergency unlock"),
            (LockState.TAMPERED, "admin_override"): (LockState.ADMIN_OVERRIDE, "Admin override"),
            (LockState.LOCKOUT, "admin_override"): (LockState.ADMIN_OVERRIDE, "Admin override"),
            (LockState.ADMIN_OVERRIDE, "restore"): (LockState.LOCKED, "Normal operation restored"),
            
            # Guest access
            (LockState.LOCKED, "guest_unlock"): (LockState.GUEST_ACCESS, "Guest access granted"),
            (LockState.GUEST_ACCESS, "guest_timeout"): (LockState.LOCKED, "Guest access expired"),
            
            # Connectivity
            (LockState.LOCKED, "offline"): (LockState.OFFLINE, "Connection lost"),
            (LockState.OFFLINE, "online"): (LockState.LOCKED, "Connection restored"),
        }
    
    def process_trigger(self, trigger_type: TriggerType, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Process various trigger types and determine state changes"""
        
        # Check if system is in lockout
        if self._is_in_lockout():
            return False, "System is in lockout mode"
        
        # Update sensors based on trigger
        self._update_sensors(trigger_type, data)
        
        # Process different trigger types
        if trigger_type == TriggerType.KEYPAD:
            return self._process_keypad_input(data.get("code", ""))
        
        elif trigger_type == TriggerType.BIOMETRIC:
            return self._process_biometric_input(data.get("biometric_data", ""))
        
        elif trigger_type == TriggerType.PROXIMITY:
            return self._process_proximity_trigger(data.get("user_id", ""))
        
        elif trigger_type == TriggerType.MOBILE_APP:
            return self._process_mobile_app_command(data.get("command", ""), data.get("user_id", ""))
        
        elif trigger_type == TriggerType.PHYSICAL_KEY:
            return self._process_physical_key()
        
        elif trigger_type == TriggerType.SCHEDULE:
            return self._process_scheduled_event(data.get("event", ""))
        
        elif trigger_type == TriggerType.EMERGENCY:
            return self._process_emergency_trigger(data.get("emergency_type", ""))
        
        elif trigger_type == TriggerType.SYSTEM:
            return self._process_system_event(data.get("event", ""))
        
        elif trigger_type == TriggerType.SENSOR:
            return self._process_sensor_event(data.get("sensor", ""), data.get("value", None))
        
        return False, "Unknown trigger type"
    
    def _process_keypad_input(self, code: str) -> Tuple[bool, str]:
        """Process keypad code input"""
        user = self._authenticate_code(code)
        if user:
            if self.current_state == LockState.LOCKED:
                success = self._transition_to("unlock", f"Keypad unlock by {user}")
                if success:
                    self.failed_attempts = 0
                    return True, f"Unlocked by {user}"
                else:
                    return False, "Unlock failed"
            elif self.current_state == LockState.UNLOCKED:
                success = self._transition_to("lock", f"Keypad lock by {user}")
                return success, f"Locked by {user}" if success else "Lock failed"
            elif self.current_state == LockState.DISARMED:
                success = self._transition_to("unlock", f"Keypad unlock by {user}")
                if success:
                    self.failed_attempts = 0
                    return True, f"Unlocked by {user}"
                else:
                    return False, "Unlock failed"
            else:
                return False, f"Cannot process keypad input in current state: {self.current_state.value}"
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= self.max_failed_attempts:
                self._transition_to("lockout", "Too many failed attempts")
                self.lockout_start_time = datetime.now()
                return False, "System locked due to failed attempts"
            return False, f"Invalid code. {self.max_failed_attempts - self.failed_attempts} attempts remaining"
    
    def _process_biometric_input(self, biometric_data: str) -> Tuple[bool, str]:
        """Process biometric authentication"""
        user = self._authenticate_biometric(biometric_data)
        if user:
            if self.current_state == LockState.LOCKED:
                success = self._transition_to("unlock", f"Biometric unlock by {user}")
                return success, f"Biometric unlock by {user}" if success else "Unlock failed"
            elif self.current_state == LockState.UNLOCKED:
                success = self._transition_to("lock", f"Biometric lock by {user}")
                return success, f"Biometric lock by {user}" if success else "Lock failed"
        else:
            self.failed_attempts += 1
            return False, "Biometric authentication failed"
    
    def _process_proximity_trigger(self, user_id: str) -> Tuple[bool, str]:
        """Process proximity-based unlock"""
        if user_id in self.authorized_users:
            user_data = self.authorized_users[user_id]
            if user_data["level"].value >= SecurityLevel.USER.value:
                if self.current_state == LockState.LOCKED:
                    success = self._transition_to("unlock", f"Proximity unlock by {user_id}")
                    return success, f"Proximity unlock by {user_id}" if success else "Unlock failed"
        return False, "Unauthorized proximity access"
    
    def _process_mobile_app_command(self, command: str, user_id: str) -> Tuple[bool, str]:
        """Process mobile app commands"""
        if user_id not in self.authorized_users:
            return False, "Unauthorized user"
        
        user_data = self.authorized_users[user_id]
        
        if command == "unlock" and self.current_state == LockState.LOCKED:
            success = self._transition_to("unlock", f"Mobile app unlock by {user_id}")
            return success, f"Mobile unlock by {user_id}" if success else "Unlock failed"
        
        elif command == "lock" and self.current_state == LockState.UNLOCKED:
            success = self._transition_to("lock", f"Mobile app lock by {user_id}")
            return success, f"Mobile lock by {user_id}" if success else "Lock failed"
        
        elif command == "arm" and user_data["level"].value >= SecurityLevel.USER.value:
            success = self._transition_to("arm", f"System armed by {user_id}")
            return success, f"System armed by {user_id}" if success else "Arm failed"
        
        elif command == "disarm" and user_data["level"].value >= SecurityLevel.USER.value:
            success = self._transition_to("disarm", f"System disarmed by {user_id}")
            return success, f"System disarmed by {user_id}" if success else "Disarm failed"
        
        return False, f"Invalid command or insufficient permissions: {command}"
    
    def _process_physical_key(self) -> Tuple[bool, str]:
        """Process physical key usage"""
        if self.current_state == LockState.LOCKED:
            success = self._transition_to("unlock", "Physical key unlock")
            return success, "Physical key unlock" if success else "Unlock failed"
        elif self.current_state == LockState.UNLOCKED:
            success = self._transition_to("lock", "Physical key lock")
            return success, "Physical key lock" if success else "Lock failed"
        return False, "Physical key not applicable in current state"
    
    def _process_emergency_trigger(self, emergency_type: str) -> Tuple[bool, str]:
        """Process emergency situations"""
        if emergency_type == "fire_alarm":
            success = self._transition_to("emergency", "Fire alarm emergency unlock")
            return success, "Emergency unlock due to fire alarm" if success else "Emergency unlock failed"
        elif emergency_type == "medical":
            success = self._transition_to("emergency", "Medical emergency unlock")
            return success, "Emergency unlock for medical emergency" if success else "Emergency unlock failed"
        elif emergency_type == "power_failure":
            success = self._transition_to("emergency", "Power failure emergency unlock")
            return success, "Emergency unlock due to power failure" if success else "Emergency unlock failed"
        return False, f"Unknown emergency type: {emergency_type}"
    
    def _process_system_event(self, event: str) -> Tuple[bool, str]:
        """Process system-level events"""
        if event == "auto_lock" and self.current_state == LockState.UNLOCKED:
            if self.last_unlock_time and datetime.now() - self.last_unlock_time >= self.auto_lock_delay:
                success = self._transition_to("auto_lock", "Auto-lock timeout")
                return success, "Auto-lock engaged" if success else "Auto-lock failed"
        
        elif event == "low_battery" and self.battery_level < 20:
            success = self._transition_to("low_battery", f"Battery level: {self.battery_level}%")
            return success, "Low battery warning" if success else "Battery warning failed"
        
        elif event == "maintenance_mode":
            success = self._transition_to("maintenance", "Scheduled maintenance")
            return success, "Maintenance mode activated" if success else "Maintenance mode failed"
        
        elif event == "connectivity_lost":
            success = self._transition_to("offline", "Network connection lost")
            return success, "System offline" if success else "Offline transition failed"
        
        return False, f"Unknown system event: {event}"
    
    def _process_sensor_event(self, sensor: str, value: Any) -> Tuple[bool, str]:
        """Process sensor-based events"""
        if sensor == "tamper_sensor" and value:
            success = self._transition_to("tamper", "Tampering detected by sensor")
            return success, "Tamper alert activated" if success else "Tamper alert failed"
        
        elif sensor == "motion_sensor" and value and self.current_state == LockState.ARMED:
            success = self._transition_to("intrusion", "Motion detected while armed")
            return success, "Intrusion detected" if success else "Intrusion detection failed"
        
        elif sensor == "door_sensor" and not value:  # Door opened
            if self.current_state == LockState.LOCKED:
                success = self._transition_to("tamper", "Door opened while locked")
                return success, "Unauthorized door opening" if success else "Door sensor alert failed"
        
        return False, f"No action for sensor {sensor} with value {value}"
    
    def _transition_to(self, event: str, reason: str = "") -> bool:
        """Attempt state transition"""
        transition_key = (self.current_state, event)
        
        if transition_key in self.transitions:
            new_state, default_reason = self.transitions[transition_key]
            actual_reason = reason if reason else default_reason
            
            self._log_state_change(self.current_state, new_state, actual_reason)
            self.previous_state = self.current_state
            self.current_state = new_state
            
            # Handle special state entry actions
            self._handle_state_entry(new_state)
            
            return True
        
        return False
    
    def _handle_state_entry(self, state: LockState):
        """Handle actions when entering specific states"""
        if state == LockState.UNLOCKED:
            self.last_unlock_time = datetime.now()
        
        elif state == LockState.LOCKOUT:
            self.lockout_start_time = datetime.now()
        
        elif state == LockState.TAMPERED:
            self.intrusion_detected = True
            # In real system, would trigger alarms, notifications, etc.
        
        elif state == LockState.LOW_BATTERY:
            # In real system, would send low battery notifications
            pass
        
        elif state == LockState.EMERGENCY_UNLOCK:
            # In real system, would log emergency event, notify authorities
            pass
    
    def _authenticate_code(self, code: str) -> Optional[str]:
        """Authenticate keypad code"""
        for user_id, user_data in self.authorized_users.items():
            if user_data["code"] == code:
                # Check if guest access has expired
                if "expires" in user_data and datetime.now() > user_data["expires"]:
                    return None
                return user_id
        return None
    
    def _authenticate_biometric(self, biometric_data: str) -> Optional[str]:
        """Authenticate biometric data"""
        for user_id, user_data in self.authorized_users.items():
            if user_data.get("biometric") == biometric_data:
                return user_id
        return None
    
    def _is_in_lockout(self) -> bool:
        """Check if system is currently in lockout"""
        if self.current_state == LockState.LOCKOUT:
            if self.lockout_start_time and datetime.now() - self.lockout_start_time >= self.lockout_duration:
                # Lockout period expired
                self._transition_to("timeout", "Lockout period expired")
                return False
            return True
        return False
    
    def _update_sensors(self, trigger_type: TriggerType, data: Dict[str, Any]):
        """Update sensor readings based on triggers"""
        if trigger_type == TriggerType.PROXIMITY:
            self.sensors["proximity_sensor"] = True
        elif trigger_type == TriggerType.PHYSICAL_KEY:
            self.sensors["door_sensor"] = not self.sensors["door_sensor"]
        
        # Simulate environmental changes
        self.battery_level -= random.uniform(0.01, 0.05)  # Battery drain
        self.temperature += random.uniform(-0.5, 0.5)  # Temperature variation
        
        # Random sensor updates
        if random.random() < 0.1:  # 10% chance
            self.sensors["motion_sensor"] = random.choice([True, False])
            self.sensors["sound_sensor"] = random.uniform(20, 80)
            self.sensors["light_sensor"] = random.uniform(0, 100)
    
    def _log_state_change(self, from_state: Optional[LockState], to_state: LockState, reason: str):
        """Log state changes"""
        timestamp = datetime.now()
        log_entry = {
            "timestamp": timestamp.isoformat(),
            "from_state": from_state.value if from_state else None,
            "to_state": to_state.value,
            "reason": reason,
            "battery_level": self.battery_level,
            "temperature": self.temperature,
            "sensors": self.sensors.copy()
        }
        
        self.state_history.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.state_history) > 1000:
            self.state_history = self.state_history[-1000:]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        return {
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "battery_level": round(self.battery_level, 1),
            "temperature": round(self.temperature, 1),
            "connectivity": self.connectivity_status,
            "failed_attempts": self.failed_attempts,
            "is_locked_out": self._is_in_lockout(),
            "sensors": self.sensors.copy(),
            "authorized_users": len(self.authorized_users),
            "last_maintenance": self.last_maintenance.isoformat(),
            "intrusion_detected": self.intrusion_detected
        }
    
    def add_user(self, user_id: str, level: SecurityLevel, code: str, biometric: Optional[str] = None, expires: Optional[datetime] = None):
        """Add a new authorized user"""
        user_data = {
            "level": level,
            "code": code,
            "biometric": biometric
        }
        if expires:
            user_data["expires"] = expires
        
        self.authorized_users[user_id] = user_data
    
    def remove_user(self, user_id: str) -> bool:
        """Remove an authorized user"""
        if user_id in self.authorized_users and user_id != "admin":
            del self.authorized_users[user_id]
            return True
        return False
    
    def reset_security(self, admin_code: str) -> bool:
        """Reset security state (admin only)"""
        if self._authenticate_code(admin_code) == "admin":
            self.failed_attempts = 0
            self.lockout_start_time = None
            self.intrusion_detected = False
            if self.current_state in [LockState.LOCKOUT, LockState.TAMPERED]:
                self._transition_to("reset", "Admin security reset")
            return True
        return False

# Global instances for backward compatibility
fsm_instance = SmartDoorLockFSM()
current_state = fsm_instance.current_state.value

# Legacy FSM dictionary for backward compatibility
fsm = {
    ("LOCKED", "unlock"): "UNLOCKED",
    ("UNLOCKED", "lock"): "LOCKED",
    ("DISARMED", "arm"): "ARMED",
    ("ARMED", "disarm"): "DISARMED",
    ("LOCKED", "tamper"): "TAMPERED",
    ("UNLOCKED", "tamper"): "TAMPERED",
    ("TAMPERED", "reset"): "LOCKED",
}

# Convenience class for backward compatibility
class CarDoorLockFSM:
    """Legacy compatibility class"""
    def __init__(self):
        self.state = "UNLOCKED"
        self.fsm = fsm
        self.current_state = "UNLOCKED"
    
    def update(self, key, brake, gear):
        """Legacy update method"""
        # Simple logic for backward compatibility
        if key and brake and gear in ("D", "R"):
            self.state = "LOCKED"
            self.current_state = "LOCKED"
        else:
            self.state = "UNLOCKED" 
            self.current_state = "UNLOCKED"
        return self.state
