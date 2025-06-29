#!/usr/bin/env python3
"""
Test script to verify advanced save/load functionality
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
            print(f"\n📊 Snapshot Metadata:")
            print(f"   💾 Save timestamp: {metadata.get('timestamp', 'N/A')}")
            print(f"   📈 Variables saved: {metadata.get('variable_count', 0)}")
            print(f"   🔧 Save type: {metadata.get('save_type', 'unknown')}")
            
            saved_vars = metadata.get('saved_variables', [])
            if saved_vars:
                non_meta_vars = [v for v in saved_vars if not v.endswith('_META')]
                meta_vars = [v for v in saved_vars if v.endswith('_META')]
                print(f"   📋 Data variables: {len(non_meta_vars)}")
                print(f"   📋 Metadata entries: {len(meta_vars)}")
                if len(non_meta_vars) <= 15:
                    print(f"   📝 Variable list: {', '.join(sorted(non_meta_vars))}")
                else:
                    print(f"   📝 Variables: {', '.join(sorted(non_meta_vars)[:12])}... (+{len(non_meta_vars)-12} more)")
            
            failed_vars = metadata.get('failed_variables', [])
            if failed_vars:
                print(f"   ⚠️ Failed to save: {len(failed_vars)} variables")
                for var_name, error in failed_vars[:3]:
                    print(f"      {var_name}: {error[:50]}...")
        
        print(f"\n🎮 Game State Contents:")
        
        # Show all saved variables with their types and values
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue
            if var_name.endswith('_META'):
                continue  # Skip metadata entries in main display
                
            var_type = type(var_value).__name__
            
            if var_name == 'balance':
                print(f"   💰 {var_name}: ${var_value} ({var_type})")
            elif var_name == 'inventory':
                print(f"   🎒 {var_name}: {len(var_value)} items ({var_type})")
                if var_value:
                    for emoji, quantity in var_value.items():
                        print(f"      {emoji} x{quantity}")
            elif var_name == 'transaction_history':
                print(f"   📋 {var_name}: {len(var_value)} transactions ({var_type})")
                if var_value:
                    print("      Recent transactions:")
                    for transaction in var_value[-3:]:
                        print(f"        {transaction['timestamp']}: {transaction['type']} ${transaction['amount']} - {transaction['description']}")
            elif var_name == 'shop_items':
                print(f"   🏪 {var_name}: {len(var_value)} items ({var_type})")
                if var_value:
                    print("      Current prices:")
                    for emoji, item_data in list(var_value.items())[:3]:  # Show first 3
                        print(f"        {emoji} {item_data['name']}: ${item_data['price']} (base: ${item_data['base_price']})")
                    if len(var_value) > 3:
                        print(f"        ... and {len(var_value) - 3} more items")
            elif var_name == 'loan_info':
                print(f"   🏦 {var_name}: ${var_value.get('amount', 0)} loan ({var_type})")
            elif var_name == 'current_ui_state':
                print(f"   🖥️ {var_name}: {var_value.get('active_function', 'unknown')} active ({var_type})")
                # Show bank tab state if available
                bank_tab = var_value.get('bank_active_tab')
                if bank_tab:
                    print(f"      🏦 Bank tab: {bank_tab}")
                last_update = var_value.get('last_update')
                if last_update:
                    print(f"      ⏰ Last update: {last_update}")
            elif isinstance(var_value, (int, float)):
                print(f"   🔢 {var_name}: {var_value} ({var_type})")
            elif isinstance(var_value, str):
                display_val = var_value if len(var_value) <= 30 else var_value[:30] + "..."
                print(f"   📝 {var_name}: '{display_val}' ({var_type})")
            elif isinstance(var_value, (list, dict)):
                print(f"   📦 {var_name}: {len(var_value)} items ({var_type})")
            else:
                print(f"   ❓ {var_name}: {str(var_value)[:50]}... ({var_type})")
        
        # Show metadata variables if any
        meta_vars = [k for k in game_state.keys() if k.endswith('_META')]
        if meta_vars:
            print(f"\n🔍 Non-serializable object metadata ({len(meta_vars)} items):")
            for meta_var in meta_vars[:5]:  # Show first 5
                meta_data = game_state[meta_var]
                original_name = meta_var[:-5]  # Remove '_META'
                print(f"   ⚠️ {original_name}: {meta_data.get('type', 'unknown')} - {meta_data.get('repr', 'no info')[:40]}...")
            if len(meta_vars) > 5:
                print(f"   ... and {len(meta_vars) - 5} more metadata entries")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading save file: {e}")
        return False

def analyze_save_completeness():
    """Analyze how complete our save system is"""
    save_file = "gambling_simulator_save.dill"
    
    if not os.path.exists(save_file):
        print("❌ No save file to analyze!")
        return
    
    try:
        with open(save_file, 'rb') as f:
            game_state = dill.load(f)
        
        print("\n🔍 Save Completeness Analysis:")
        print("=" * 50)
        
        # Count different types of data
        data_counts = {
            'Serializable Variables': 0,
            'Collections (lists/dicts)': 0,
            'Numeric Values': 0,
            'String Values': 0,
            'Complex Objects': 0,
            'Metadata Entries': 0
        }
        
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue
                
            if var_name.endswith('_META'):
                data_counts['Metadata Entries'] += 1
                continue
                
            if isinstance(var_value, (list, dict)):
                data_counts['Collections (lists/dicts)'] += 1
            elif isinstance(var_value, (int, float)):
                data_counts['Numeric Values'] += 1
            elif isinstance(var_value, str):
                data_counts['String Values'] += 1
            else:
                data_counts['Complex Objects'] += 1
            
            data_counts['Serializable Variables'] += 1
        
        for category, count in data_counts.items():
            print(f"   {category}: {count}")
        
        # Analyze metadata
        metadata = game_state.get('_save_metadata', {})
        failed_vars = metadata.get('failed_variables', [])
        if failed_vars:
            print(f"\n⚠️ Variables that couldn't be serialized: {len(failed_vars)}")
            print("   Most common issues:")
            error_types = {}
            for var_name, error in failed_vars:
                error_key = error.split(':')[0] if ':' in error else error[:30]
                error_types[error_key] = error_types.get(error_key, 0) + 1
            for error, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"     {error}: {count} variables")
        
        # Calculate save file size
        file_size = os.path.getsize(save_file)
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        elif file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"
            
        print(f"\n📁 Save file size: {size_str}")
        
        # UI state analysis
        ui_state = metadata.get('ui_state', {})
        if ui_state:
            print(f"🖥️ UI state captured:")
            current_ui = ui_state.get('current_ui_state', {})
            if current_ui:
                print(f"   Active function: {current_ui.get('active_function', 'unknown')}")
                print(f"   Last update: {current_ui.get('last_update', 'unknown')}")
            window_info = ui_state.get('window_info', {})
            if window_info:
                print(f"   Window: {window_info.get('geometry', 'unknown geometry')}")
        
        print("✅ Advanced save system analysis complete!")
        
    except Exception as e:
        print(f"❌ Error analyzing save file: {e}")

if __name__ == "__main__":
    print("🎲 Gambling Simulator Advanced Save/Load Test")
    print("=" * 50)
    test_save_file()
    analyze_save_completeness()
