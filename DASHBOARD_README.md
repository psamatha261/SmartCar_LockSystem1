# Smart Door Lock Dashboard

A comprehensive tkinter-based desktop dashboard for monitoring and controlling the smart door lock system with real-time data visualization, historical analytics, and interactive controls.

## Features

### 🔍 Real-time Monitoring
- Live door lock status display with LED-style indicators
- System health monitoring
- Last activity tracking
- Auto-refresh functionality (configurable interval)

### 📊 Data Visualization
- **Timeline Chart**: Activity timeline showing state changes over the last 7 days
- **Distribution Chart**: Pie chart showing lock vs unlock ratio
- **Hourly Activity Chart**: Bar chart displaying activity patterns by hour

### 🎛️ Interactive Controls
- Manual lock/unlock buttons
- Test scenario execution
- Data export (JSON/CSV formats)
- Log management (refresh, clear)

### 📈 Analytics & Statistics
- Total events counter
- Lock/unlock event counts
- System uptime tracking
- Average session duration
- Activity pattern analysis

### ⚙️ Configuration
- Auto-refresh toggle
- Refresh interval adjustment
- Settings dialog
- Help documentation

## Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Required Dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:
- `matplotlib>=3.5.0` - For data visualization charts
- `pandas>=1.3.0` - For data processing (optional, used in data manager)
- `numpy>=1.21.0` - For numerical operations

## Project Structure

```
smart_door_lock/
├── smart_lock_dashboard.py    # Main dashboard application
├── dashboard_data.py          # Data processing and analytics module
├── fsm_states.py             # Finite State Machine implementation
├── door_lock_simulator.py    # System simulator
├── test_scenarios.py         # Test scenarios and cases
├── lock_log.csv              # Historical log data
├── requirements.txt          # Python dependencies
└── DASHBOARD_README.md       # This documentation
```

## Usage

### Starting the Dashboard

1. **Basic Launch**:
   ```bash
   python smart_lock_dashboard.py
   ```

2. **From Command Line**:
   ```bash
   cd smart_door_lock
   python smart_lock_dashboard.py
   ```

### Dashboard Interface

The dashboard is organized into several panels:

#### Left Panel - System Status
- **Current State**: Shows LOCKED/UNLOCKED with color-coded LED indicator
- **System Health**: Displays HEALTHY/WARNING/ERROR status
- **Statistics**: Real-time counts and metrics
- **Manual Controls**: Lock/Unlock buttons and test execution

#### Center Panel - Analytics & Visualization
- **Timeline Tab**: Interactive timeline chart of recent activity
- **Distribution Tab**: Pie chart showing state distribution
- **Hourly Activity Tab**: Bar chart of activity by hour of day

#### Right Panel - Activity Logs
- **Log Display**: Scrollable table of recent events with timestamps
- **Log Controls**: Refresh, Export, and Clear buttons
- **Settings**: Auto-refresh configuration

#### Bottom Panel - Main Controls
- **Refresh All**: Update all dashboard data
- **Generate Report**: Create comprehensive system report
- **Settings**: Open configuration dialog
- **Help**: Display help documentation
- **Exit**: Close the application

### Key Operations

#### Manual Control
1. Click **🔒 Lock** to manually lock the door
2. Click **🔓 Unlock** to manually unlock the door
3. Click **🧪 Run Test** to execute predefined test scenarios

#### Data Export
1. Click **💾 Export** in the logs panel
2. Choose file format (JSON or CSV)
3. Select save location
4. Data will be exported with timestamps and statistics

#### Report Generation
1. Click **📊 Generate Report** in the bottom panel
2. Report will be saved as a text file with timestamp
3. Includes system status, statistics, and state distribution

#### Configuration
1. Click **⚙️ Settings** to open configuration dialog
2. Toggle auto-refresh on/off
3. Adjust refresh interval (minimum 1 second)
4. Changes apply immediately

## Data Management

### Log File Format
The system maintains logs in `lock_log.csv` with the following format:
```csv
timestamp,action,reason
2025-07-26T14:30:00.123456,UNLOCKED → LOCKED,Car shifted to Drive
2025-07-26T14:35:00.789012,LOCKED → UNLOCKED,Car shifted to Park
```

### Data Processing
- **Real-time Updates**: Dashboard refreshes every 5 seconds by default
- **Historical Analysis**: Processes up to 7 days of historical data
- **Statistics Calculation**: Automatic computation of usage patterns
- **Data Validation**: Error handling for corrupted or missing data

## Troubleshooting

### Common Issues

#### Dashboard Won't Start
- **Check Python Version**: Ensure Python 3.7+ is installed
- **Install Dependencies**: Run `pip install -r requirements.txt`
- **Check tkinter**: Verify tkinter is available (`python -c "import tkinter"`)

#### No Data Displayed
- **Check Log File**: Ensure `lock_log.csv` exists and is readable
- **Run Simulator**: Execute `python door_lock_simulator.py` to generate test data
- **Check Permissions**: Verify read/write access to the project directory

#### Charts Not Displaying
- **matplotlib Issues**: Reinstall matplotlib (`pip install --upgrade matplotlib`)
- **Backend Problems**: Try different matplotlib backend
- **Memory Issues**: Close other applications to free up memory

#### Performance Issues
- **Large Log Files**: Clear old logs or archive historical data
- **Refresh Rate**: Increase refresh interval in settings
- **System Resources**: Close unnecessary applications

### Error Messages

#### "Failed to refresh data"
- Check if log file is accessible
- Verify file permissions
- Restart the dashboard application

#### "No test scenarios available"
- Ensure `test_scenarios.py` is in the same directory
- Check if scenarios list is properly defined
- Verify import statements

#### "Failed to export data"
- Check write permissions in target directory
- Ensure sufficient disk space
- Verify file path is valid

## Advanced Usage

### Custom Test Scenarios
Edit `test_scenarios.py` to add custom test cases:
```python
scenarios = [
    {"event": "lock", "reason": "Custom test scenario"},
    {"event": "unlock", "reason": "Another custom test"},
]
```

### Data Analysis
The dashboard provides comprehensive analytics:
- **Session Duration**: Average time between state changes
- **Usage Patterns**: Hourly and daily activity distribution
- **State Distribution**: Percentage of time in each state
- **System Health**: Monitoring of data integrity and system status

### Integration
The dashboard can be integrated with:
- **External Logging Systems**: Export data to external databases
- **Monitoring Tools**: Use health status for system monitoring
- **Automation Scripts**: Trigger actions based on dashboard data

## Development

### Architecture
- **MVC Pattern**: Separation of data, view, and control logic
- **Modular Design**: Independent components for easy maintenance
- **Event-Driven**: Responsive UI with proper event handling

### Extending the Dashboard
1. **Add New Charts**: Extend the analytics panel with custom visualizations
2. **Custom Data Sources**: Modify `dashboard_data.py` for different data inputs
3. **Additional Controls**: Add new buttons and functionality to control panels
4. **Themes**: Customize colors and styles in the `setup_styles()` method

### Code Structure
- **SmartLockDashboard**: Main application class
- **DashboardDataManager**: Data processing and analytics
- **Chart Methods**: Individual methods for each visualization
- **Event Handlers**: Methods for user interactions

## Support

For issues, questions, or contributions:
1. Check this documentation first
2. Review error messages and troubleshooting section
3. Verify system requirements and dependencies
4. Test with minimal configuration

## Version History

- **v1.0**: Initial release with core dashboard functionality
- Real-time monitoring and visualization
- Manual controls and test execution
- Data export and reporting capabilities
- Comprehensive help and documentation

## License

This dashboard is part of the Smart Door Lock System project.