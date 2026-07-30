# Read the new dictionary text
with open('new_dict.txt', 'r', encoding='utf-8') as f:
    new_dict_code = f.read()

# Read app.py
with open('app.py', 'r', encoding='utf-8') as f:
    app_code = f.read()

# Split and join using standard marker substrings
start_marker = "# --- Dos and Don'ts Dictionary ---\n"
end_marker = "# --- Model Loading ---"

if start_marker in app_code and end_marker in app_code:
    parts = app_code.split(start_marker)
    after_part = parts[1].split(end_marker)
    
    new_app_code = parts[0] + start_marker + new_dict_code + "\n" + end_marker + after_part[1]
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_app_code)
    print("Injected successfully using robust string markers!")
else:
    print("Error: Could not find markers in app.py!")
