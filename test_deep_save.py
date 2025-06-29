#!/usr/bin/env python3
"""
Enhanced test script to verify comprehensive save/load functionality
"""
import dill
import os

def test_save_file():
    save_file = "gambling_simulator_save.dill"
    
    if not os.path.exists(save_file):
        print("❌ No save file found!")
        return False
    
    try:
        with open(save_file, 'rb') as f:
            game_state = dill.load(f)
        
        print("✅ Save file loaded successfully!")
        
        # Check for metadata
        metadata = game_state.get('_save_metadata', {})
        if metadata:
            print(f"\n📊 Deep Snapshot Metadata:")
            print(f"   💾 Save timestamp: {metadata.get('timestamp', 'N/A')}")
            print(f"   📈 Variables saved: {metadata.get('variable_count', 0)}")
            print(f"   🔍 Save type: {metadata.get('save_type', 'unknown')}")
            
            saved_vars = metadata.get('saved_variables', [])
            if saved_vars:
                print(f"   📋 Variable list: {', '.join(sorted(saved_vars)[:15])}{'...' if len(saved_vars) > 15 else ''}")
            
            # Show UI state info
            ui_state = metadata.get('ui_state', {})
            if ui_state:
                print(f"\n🖥️ UI State Information:")
                current_ui = ui_state.get('current_ui_state', {})
                if current_ui:
                    print(f"   🎯 Active function: {current_ui.get('active_function', 'unknown')}")
                    print(f"   ⏰ Last update: {current_ui.get('last_update', 'unknown')}")
                
                ui_elements = ui_state.get('ui_elements', {})
                if ui_elements:
                    print(f"   🧩 UI elements captured: {len(ui_elements)}")
                    existing_elements = [name for name, info in ui_elements.items() if info.get('exists') == True]
                    if existing_elements:
                        print(f"   ✅ Active UI elements: {', '.join(existing_elements[:5])}{'...' if len(existing_elements) > 5 else ''}")
                
                window_state = ui_state.get('window_state', {})
                if window_state:
                    print(f"   🏠 Window geometry: {window_state.get('geometry', 'unknown')}")
                    print(f"   📝 Window title: {window_state.get('title', 'unknown')}")
        
        print(f"\n🎮 Complete Game State Analysis:")
        
        # Categorize all variables
        categories = {
            'Game Core': [],
            'UI Elements': [],
            'Collections': [],
            'Functions/Objects': [],
            'Numeric Values': [],
            'Text/Strings': [],
            'Type Info': []
        }
        
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue
                
            var_type = type(var_value).__name__
            
            if var_name.endswith('_TYPE_INFO'):
                categories['Type Info'].append(var_name)
            elif var_name in ['balance', 'inventory', 'shop_items', 'transaction_history', 'loan_info']:
                categories['Game Core'].append(var_name)
            elif 'frame' in var_name.lower() or 'label' in var_name.lower() or 'button' in var_name.lower() or var_name.startswith('current_'):
                categories['UI Elements'].append(var_name)
            elif isinstance(var_value, (list, dict)):
                categories['Collections'].append(var_name)
            elif callable(var_value) or hasattr(var_value, '__call__'):
                categories['Functions/Objects'].append(var_name)
            elif isinstance(var_value, (int, float)):
                categories['Numeric Values'].append(var_name)
            elif isinstance(var_value, str):
                categories['Text/Strings'].append(var_name)
            else:
                categories['Functions/Objects'].append(var_name)
        
        for category, vars_list in categories.items():
            if vars_list:
                print(f"   {category}: {len(vars_list)} items")
                if len(vars_list) <= 8:
                    print(f"     └─ {', '.join(vars_list)}")
                else:
                    print(f"     └─ {', '.join(vars_list[:8])}... (+{len(vars_list)-8} more)")
        
        # Show detailed info for key game variables
        print(f"\n💎 Key Game Variables:")
        key_vars = ['balance', 'inventory', 'shop_items', 'transaction_history', 'loan_info', 'current_bet', 'game_active']
        for var in key_vars:
            if var in game_state:
                value = game_state[var]
                if var == 'balance':
                    print(f"   💰 {var}: ${value}")
                elif var == 'inventory':
                    print(f"   🎒 {var}: {len(value)} items")
                    if value:
                        for emoji, qty in list(value.items())[:3]:
                            print(f"       {emoji} x{qty}")
                elif var == 'shop_items':
                    print(f"   🏪 {var}: {len(value)} items")
                elif var == 'transaction_history':
                    print(f"   📋 {var}: {len(value)} transactions")
                elif var == 'loan_info':
                    print(f"   🏦 {var}: ${value.get('amount', 0)} loan")
                else:
                    print(f"   🎯 {var}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading save file: {e}")
        return False

def analyze_save_completeness():
    """Analyze how comprehensive our deep save system is"""
    save_file = "gambling_simulator_save.dill"
    
    if not os.path.exists(save_file):
        print("❌ No save file to analyze!")
        return
    
    try:
        with open(save_file, 'rb') as f:
            game_state = dill.load(f)
        
        print("\n🔍 Deep Save Completeness Analysis:")
        print("=" * 60)
        
        # Count different types of data
        total_vars = len([k for k in game_state.keys() if k != '_save_metadata'])
        ui_vars = len([k for k in game_state.keys() if 'frame' in k.lower() or 'label' in k.lower() or k.startswith('current_')])
        game_vars = len([k for k in game_state.keys() if k in ['balance', 'inventory', 'shop_items', 'transaction_history', 'loan_info']])
        type_info_vars = len([k for k in game_state.keys() if k.endswith('_TYPE_INFO')])
        
        print(f"   📊 Total variables saved: {total_vars}")
        print(f"   🎮 Core game variables: {game_vars}")
        print(f"   🖥️ UI-related variables: {ui_vars}")
        print(f"   🔍 Type info entries: {type_info_vars}")
        print(f"   📦 Other variables: {total_vars - ui_vars - game_vars - type_info_vars}")
        
        # Calculate save file size
        file_size = os.path.getsize(save_file)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"
            
        print(f"\n📁 Save file size: {size_str}")
        
        # Check metadata for save type
        metadata = game_state.get('_save_metadata', {})
        save_type = metadata.get('save_type', 'unknown')
        
        if save_type == 'deep_snapshot':
            print("✅ Deep snapshot system is active and comprehensive!")
        else:
            print("⚠️ Save system may not be using deep snapshot mode")
        
    except Exception as e:
        print(f"❌ Error analyzing save file: {e}")

if __name__ == "__main__":
    print("🎲 Gambling Simulator Deep Save/Load Test")
    print("=" * 50)
    test_save_file()
    analyze_save_completeness()
