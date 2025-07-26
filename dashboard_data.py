"""
Smart Door Lock Dashboard - Data Processing Module
Handles data reading, processing, and analytics for the dashboard
"""

import csv
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import os
from collections import defaultdict, Counter
import json

class DashboardDataManager:
    """Manages data processing and analytics for the smart door lock dashboard"""
    
    def __init__(self, log_file: str = "lock_log.csv"):
        self.log_file = log_file
        self.data_cache = []
        self.last_update = None
        self.stats_cache = {}
        
    def read_log_data(self) -> List[Dict[str, Any]]:
        """Read and parse the CSV log file"""
        data = []
        if not os.path.exists(self.log_file):
            return data
            
        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        try:
                            timestamp = datetime.fromisoformat(row[0])
                            action = row[1]
                            reason = row[2]
                            
                            # Parse state transition
                            if '→' in action:
                                from_state, to_state = action.split(' → ')
                                from_state = from_state.strip()
                                to_state = to_state.strip()
                            else:
                                from_state = to_state = action.strip()
                            
                            data.append({
                                'timestamp': timestamp,
                                'action': action,
                                'from_state': from_state,
                                'to_state': to_state,
                                'reason': reason,
                                'raw_row': row
                            })
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing row {row}: {e}")
                            continue
        except Exception as e:
            print(f"Error reading log file: {e}")
            
        return sorted(data, key=lambda x: x['timestamp'])
    
    def get_current_state(self) -> str:
        """Get the current state of the door lock"""
        data = self.read_log_data()
        if not data:
            return "UNKNOWN"
        return data[-1]['to_state']
    
    def get_recent_activity(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent activity within specified hours"""
        data = self.read_log_data()
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [entry for entry in data if entry['timestamp'] >= cutoff_time]
    
    def calculate_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive statistics from the log data"""
        data = self.read_log_data()
        if not data:
            return {
                'total_events': 0,
                'lock_events': 0,
                'unlock_events': 0,
                'current_state': 'UNKNOWN',
                'last_activity': None,
                'uptime_hours': 0,
                'state_distribution': {},
                'hourly_activity': {},
                'daily_activity': {},
                'average_session_duration': 0
            }
        
        # Basic counts
        total_events = len(data)
        lock_events = sum(1 for entry in data if entry['to_state'] == 'LOCKED')
        unlock_events = sum(1 for entry in data if entry['to_state'] == 'UNLOCKED')
        
        # Current state and last activity
        current_state = data[-1]['to_state']
        last_activity = data[-1]['timestamp']
        
        # Calculate uptime
        first_event = data[0]['timestamp']
        uptime_hours = (datetime.now() - first_event).total_seconds() / 3600
        
        # State distribution
        state_counter = Counter(entry['to_state'] for entry in data)
        state_distribution = dict(state_counter)
        
        # Activity patterns
        hourly_activity = defaultdict(int)
        daily_activity = defaultdict(int)
        
        for entry in data:
            hour = entry['timestamp'].hour
            date = entry['timestamp'].date()
            hourly_activity[hour] += 1
            daily_activity[str(date)] += 1
        
        # Calculate average session duration
        session_durations = []
        current_session_start = None
        current_session_state = None
        
        for entry in data:
            if current_session_state != entry['to_state']:
                if current_session_start and current_session_state:
                    duration = (entry['timestamp'] - current_session_start).total_seconds()
                    session_durations.append(duration)
                current_session_start = entry['timestamp']
                current_session_state = entry['to_state']
        
        avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
        
        return {
            'total_events': total_events,
            'lock_events': lock_events,
            'unlock_events': unlock_events,
            'current_state': current_state,
            'last_activity': last_activity,
            'uptime_hours': round(uptime_hours, 2),
            'state_distribution': state_distribution,
            'hourly_activity': dict(hourly_activity),
            'daily_activity': dict(daily_activity),
            'average_session_duration': round(avg_session_duration, 2),
            'session_durations': session_durations
        }
    
    def get_activity_timeline(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get activity timeline for visualization"""
        data = self.read_log_data()
        cutoff_time = datetime.now() - timedelta(days=days)
        recent_data = [entry for entry in data if entry['timestamp'] >= cutoff_time]
        
        timeline = []
        for entry in recent_data:
            timeline.append({
                'timestamp': entry['timestamp'].isoformat(),
                'state': entry['to_state'],
                'action': entry['action'],
                'reason': entry['reason']
            })
        
        return timeline
    
    def export_data(self, format: str = 'json', filename: Optional[str] = None) -> str:
        """Export data in specified format"""
        data = self.read_log_data()
        stats = self.calculate_statistics()
        
        export_data = {
            'export_timestamp': datetime.now().isoformat(),
            'statistics': stats,
            'raw_data': []
        }
        
        for entry in data:
            export_data['raw_data'].append({
                'timestamp': entry['timestamp'].isoformat(),
                'action': entry['action'],
                'from_state': entry['from_state'],
                'to_state': entry['to_state'],
                'reason': entry['reason']
            })
        
        if not filename:
            filename = f"dashboard_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format.lower() == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        elif format.lower() == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Action', 'From State', 'To State', 'Reason'])
                for entry in data:
                    writer.writerow([
                        entry['timestamp'].isoformat(),
                        entry['action'],
                        entry['from_state'],
                        entry['to_state'],
                        entry['reason']
                    ])
        
        return filename
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health indicators"""
        data = self.read_log_data()
        stats = self.calculate_statistics()
        
        # Check for recent activity
        recent_activity = self.get_recent_activity(1)  # Last hour
        is_active = len(recent_activity) > 0
        
        # Check for errors or anomalies
        error_indicators = []
        if stats['total_events'] == 0:
            error_indicators.append("No activity recorded")
        
        # Check file accessibility
        log_file_accessible = os.path.exists(self.log_file) and os.access(self.log_file, os.R_OK)
        
        health_status = "HEALTHY"
        if error_indicators:
            health_status = "WARNING"
        if not log_file_accessible:
            health_status = "ERROR"
        
        return {
            'status': health_status,
            'is_active': is_active,
            'log_file_accessible': log_file_accessible,
            'last_update': datetime.now().isoformat(),
            'error_indicators': error_indicators,
            'data_points': len(data)
        }

# Utility functions for dashboard components
def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"

def format_timestamp(timestamp: datetime) -> str:
    """Format timestamp for display"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds//3600}h ago"
    elif diff.seconds > 60:
        return f"{diff.seconds//60}m ago"
    else:
        return "Just now"

if __name__ == "__main__":
    # Test the data manager
    dm = DashboardDataManager()
    stats = dm.calculate_statistics()
    print("Dashboard Data Manager Test:")
    print(f"Current State: {stats['current_state']}")
    print(f"Total Events: {stats['total_events']}")
    print(f"Lock Events: {stats['lock_events']}")
    print(f"Unlock Events: {stats['unlock_events']}")
    print(f"Uptime: {stats['uptime_hours']} hours")