from pathlib import Path

current_directory = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_directory}: ")

for filepath in current_directory.iterdir():
    if filepath.name == current_file:
        continue

    print(f"    - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"   - Content: {content}")    
