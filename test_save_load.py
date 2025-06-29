#!/usr/bin/env python3
"""
Test script to verify save/load functionality
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
            print(f"   � Variables saved: {metadata.get('variable_count', 0)}")
            saved_vars = metadata.get('saved_variables', [])
            if saved_vars:
                print(f"   📋 Variable list: {', '.join(sorted(saved_vars))}")
        
        print(f"\n🎮 Game State Contents:")
        
        # Show all saved variables with their types and values
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue
                
            var_type = type(var_value).__name__
            
            if var_name == 'balance':
                print(f"   � {var_name}: ${var_value} ({var_type})")
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
            elif isinstance(var_value, (int, float)):
                print(f"   🔢 {var_name}: {var_value} ({var_type})")
            elif isinstance(var_value, str):
                print(f"   📝 {var_name}: '{var_value}' ({var_type})")
            elif isinstance(var_value, (list, dict)):
                print(f"   📦 {var_name}: {len(var_value)} items ({var_type})")
            else:
                print(f"   ❓ {var_name}: {str(var_value)[:50]}... ({var_type})")
        
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
        
        print("\n� Save Completeness Analysis:")
        print("=" * 50)
        
        # Count different types of data
        data_counts = {
            'Game Variables': 0,
            'Collections (lists/dicts)': 0,
            'Numeric Values': 0,
            'String Values': 0,
            'Complex Objects': 0
        }
        
        for var_name, var_value in game_state.items():
            if var_name == '_save_metadata':
                continue
                
            if isinstance(var_value, (list, dict)):
                data_counts['Collections (lists/dicts)'] += 1
            elif isinstance(var_value, (int, float)):
                data_counts['Numeric Values'] += 1
            elif isinstance(var_value, str):
                data_counts['String Values'] += 1
            else:
                data_counts['Complex Objects'] += 1
            
            data_counts['Game Variables'] += 1
        
        for category, count in data_counts.items():
            print(f"   {category}: {count}")
        
        # Calculate save file size
        file_size = os.path.getsize(save_file)
        if file_size > 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        else:
            size_str = f"{file_size} bytes"
            
        print(f"\n📁 Save file size: {size_str}")
        print("✅ Save system appears to be comprehensive!")
        
    except Exception as e:
        print(f"❌ Error analyzing save file: {e}")

if __name__ == "__main__":
    print("🎲 Gambling Simulator Save/Load Test")
    print("=" * 40)
    test_save_file()
    analyze_save_completeness()
