import os

def generate_tree(root_path, prefix="", output_file=None):
    """
    Recursively generates a visual tree structure of directories and files.
    the output is printed to console and optionally written to a file.
    the function ignores certain system and virtual environment folders and the style of the tree
    uses box-drawing characters for better visual representation a style that i like to see, so i replicated.
    """
    # Folders to ignore (customize as needed)
    ignore_list = {'.git', '__pycache__', 'node_modules', '.vscode', '.idea', 'venv', 'env', 'dist', 'build'}

    try:
        # List items, sorted alphabetically for consistency
        items = sorted(os.listdir(root_path))
    except PermissionError:
        msg = f"{prefix}[Access Denied]"
        print(msg)
        if output_file: output_file.write(msg + "\n")
        return

    # Filter out ignored items
    items = [i for i in items if i not in ignore_list]
    
    count = 0
    total = len(items)

    for item in items:
        count += 1
        full_path = os.path.join(root_path, item)
        is_last = (count == total)

        # Visual connectors
        connector = "└── " if is_last else "├── "
        
        # Current line string
        line = f"{prefix}{connector}{item}"
        
        # 1. Print to console
        print(line)
        
        # 2. Write to file
        if output_file:
            output_file.write(line + "\n")

        # Recursion for directories
        if os.path.isdir(full_path):
            extension = "    " if is_last else "│   "
            generate_tree(full_path, prefix + extension, output_file)

def main():
    print("--- Project Structure Mapper ---")
    print("Generates a text-based tree view of your project folders.")
    
    path_input = input("\nEnter project path (Press Enter for current folder): ").strip()
    
    # Default to current working directory if input is empty
    target_path = path_input if path_input else os.getcwd()

    if not os.path.exists(target_path):
        print(f"Error: Path '{target_path}' does not exist.")
        return

    file_name = "project_structure.txt"
    
    print(f"\nScanning: {target_path}")
    print(f"Generating: {file_name} ...\n")

    # Write output with UTF-8 encoding
    with open(file_name, "w", encoding="utf-8") as f:
        header = f"Project Structure: {os.path.basename(target_path)}/"
        print(header)
        f.write(header + "\n")
        
        generate_tree(target_path, "", f)

    print(f"\n[Success] Structure saved to '{file_name}'.")

if __name__ == "__main__":
    main()