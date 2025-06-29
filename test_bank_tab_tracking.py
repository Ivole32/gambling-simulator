#!/usr/bin/env python3

"""
Test script for verifying bank tab state tracking and restoration.
This script simulates usage and verifies the save/load system tracks inner tab states.
"""

import os
import sys
import dill
import time

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bank_tab_tracking():
    """Test the bank tab tracking functionality"""
    
    print("🧪 Testing Bank Tab State Tracking")
    print("=" * 50)
    
    save_file = "gambling_simulator_save.dill"
    
    # Clean up any existing save file
    if os.path.exists(save_file):
        os.remove(save_file)
        print("🗑️ Cleaned up existing save file")
    
    # Import UI module to get access to the state tracking
    try:
        import UI as ui_module
        print("✅ Successfully imported UI module")
    except Exception as e:
        print(f"❌ Failed to import UI module: {e}")
        return False
    
    # Check if the new bank tracking components exist
    required_components = [
        'current_ui_state', 
        'bank_tabview_ref',
        'track_bank_tab_change'
    ]
    
    missing_components = []
    for component in required_components:
        if not hasattr(ui_module, component):
            missing_components.append(component)
    
    if missing_components:
        print(f"❌ Missing components: {missing_components}")
        return False
    else:
        print("✅ All required components found")
    
    # Test initial state
    print(f"\n📊 Initial UI State:")
    current_state = ui_module.current_ui_state
    print(f"  - Active function: {current_state.get('active_function', 'None')}")
    print(f"  - Bank active tab: {current_state.get('bank_active_tab', 'None')}")
    print(f"  - Last update: {current_state.get('last_update', 'None')}")
    
    # Simulate bank tab state changes
    print(f"\n🏦 Simulating Bank Tab Changes:")
    
    # Test 1: Set different tab states
    test_tabs = ["📊 Dashboard", "📈 Analytics", "💳 Credit", "📋 Transactions"]
    
    for tab in test_tabs:
        ui_module.current_ui_state['bank_active_tab'] = tab
        ui_module.current_ui_state['active_function'] = 'show_bank'
        ui_module.current_ui_state['last_update'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"  - Set bank tab to: {tab}")
        
        # Test save with this state
        try:
            ui_module.save_game_state()
            print(f"    ✅ Save successful for {tab}")
        except Exception as e:
            print(f"    ❌ Save failed for {tab}: {e}")
            return False
        
        # Test load and verify state is preserved
        try:
            ui_module.load_game_state()
            restored_tab = ui_module.current_ui_state.get('bank_active_tab')
            if restored_tab == tab:
                print(f"    ✅ Load successful, tab restored: {restored_tab}")
            else:
                print(f"    ❌ Load failed, expected {tab}, got {restored_tab}")
                return False
        except Exception as e:
            print(f"    ❌ Load failed for {tab}: {e}")
            return False
    
    # Test 2: Verify save file contains bank tab info
    print(f"\n💾 Analyzing Save File Contents:")
    
    try:
        with open(save_file, 'rb') as f:
            save_data = dill.load(f)
        
        metadata = save_data.get('_save_metadata', {})
        saved_vars = metadata.get('saved_variables', [])
        ui_state = metadata.get('ui_state', {})
        current_ui = ui_state.get('current_ui_state', {})
        
        print(f"  - Total saved variables: {len(saved_vars)}")
        print(f"  - current_ui_state in saved vars: {'current_ui_state' in saved_vars}")
        print(f"  - Bank tab in UI state: {current_ui.get('bank_active_tab', 'Not found')}")
        print(f"  - Active function: {current_ui.get('active_function', 'Not found')}")
        print(f"  - Last update: {current_ui.get('last_update', 'Not found')}")
        
        # Check if bank_active_tab is properly saved
        if current_ui.get('bank_active_tab'):
            print("  ✅ Bank tab state is properly saved in UI state")
        else:
            print("  ❌ Bank tab state is missing from UI state")
            return False
            
    except Exception as e:
        print(f"  ❌ Failed to analyze save file: {e}")
        return False
    
    # Test 3: Verify the tracking function exists and works
    print(f"\n🔄 Testing Bank Tab Change Tracking:")
    
    # Mock a bank tabview reference (since we're not running the full UI)
    class MockTabview:
        def __init__(self, initial_tab="📊 Dashboard"):
            self.current_tab = initial_tab
        
        def get(self):
            return self.current_tab
        
        def set(self, tab):
            self.current_tab = tab
    
    # Test the tracking function
    ui_module.bank_tabview_ref = MockTabview("📈 Analytics")
    
    try:
        ui_module.track_bank_tab_change()
        tracked_tab = ui_module.current_ui_state.get('bank_active_tab')
        if tracked_tab == "📈 Analytics":
            print("  ✅ Bank tab tracking function works correctly")
        else:
            print(f"  ❌ Tracking failed, expected '📈 Analytics', got '{tracked_tab}'")
            return False
    except Exception as e:
        print(f"  ❌ Bank tab tracking function failed: {e}")
        return False
    
    print(f"\n🎉 All Bank Tab Tracking Tests Passed!")
    print(f"\n📋 Test Summary:")
    print(f"  ✅ Bank tab state is tracked in current_ui_state")
    print(f"  ✅ Bank tab state is saved and loaded correctly")
    print(f"  ✅ Save file contains bank tab information")
    print(f"  ✅ Tracking function works as expected")
    print(f"\n🏦 The save system now includes comprehensive inner tab tracking!")
    
    # Clean up
    if os.path.exists(save_file):
        os.remove(save_file)
        print(f"\n🗑️ Cleaned up test save file")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Bank Tab Tracking Tests...")
    
    success = test_bank_tab_tracking()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("🏦 Bank tab state tracking is now fully implemented!")
    else:
        print("\n❌ Some tests failed!")
        print("🔧 Please check the implementation.")
    
    print("\n" + "=" * 60)
