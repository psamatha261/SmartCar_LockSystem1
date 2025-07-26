"""
Fix Unicode characters in Python files for Windows terminal compatibility
"""

import re

def fix_unicode_in_file(filename):
    """Fix Unicode emoji characters in a file"""
    
    # Read the file
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacements for common emoji characters
    replacements = {
        '🚀': '*** ',
        '🧪': '*** ',
        '🏠': '*** ',
        '⚠️': '*** ',
        '🔍': '*** ',
        '💪': '*** ',
        '📊': '*** ',
        '✅': '[OK]',
        '❌': '[FAIL]',
        '🎉': '*** ',
        '🚗': '*** ',
        '🚨': '*** ',
        '🔧': '*** ',
        '🔋': '*** ',
        '📡': '*** ',
        '🛡️': '*** ',
        '📉': '*** ',
        '🔒': '*** ',
        '🔓': '*** ',
        '🚫': '*** ',
        '⏰': '*** ',
        '📞': '*** ',
        '📱': '*** ',
        '💡': '*** ',
        '🏥': '*** ',
        '🔑': '*** ',
        '💾': '*** ',
        '🗑️': '*** ',
        '🔄': '*** ',
        '📊': '*** ',
        '⚙️': '*** ',
        '❓': '*** ',
        '❌': '*** ',
        '⏸️': '*** ',
        '📢': '*** ',
        '🎭': '*** ',
        '---': '---'
    }
    
    # Apply replacements
    for emoji, replacement in replacements.items():
        content = content.replace(emoji, replacement)
    
    # Write back to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed Unicode characters in {filename}")

if __name__ == "__main__":
    files_to_fix = [
        'test_scenarios.py',
        'door_lock_simulator.py', 
        'emergency_protocols.py'
    ]
    
    for filename in files_to_fix:
        try:
            fix_unicode_in_file(filename)
        except Exception as e:
            print(f"Error fixing {filename}: {e}")
    
    print("Unicode fix completed!")