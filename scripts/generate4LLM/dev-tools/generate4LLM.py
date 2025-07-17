#!/usr/bin/env python3
"""
Script to generate a markdown file with folder structure and file contents for LLM analysis.
This script is designed to be run from a subdirectory (e.g., 'dev-tools') and will
analyze the parent directory.

Usage: python dev-tools/generate4LLM.py
"""

import os
import sys
from pathlib import Path

# --- Configuration ---

# Configure which files to include in the markdown based on their name or extension.
include_files = [
    "main.py",
    "app.py",
    "requirements.txt",
    "README.md",
    "config.py",
    "utils.py",
    "models.py",
    "views.py",
    "routes.py",
    "*.js",
    "*.html",
    "*.css",
    "*.json",
    "*.yml",
    "*.yaml",
    "Dockerfile",
    "docker-compose.yml",
    ".env.example",
    "package.json",
    "tsconfig.json",
    "*.ts",
    "*.tsx",
    "*.jsx"
]

# Directories to exclude from the tree structure and file processing.
# The script will automatically add its own parent directory (e.g., 'dev-tools') to this set.
exclude_dirs = {
    "__pycache__",
    ".git",
    ".vscode",
    ".idea",
    "node_modules",
    ".next",
    "build",
    "dist",
    ".pytest_cache",
    ".coverage",
    "venv",
    "env",
    ".env",
    ".mypy_cache",
    ".DS_Store"
}

# Specific files to exclude from the tree and content processing.
exclude_files = {
    ".gitignore",
    ".env",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".DS_Store",
    "Thumbs.db",
    "*.log",
    "package-lock.json",
    "yarn.lock"
}

# --- Core Logic ---

def should_include_file(file_path):
    """Check if a file should be included based on include_files patterns."""
    file_name = os.path.basename(file_path)
    
    for pattern in include_files:
        if pattern.startswith("*"):
            # Handle wildcard patterns like "*.js"
            if file_name.endswith(pattern[1:]):
                return True
        else:
            # Handle exact matches
            if file_name == pattern:
                return True
    
    return False

def should_exclude(path_name, is_dir=False):
    """Check if a file or directory should be excluded."""
    if is_dir:
        return path_name in exclude_dirs
    else:
        return path_name in exclude_files

def generate_tree(directory, prefix="", max_depth=10, current_depth=0):
    """Generate ASCII tree structure of the directory, respecting exclusions."""
    if current_depth > max_depth:
        return ""
    
    tree_str = ""
    
    try:
        # Get all items in directory, filter out excluded ones
        items = [item for item in os.listdir(directory) if not should_exclude(item, os.path.isdir(os.path.join(directory, item)))]
        
        # Sort items: directories first, then files, alphabetically
        items.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x.lower()))
        
        for i, item in enumerate(items):
            is_last_item = i == len(items) - 1
            item_path = os.path.join(directory, item)
            is_dir = os.path.isdir(item_path)
            
            # Choose the appropriate tree symbols
            tree_symbol = "└── " if is_last_item else "├── "
            next_prefix = prefix + ("    " if is_last_item else "│   ")
            
            tree_str += f"{prefix}{tree_symbol}{item}\n"
            
            # Recursively process subdirectories
            if is_dir:
                tree_str += generate_tree(
                    item_path, 
                    next_prefix, 
                    max_depth, 
                    current_depth + 1
                )
    
    except PermissionError:
        tree_str += f"{prefix}[Permission Denied]\n"
    
    return tree_str

def read_file_content(file_path):
    """Read and return file content, handling different encodings."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error reading file: {e}]"

def find_files_to_process(root_dir):
    """Find all files that match the include patterns, respecting exclusions."""
    files_to_process = []
    
    for root, dirs, files in os.walk(root_dir, topdown=True):
        # Modify dirs in-place to prevent walking into excluded directories
        dirs[:] = [d for d in dirs if not should_exclude(d, True)]
        
        for file in files:
            if should_exclude(file, False):
                continue
                
            file_path = os.path.join(root, file)
            
            if should_include_file(file_path):
                # Store the relative path from the root_dir
                relative_path = os.path.relpath(file_path, root_dir)
                files_to_process.append(relative_path)
    
    return sorted(files_to_process)

def generate_markdown():
    """Generate the markdown file with folder structure and file contents."""
    # The script is in /dev-tools, so the root is its parent directory.
    script_path = Path(__file__).resolve()
    dev_tools_dir = script_path.parent
    root_dir = dev_tools_dir.parent
    
    # Add the script's own directory to the exclusion list
    exclude_dirs.add(dev_tools_dir.name)

    # The output file will be created in the root project directory.
    output_file_path = root_dir / "dev-tools/4LLM.md"
    
    print(f"Generating markdown for project at: {root_dir}")
    print(f"Output file will be: {output_file_path}")
    print(f"Ignoring directory: {dev_tools_dir.name}")
    
    # 1. Generate folder structure tree
    print("\nGenerating folder structure...")
    project_name = os.path.basename(root_dir)
    tree_structure = f"{project_name}\n"
    tree_structure += generate_tree(str(root_dir))
    
    # 2. Find all files to include
    print("Finding files to include...")
    files_to_process = find_files_to_process(str(root_dir))
    
    if not files_to_process:
        print("Warning: No files found to include based on the specified patterns.")
    else:
        print(f"Found {len(files_to_process)} files to include:")
        for file in files_to_process:
            print(f"  - {file}")
    
    # 3. Generate the full markdown content
    print("\nGenerating markdown content...")
    markdown_content = f"# Project: {project_name}\n\n"
    markdown_content += "## Project Structure\n\n"
    markdown_content += "```\n"
    markdown_content += tree_structure
    markdown_content += "```\n\n"
    
    markdown_content += "--- \n\n"
    markdown_content += "## File Contents\n\n"
    
    for relative_path in files_to_process:
        full_path = root_dir / relative_path
        
        # Use forward slashes for consistency in the output
        display_path = str(Path(relative_path).as_posix())
        
        markdown_content += f"### `FILE: {display_path}`\n\n"
        
        # Determine file extension for syntax highlighting
        language = os.path.splitext(display_path)[1].lstrip('.')
        
        file_content = read_file_content(full_path)
        
        markdown_content += f"```{language}\n"
        markdown_content += file_content
        markdown_content += "\n```\n\n"
    
    # 4. Write the content to the markdown file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Successfully generated {output_file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to run the script."""
    print("Starting 4LLM markdown generation...")
    print("=" * 50)
    
    try:
        generate_markdown()
        print("=" * 50)
        print("Generation complete!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

