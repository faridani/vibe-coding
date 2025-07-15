#!/usr/bin/env python3
"""
Script to generate a markdown file with folder structure and file contents for LLM analysis.
Usage: python generate4LLM.py
"""



import os
import sys
from pathlib import Path

# Configure which files to include in the markdown
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

# Files and directories to exclude from tree structure
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
    "package.old.json",
    "stockfish.js"
}

def should_include_file(file_path):
    """Check if a file should be included based on include_files patterns."""
    file_name = os.path.basename(file_path)
    
    for pattern in include_files:
        if pattern.startswith("*"):
            # Handle wildcard patterns like "*.js"
            extension = pattern[1:]  # Remove the *
            if file_name.endswith(extension):
                return True
        else:
            # Handle exact matches
            if file_name == pattern:
                return True
    
    return False

def should_exclude_from_tree(name, is_dir=False):
    """Check if a file or directory should be excluded from the tree."""
    if is_dir:
        return name in exclude_dirs
    else:
        return name in exclude_files or name.startswith('.')

def generate_tree(directory, prefix="", is_last=True, max_depth=10, current_depth=0):
    """Generate ASCII tree structure of the directory."""
    if current_depth > max_depth:
        return ""
    
    tree_str = ""
    
    try:
        # Get all items in directory
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            is_dir = os.path.isdir(item_path)
            
            # Skip excluded items
            if should_exclude_from_tree(item, is_dir):
                continue
                
            items.append((item, is_dir, item_path))
        
        # Sort items: directories first, then files
        items.sort(key=lambda x: (not x[1], x[0].lower()))
        
        for i, (item, is_dir, item_path) in enumerate(items):
            is_last_item = i == len(items) - 1
            
            # Choose the appropriate tree symbols
            if is_last_item:
                tree_symbol = "└── "
                next_prefix = prefix + "    "
            else:
                tree_symbol = "├── "
                next_prefix = prefix + "│   "
            
            tree_str += f"{prefix}{tree_symbol}{item}\n"
            
            # Recursively process subdirectories
            if is_dir:
                tree_str += generate_tree(
                    item_path, 
                    next_prefix, 
                    is_last_item, 
                    max_depth, 
                    current_depth + 1
                )
    
    except PermissionError:
        tree_str += f"{prefix}[Permission Denied]\n"
    
    return tree_str

def read_file_content(file_path):
    """Read and return file content, handling different encodings."""
    try:
        # Try UTF-8 first
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            # Try latin-1 as fallback
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            return f"[Error reading file: {e}]"
    except Exception as e:
        return f"[Error reading file: {e}]"

def find_files_to_include(root_dir):
    """Find all files that match the include patterns."""
    files_to_include = []
    
    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from dirs list to prevent walking into them
        dirs[:] = [d for d in dirs if not should_exclude_from_tree(d, True)]
        
        for file in files:
            if should_exclude_from_tree(file, False):
                continue
                
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)
            
            if should_include_file(file_path):
                files_to_include.append(relative_path)
    
    return sorted(files_to_include)

def generate_markdown():
    """Generate the markdown file with folder structure and file contents."""
    root_dir = os.getcwd()
    output_file = "4LLM.md"
    
    print(f"Generating markdown file: {output_file}")
    print(f"Root directory: {root_dir}")
    
    # Generate folder structure
    print("Generating folder structure...")
    folder_name = os.path.basename(root_dir)
    tree_structure = f"{folder_name}\n"
    tree_structure += generate_tree(root_dir)
    
    # Find files to include
    print("Finding files to include...")
    files_to_include = find_files_to_include(root_dir)
    
    print(f"Found {len(files_to_include)} files to include:")
    for file in files_to_include:
        print(f"  - {file}")
    
    # Generate markdown content
    print("Generating markdown content...")
    markdown_content = "# Project Structure and Files\n\n"
    markdown_content += "My folder structure is as below:\n\n"
    markdown_content += "```\n"
    markdown_content += tree_structure
    markdown_content += "```\n\n"
    
    # Add file contents
    markdown_content += "## File Contents\n\n"
    
    for file_path in files_to_include:
        full_path = os.path.join(root_dir, file_path)
        
        # Use forward slashes for consistency
        display_path = file_path.replace("\\", "/")
        
        markdown_content += f"## FILE: {display_path}\n\n"
        
        # Determine file extension for syntax highlighting
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Map extensions to markdown code block languages
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.sh': 'bash',
            '.sql': 'sql',
            '.xml': 'xml',
            '.dockerfile': 'dockerfile'
        }
        
        language = language_map.get(file_extension, '')
        
        file_content = read_file_content(full_path)
        
        markdown_content += f"```{language}\n"
        markdown_content += file_content
        markdown_content += "\n```\n\n"
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Successfully generated {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")
        sys.exit(1)

def main():
    """Main function."""
    print("Starting 4LLM markdown generation...")
    print("=" * 50)
    
    try:
        generate_markdown()
        print("=" * 50)
        print("Generation complete!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
