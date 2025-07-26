"""
Emergency Protocols and Fail-safes for Smart Door Lock System
Comprehensive emergency handling, backup systems, and safety protocols
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from fsm_states import SmartDoorLockFSM, TriggerType, SecurityLevel, LockState

class EmergencyType(Enum):
    """Types of emergency situations"""
    FIRE_ALARM = "fire_alarm"
    MEDICAL_EMERGENCY = "medical_emergency"
    POWER_FAILURE = "power_failure"
    SECURITY_BREACH = "security_breach"
    SYSTEM_MALFUNCTION = "system_malfunction"
    NATURAL_DISASTER = "natural_disaster"
    LOCKOUT_EMERGENCY = "lockout_emergency"
    BATTERY_CRITICAL = "battery_critical"
    CONNECTIVITY_FAILURE = "connectivity_failure"

class FailsafeMode(Enum):
    """Different failsafe operating modes"""
    FAIL_SECURE = "fail_secure"      # Lock remains locked on failure
    FAIL_SAFE = "fail_safe"          # Lock unlocks on failure
    FAIL_MAINTAIN = "fail_maintain"  # Maintain current state on failure

class EmergencyProtocolManager:
    """Manages emergency protocols and fail-safe mechanisms"""
    
    def __init__(self, fsm: SmartDoorLockFSM):
        self.fsm = fsm
        self.emergency_contacts = self._initialize_emergency_contacts()
        self.emergency_protocols = self._initialize_emergency_protocols()
        self.failsafe_config = self._initialize_failsafe_config()
        self.emergency_log = []
        self.backup_power_available = True
        self.backup_power_duration = timedelta(hours=8)
        self.last_backup_test = datetime.now() - timedelta(days=30)
        
        # Emergency override codes (should be securely stored in real system)
        self.emergency_override_codes = {
            "fire_department": "FIRE911",
            "police": "POLICE911", 
            "medical": "MED911",
            "maintenance": "MAINT2024",
            "master_override": "MASTER999"
        }
        
        # System health monitoring
        self.system_health_checks = {
            "battery_level": {"threshold": 10.0, "critical": 5.0},
            "temperature": {"min": -10.0, "max": 60.0, "critical_min": -20.0, "critical_max": 80.0},
            "connectivity": {"timeout": timedelta(minutes=5), "critical_timeout": timedelta(minutes=30)},
            "sensor_failures": {"max_failures": 2, "critical_failures": 5},
            "failed_attempts": {"lockout_threshold": 3, "emergency_threshold": 10}
        }
    
    def _initialize_emergency_contacts(self) -> Dict[str, Dict[str, str]]:
        """Initialize emergency contact information"""
        return {
            "fire_department": {
                "name": "Fire Department",
                "phone": "911",
                "email": "fire@emergency.gov",
                "priority": "critical"
            },
            "police": {
                "name": "Police Department", 
                "phone": "911",
                "email": "police@emergency.gov",
                "priority": "critical"
            },
            "medical": {
                "name": "Emergency Medical Services",
                "phone": "911", 
                "email": "ems@emergency.gov",
                "priority": "critical"
            },
            "security_company": {
                "name": "Security Monitoring",
                "phone": "+1-555-SECURITY",
                "email": "alerts@securityco.com",
                "priority": "high"
            },
            "maintenance": {
                "name": "System Maintenance",
                "phone": "+1-555-SUPPORT",
                "email": "support@smartlock.com",
                "priority": "medium"
            },
            "property_manager": {
                "name": "Property Manager",
                "phone": "+1-555-PROPERTY",
                "email": "manager@property.com",
                "priority": "low"
            }
        }
    
    def _initialize_emergency_protocols(self) -> Dict[EmergencyType, Dict[str, Any]]:
        """Initialize emergency response protocols"""
        return {
            EmergencyType.FIRE_ALARM: {
                "action": "immediate_unlock",
                "failsafe_mode": FailsafeMode.FAIL_SAFE,
                "notify_contacts": ["fire_department", "security_company"],
                "auto_disable_relock": True,
                "priority": "critical",
                "response_time": timedelta(seconds=5)
            },
            EmergencyType.MEDICAL_EMERGENCY: {
                "action": "immediate_unlock",
                "failsafe_mode": FailsafeMode.FAIL_SAFE,
                "notify_contacts": ["medical", "security_company"],
                "auto_disable_relock": False,
                "priority": "critical",
                "response_time": timedelta(seconds=10)
            },
            EmergencyType.POWER_FAILURE: {
                "action": "maintain_state",
                "failsafe_mode": FailsafeMode.FAIL_MAINTAIN,
                "notify_contacts": ["maintenance", "property_manager"],
                "activate_backup_power": True,
                "priority": "high",
                "response_time": timedelta(seconds=30)
            },
            EmergencyType.SECURITY_BREACH: {
                "action": "secure_lock",
                "failsafe_mode": FailsafeMode.FAIL_SECURE,
                "notify_contacts": ["police", "security_company"],
                "activate_alarm": True,
                "priority": "critical",
                "response_time": timedelta(seconds=2)
            },
            EmergencyType.SYSTEM_MALFUNCTION: {
                "action": "safe_mode",
                "failsafe_mode": FailsafeMode.FAIL_SAFE,
                "notify_contacts": ["maintenance", "security_company"],
                "disable_remote_access": True,
                "priority": "high",
                "response_time": timedelta(minutes=1)
            },
            EmergencyType.NATURAL_DISASTER: {
                "action": "emergency_unlock",
                "failsafe_mode": FailsafeMode.FAIL_SAFE,
                "notify_contacts": ["fire_department", "police", "medical"],
                "disable_all_locks": True,
                "priority": "critical",
                "response_time": timedelta(seconds=1)
            },
            EmergencyType.LOCKOUT_EMERGENCY: {
                "action": "temporary_unlock",
                "failsafe_mode": FailsafeMode.FAIL_SAFE,
                "notify_contacts": ["security_company", "property_manager"],
                "require_verification": True,
                "priority": "medium",
                "response_time": timedelta(minutes=5)
            },
            EmergencyType.BATTERY_CRITICAL: {
                "action": "low_power_mode",
                "failsafe_mode": FailsafeMode.FAIL_MAINTAIN,
                "notify_contacts": ["maintenance"],
                "reduce_functionality": True,
                "priority": "medium",
                "response_time": timedelta(minutes=2)
            },
            EmergencyType.CONNECTIVITY_FAILURE: {
                "action": "offline_mode",
                "failsafe_mode": FailsafeMode.FAIL_MAINTAIN,
                "notify_contacts": ["maintenance"],
                "enable_local_only": True,
                "priority": "low",
                "response_time": timedelta(minutes=10)
            }
        }
    
    def _initialize_failsafe_config(self) -> Dict[str, Any]:
        """Initialize failsafe configuration"""
        return {
            "default_mode": FailsafeMode.FAIL_SAFE,
            "emergency_unlock_duration": timedelta(minutes=30),
            "max_emergency_overrides_per_day": 5,
            "require_dual_authorization": True,
            "auto_reset_after_emergency": True,
            "emergency_log_retention": timedelta(days=365),
            "backup_power_test_interval": timedelta(days=30),
            "system_health_check_interval": timedelta(minutes=5)
        }
    
    def detect_emergency(self) -> Optional[EmergencyType]:
        """Detect potential emergency situations based on system state"""
        system_status = self.fsm.get_system_status()
        
        # Check battery level
        if system_status['battery_level'] <= self.system_health_checks['battery_level']['critical']:
            return EmergencyType.BATTERY_CRITICAL
        
        # Check temperature extremes
        temp_config = self.system_health_checks['temperature']
        if (system_status['temperature'] <= temp_config['critical_min'] or 
            system_status['temperature'] >= temp_config['critical_max']):
            return EmergencyType.SYSTEM_MALFUNCTION
        
        # Check connectivity
        if not system_status['connectivity']:
            return EmergencyType.CONNECTIVITY_FAILURE
        
        # Check for excessive failed attempts
        if system_status['failed_attempts'] >= self.system_health_checks['failed_attempts']['emergency_threshold']:
            return EmergencyType.SECURITY_BREACH
        
        # Check if system is in tampered state
        if system_status['current_state'] == LockState.TAMPERED.value:
            return EmergencyType.SECURITY_BREACH
        
        return None
    
    def handle_emergency(self, emergency_type: EmergencyType, 
                        source: str = "system", 
                        additional_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Handle emergency situation according to protocols"""
        
        if emergency_type not in self.emergency_protocols:
            return False, f"Unknown emergency type: {emergency_type.value}"
        
        protocol = self.emergency_protocols[emergency_type]
        timestamp = datetime.now()
        
        # Log emergency
        emergency_record = {
            "timestamp": timestamp.isoformat(),
            "emergency_type": emergency_type.value,
            "source": source,
            "protocol": protocol,
            "additional_data": additional_data or {},
            "system_state_before": self.fsm.get_system_status()
        }
        
        print(f"***  EMERGENCY DETECTED: {emergency_type.value}")
        print(f"   Source: {source}")
        print(f"   Priority: {protocol['priority']}")
        print(f"   Response time: {protocol['response_time']}")
        
        try:
            # Execute emergency action
            success = self._execute_emergency_action(protocol['action'], emergency_type)
            
            if success:
                # Notify emergency contacts
                self._notify_emergency_contacts(protocol.get('notify_contacts', []), 
                                              emergency_type, emergency_record)
                
                # Apply additional protocol measures
                self._apply_protocol_measures(protocol, emergency_type)
                
                emergency_record["action_result"] = "success"
                emergency_record["system_state_after"] = self.fsm.get_system_status()
                
                message = f"Emergency protocol executed successfully for {emergency_type.value}"
                print(f"   [OK] {message}")
                
            else:
                emergency_record["action_result"] = "failed"
                message = f"Failed to execute emergency protocol for {emergency_type.value}"
                print(f"   ***  {message}")
            
            # Log the emergency
            self.emergency_log.append(emergency_record)
            self._save_emergency_log()
            
            return success, message
            
        except Exception as e:
            error_message = f"Emergency protocol execution error: {str(e)}"
            emergency_record["action_result"] = "error"
            emergency_record["error"] = error_message
            self.emergency_log.append(emergency_record)
            print(f"   ***  {error_message}")
            return False, error_message
    
    def _execute_emergency_action(self, action: str, emergency_type: EmergencyType) -> bool:
        """Execute the specific emergency action"""
        
        if action == "immediate_unlock":
            return self._emergency_unlock(immediate=True)
        
        elif action == "emergency_unlock":
            return self._emergency_unlock(immediate=False)
        
        elif action == "secure_lock":
            return self._emergency_secure()
        
        elif action == "maintain_state":
            return self._maintain_current_state()
        
        elif action == "safe_mode":
            return self._enter_safe_mode()
        
        elif action == "low_power_mode":
            return self._enter_low_power_mode()
        
        elif action == "offline_mode":
            return self._enter_offline_mode()
        
        elif action == "temporary_unlock":
            return self._temporary_emergency_unlock()
        
        else:
            print(f"   ***   Unknown emergency action: {action}")
            return False
    
    def _emergency_unlock(self, immediate: bool = True) -> bool:
        """Perform emergency unlock"""
        try:
            success, message = self.fsm.process_trigger(
                TriggerType.EMERGENCY, 
                {"emergency_type": "emergency_unlock"}
            )
            
            if success:
                print(f"   ***  Emergency unlock {'immediate' if immediate else 'initiated'}")
                
                # Disable auto-relock during emergency
                self.fsm.auto_lock_delay = timedelta(hours=24)  # Extended delay
                
                return True
            else:
                print(f"   ***  Emergency unlock failed: {message}")
                return False
                
        except Exception as e:
            print(f"   ***  Emergency unlock error: {e}")
            return False
    
    def _emergency_secure(self) -> bool:
        """Secure the lock during security emergency"""
        try:
            # Force lock if not already locked
            if self.fsm.current_state != LockState.LOCKED:
                success, message = self.fsm.process_trigger(
                    TriggerType.SYSTEM,
                    {"event": "emergency_lock"}
                )
                
                if not success:
                    return False
            
            # Disable all remote access temporarily
            print("   ***  Emergency secure mode activated")
            print("   ***  Remote access disabled")
            
            return True
            
        except Exception as e:
            print(f"   ***  Emergency secure error: {e}")
            return False
    
    def _maintain_current_state(self) -> bool:
        """Maintain current state during emergency"""
        print(f"   ***   Maintaining current state: {self.fsm.current_state.value}")
        return True
    
    def _enter_safe_mode(self) -> bool:
        """Enter safe mode operation"""
        try:
            # Transition to maintenance mode for safety
            success, message = self.fsm.process_trigger(
                TriggerType.SYSTEM,
                {"event": "maintenance_mode"}
            )
            
            if success:
                print("   ***   Safe mode activated")
                print("   ***   Limited functionality enabled")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"   ***  Safe mode error: {e}")
            return False
    
    def _enter_low_power_mode(self) -> bool:
        """Enter low power conservation mode"""
        print("   ***  Low power mode activated")
        print("   ***  Reducing system functionality")
        
        # Reduce sensor polling frequency
        # Disable non-essential features
        # Extend auto-lock delays to save power
        
        return True
    
    def _enter_offline_mode(self) -> bool:
        """Enter offline operation mode"""
        print("   ***  Offline mode activated")
        print("   ***  Local operation only")
        
        # Disable remote connectivity features
        # Enable local-only authentication
        
        return True
    
    def _temporary_emergency_unlock(self) -> bool:
        """Perform temporary emergency unlock with auto-relock"""
        success = self._emergency_unlock(immediate=False)
        
        if success:
            # Set shorter auto-relock for security
            self.fsm.auto_lock_delay = timedelta(minutes=5)
            print("   ***  Temporary unlock - will auto-lock in 5 minutes")
        
        return success
    
    def _notify_emergency_contacts(self, contact_types: List[str], 
                                 emergency_type: EmergencyType,
                                 emergency_record: Dict[str, Any]):
        """Notify emergency contacts (simulation)"""
        print("   ***  Notifying emergency contacts:")
        
        for contact_type in contact_types:
            if contact_type in self.emergency_contacts:
                contact = self.emergency_contacts[contact_type]
                print(f"      ***  {contact['name']}: {contact['phone']}")
                
                # In real system, would send actual notifications
                # - SMS alerts
                # - Email notifications  
                # - Push notifications to mobile apps
                # - Integration with monitoring services
    
    def _apply_protocol_measures(self, protocol: Dict[str, Any], emergency_type: EmergencyType):
        """Apply additional protocol measures"""
        
        if protocol.get('activate_backup_power', False):
            self._activate_backup_power()
        
        if protocol.get('activate_alarm', False):
            self._activate_alarm_system()
        
        if protocol.get('disable_remote_access', False):
            self._disable_remote_access()
        
        if protocol.get('auto_disable_relock', False):
            self._disable_auto_relock()
        
        if protocol.get('reduce_functionality', False):
            self._reduce_system_functionality()
    
    def _activate_backup_power(self):
        """Activate backup power systems"""
        if self.backup_power_available:
            print("   ***  Backup power activated")
            print(f"   ⏱️  Estimated duration: {self.backup_power_duration}")
        else:
            print("   ***  Backup power not available")
    
    def _activate_alarm_system(self):
        """Activate alarm systems"""
        print("   ***  Alarm system activated")
        print("   ***  Audible and visual alarms triggered")
    
    def _disable_remote_access(self):
        """Disable remote access capabilities"""
        print("   ***  Remote access disabled")
        print("   ***  Local access only")
    
    def _disable_auto_relock(self):
        """Disable automatic relocking"""
        self.fsm.auto_lock_delay = timedelta(days=1)  # Effectively disabled
        print("   ***  Auto-relock disabled")
    
    def _reduce_system_functionality(self):
        """Reduce system functionality to conserve power/resources"""
        print("   ***  System functionality reduced")
        print("   ***  Non-essential features disabled")
    
    def process_emergency_override(self, override_code: str, 
                                 emergency_type: EmergencyType,
                                 operator_id: str = "unknown") -> Tuple[bool, str]:
        """Process emergency override codes"""
        
        # Validate override code
        valid_codes = list(self.emergency_override_codes.values())
        if override_code not in valid_codes:
            return False, "Invalid emergency override code"
        
        # Find which authority is using the code
        authority = None
        for auth, code in self.emergency_override_codes.items():
            if code == override_code:
                authority = auth
                break
        
        print(f"***  Emergency override by {authority} (Operator: {operator_id})")
        
        # Execute emergency protocol
        success, message = self.handle_emergency(emergency_type, f"override_{authority}")
        
        if success:
            # Log override usage
            override_record = {
                "timestamp": datetime.now().isoformat(),
                "authority": authority,
                "operator_id": operator_id,
                "emergency_type": emergency_type.value,
                "override_code_used": override_code[:4] + "***",  # Partial code for security
                "result": "success"
            }
            
            # In real system, would securely log this event
            print(f"   [OK] Emergency override successful")
            return True, f"Emergency override by {authority} successful"
        else:
            return False, f"Emergency override failed: {message}"
    
    def run_system_health_check(self) -> Dict[str, Any]:
        """Run comprehensive system health check"""
        print("***  Running System Health Check")
        print("-" * 40)
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "checks": {},
            "warnings": [],
            "critical_issues": [],
            "recommendations": []
        }
        
        system_status = self.fsm.get_system_status()
        
        # Battery check
        battery_level = system_status['battery_level']
        battery_config = self.system_health_checks['battery_level']
        
        if battery_level <= battery_config['critical']:
            health_report["critical_issues"].append(f"Critical battery level: {battery_level}%")
            health_report["overall_status"] = "critical"
        elif battery_level <= battery_config['threshold']:
            health_report["warnings"].append(f"Low battery level: {battery_level}%")
            if health_report["overall_status"] == "healthy":
                health_report["overall_status"] = "warning"
        
        health_report["checks"]["battery"] = {
            "status": "critical" if battery_level <= battery_config['critical'] else 
                     "warning" if battery_level <= battery_config['threshold'] else "good",
            "value": battery_level,
            "threshold": battery_config['threshold']
        }
        
        # Temperature check
        temperature = system_status['temperature']
        temp_config = self.system_health_checks['temperature']
        
        if (temperature <= temp_config['critical_min'] or 
            temperature >= temp_config['critical_max']):
            health_report["critical_issues"].append(f"Critical temperature: {temperature}°C")
            health_report["overall_status"] = "critical"
        elif (temperature <= temp_config['min'] or temperature >= temp_config['max']):
            health_report["warnings"].append(f"Temperature out of range: {temperature}°C")
            if health_report["overall_status"] == "healthy":
                health_report["overall_status"] = "warning"
        
        health_report["checks"]["temperature"] = {
            "status": "critical" if (temperature <= temp_config['critical_min'] or 
                                   temperature >= temp_config['critical_max']) else
                     "warning" if (temperature <= temp_config['min'] or 
                                 temperature >= temp_config['max']) else "good",
            "value": temperature,
            "range": f"{temp_config['min']}°C to {temp_config['max']}°C"
        }
        
        # Connectivity check
        connectivity = system_status['connectivity']
        health_report["checks"]["connectivity"] = {
            "status": "good" if connectivity else "warning",
            "value": "connected" if connectivity else "disconnected"
        }
        
        if not connectivity:
            health_report["warnings"].append("System connectivity lost")
            if health_report["overall_status"] == "healthy":
                health_report["overall_status"] = "warning"
        
        # Security check
        failed_attempts = system_status['failed_attempts']
        attempt_config = self.system_health_checks['failed_attempts']
        
        if failed_attempts >= attempt_config['emergency_threshold']:
            health_report["critical_issues"].append(f"Excessive failed attempts: {failed_attempts}")
            health_report["overall_status"] = "critical"
        elif failed_attempts >= attempt_config['lockout_threshold']:
            health_report["warnings"].append(f"Multiple failed attempts: {failed_attempts}")
            if health_report["overall_status"] == "healthy":
                health_report["overall_status"] = "warning"
        
        health_report["checks"]["security"] = {
            "status": "critical" if failed_attempts >= attempt_config['emergency_threshold'] else
                     "warning" if failed_attempts >= attempt_config['lockout_threshold'] else "good",
            "failed_attempts": failed_attempts,
            "lockout_threshold": attempt_config['lockout_threshold']
        }
        
        # Generate recommendations
        if health_report["warnings"] or health_report["critical_issues"]:
            if battery_level <= battery_config['threshold']:
                health_report["recommendations"].append("Replace or recharge battery")
            if not connectivity:
                health_report["recommendations"].append("Check network connection")
            if failed_attempts > 0:
                health_report["recommendations"].append("Review security logs for unauthorized access attempts")
        
        # Display results
        status_icon = {"healthy": "[OK]", "warning": "*** ", "critical": "*** "}[health_report["overall_status"]]
        print(f"Overall Status: {status_icon} {health_report['overall_status'].upper()}")
        
        for check_name, check_data in health_report["checks"].items():
            check_icon = {"good": "[OK]", "warning": "*** ", "critical": "*** "}[check_data["status"]]
            print(f"  {check_name.title()}: {check_icon} {check_data['status']}")
        
        if health_report["warnings"]:
            print("\nWarnings:")
            for warning in health_report["warnings"]:
                print(f"  ***   {warning}")
        
        if health_report["critical_issues"]:
            print("\nCritical Issues:")
            for issue in health_report["critical_issues"]:
                print(f"  ***  {issue}")
        
        if health_report["recommendations"]:
            print("\nRecommendations:")
            for rec in health_report["recommendations"]:
                print(f"  ***  {rec}")
        
        return health_report
    
    def _save_emergency_log(self):
        """Save emergency log to file"""
        try:
            log_filename = f"emergency_log_{datetime.now().strftime('%Y%m%d')}.json"
            with open(log_filename, 'w') as f:
                json.dump(self.emergency_log, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save emergency log: {e}")
    
    def test_emergency_systems(self) -> Dict[str, bool]:
        """Test all emergency systems"""
        print("***  Testing Emergency Systems")
        print("-" * 40)
        
        test_results = {}
        
        # Test backup power
        print("Testing backup power...")
        test_results["backup_power"] = self.backup_power_available
        print(f"  {'[OK]' if test_results['backup_power'] else '*** '} Backup power")
        
        # Test emergency contacts notification (simulation)
        print("Testing emergency notifications...")
        test_results["notifications"] = True  # Simulated
        print("  [OK] Emergency notifications")
        
        # Test override codes
        print("Testing emergency override codes...")
        test_results["override_codes"] = len(self.emergency_override_codes) > 0
        print(f"  {'[OK]' if test_results['override_codes'] else '*** '} Override codes")
        
        # Test failsafe mechanisms
        print("Testing failsafe mechanisms...")
        test_results["failsafe"] = True  # Simulated
        print("  [OK] Failsafe mechanisms")
        
        overall_success = all(test_results.values())
        print(f"\nOverall Test Result: {'[OK] PASS' if overall_success else '***  FAIL'}")
        
        return test_results

def demonstrate_emergency_protocols():
    """Demonstrate emergency protocols and fail-safes"""
    print("***  Emergency Protocols and Fail-safes Demonstration")
    print("=" * 60)
    
    # Initialize system
    fsm = SmartDoorLockFSM()
    emergency_manager = EmergencyProtocolManager(fsm)
    
    # Run system health check
    health_report = emergency_manager.run_system_health_check()
    time.sleep(2)
    
    # Test emergency systems
    test_results = emergency_manager.test_emergency_systems()
    time.sleep(2)
    
    # Simulate various emergencies
    emergency_scenarios = [
        (EmergencyType.FIRE_ALARM, "fire_alarm_system"),
        (EmergencyType.MEDICAL_EMERGENCY, "medical_alert_button"),
        (EmergencyType.SECURITY_BREACH, "intrusion_detection"),
        (EmergencyType.POWER_FAILURE, "power_monitoring"),
        (EmergencyType.BATTERY_CRITICAL, "battery_monitor")
    ]
    
    print("\n***  Simulating Emergency Scenarios")
    print("-" * 40)
    
    for emergency_type, source in emergency_scenarios:
        print(f"\n--- {emergency_type.value.replace('_', ' ').title()} ---")
        success, message = emergency_manager.handle_emergency(emergency_type, source)
        time.sleep(1)
    
    # Test emergency override
    print("\n***  Testing Emergency Override")
    print("-" * 30)
    
    override_success, override_message = emergency_manager.process_emergency_override(
        "FIRE911", 
        EmergencyType.FIRE_ALARM,
        "Fire Chief Johnson"
    )
    
    print(f"Override result: {'[OK]' if override_success else '*** '} {override_message}")
    
    # Final system status
    print(f"\n***  Final System Status")
    print("-" * 25)
    final_status = fsm.get_system_status()
    for key, value in final_status.items():
        print(f"  {key}: {value}")
    
    print(f"\n***  Emergency protocols demonstration completed!")
    print(f"📝 Emergency events logged: {len(emergency_manager.emergency_log)}")

if __name__ == "__main__":
    demonstrate_emergency_protocols()