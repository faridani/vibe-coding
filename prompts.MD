Write a Python script that can take a large project folder and produce a markdown file with the content of each file. Before each file it should place the location of the file. For example it should have 
/frontend/src/components/nodepanel.jsx 
And then the content of the file. It should have an ignore list for folders and filetypes. Also it has to be able to ingore individual files so to this, please add a list for IGNORED_FILES. Use the following script as a refrence and improve it and make it elegant. Try to comment the code as much as possible. 

#!/usr/bin/env python3
import os
from pathlib import Path
import datetime
import argparse
from typing import TextIO, Set

# Configure which files and directories to ignore
IGNORED_DIRS: Set[str] = {
    'node_modules',
    '.git',
    'dist',
    'build',
    'coverage',
    '__pycache__',
    '.pytest_cache',
    'venv',
    'env'
}

IGNORED_FILE_EXTENSIONS: Set[str] = {
    # Images
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    # Fonts
    '.ttf', '.woff', '.woff2', '.eot',
    # Media
    '.mp4', '.webm', '.ogg',
    # Documents
    '.pdf', '.doc', '.docx',
    # Archives
    '.zip', '.tar', '.gz',
    # Binary/Compiled
    '.pyc', '.pyo', '.pyd',
}

# Language mapping for syntax highlighting
LANGUAGE_MAP: dict[str, str] = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.md': 'markdown',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.sh': 'bash',
    '.bash': 'bash',
    '.sql': 'sql',
    '.rs': 'rust',
    '.go': 'go',
    '.rb': 'ruby',
    '.php': 'php',
}

def should_process_path(path: Path) -> bool:
    """
    Determine if a path should be processed based on ignore rules.
    """
    # Check if it's an ignored directory
    if path.name in IGNORED_DIRS:
        return False
    
    # Check if it's a hidden file/directory
    if path.name.startswith('.'):
        return False
    
    # Check file extension
    if path.suffix.lower() in IGNORED_FILE_EXTENSIONS:
        return False
    
    return True

def get_language_from_path(file_path: Path) -> str:
    """
    Determine the language for syntax highlighting based on file extension.
    """
    return LANGUAGE_MAP.get(file_path.suffix.lower(), '')

def process_file(file_path: Path, output_file: TextIO, root_path: Path) -> None:
    """
    Process a single file and write its content to the markdown document.
    """
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get relative path for display
        relative_path = file_path.relative_to(root_path)
        
        # Write file path and content to markdown
        output_file.write(f'\n## {relative_path}\n\n')
        
        # Get language for syntax highlighting
        language = get_language_from_path(file_path)
        output_file.write(f'```{language}\n')
        output_file.write(content)
        
        # Ensure there's a newline at the end of the content
        if not content.endswith('\n'):
            output_file.write('\n')
        
        output_file.write('```\n\n')
        
    except UnicodeDecodeError:
        print(f"Warning: Skipping binary file {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")

def process_directory(dir_path: Path, output_file: TextIO, root_path: Path) -> None:
    """
    Recursively process a directory and all its subdirectories.
    """
    try:
        # Sort entries for consistent output
        entries = sorted(dir_path.iterdir())
        
        for entry in entries:
            if not should_process_path(entry):
                continue
            
            if entry.is_dir():
                process_directory(entry, output_file, root_path)
            elif entry.is_file():
                process_file(entry, output_file, root_path)
                
    except Exception as e:
        print(f"Error processing directory {dir_path}: {str(e)}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate markdown documentation for a project')
    parser.add_argument('project_path', nargs='?', default='.',
                      help='Path to the project directory (default: current directory)')
    parser.add_argument('output_file', nargs='?', default='project-documentation.md',
                      help='Output markdown file (default: project-documentation.md)')
    
    args = parser.parse_args()
    
    # Convert to Path objects
    project_path = Path(args.project_path).resolve()
    output_path = Path(args.output_file)
    
    print(f"Generating documentation for: {project_path}")
    print(f"Output will be saved to: {output_path}")
    
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            # Write header
            output_file.write('# Project Documentation\n\n')
            output_file.write(f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
            
            # Process the project directory
            process_directory(project_path, output_file, project_path)
            
        print('Documentation generated successfully!')
        
    except Exception as e:
        print(f"Error generating documentation: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()
