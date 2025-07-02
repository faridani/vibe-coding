import os
from pathlib import Path
import datetime
import argparse
from typing import Set, TextIO

# Define constants for ignored directories and file extensions
IGNORED_DIRS: Set[str] = {
    'node_modules', '.git', 'dist', 'build', 'coverage', '__pycache__', '.pytest_cache', 'venv', 'env'
}

IGNORED_FILES: Set[str] = {
    'package-lock.json',
    'project_documentation.md'
}

IGNORED_FILE_EXTENSIONS: Set[str] = {
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',  # Images
    '.ttf', '.woff', '.woff2', '.eot',                # Fonts
    '.mp4', '.webm', '.ogg',                         # Media
    '.pdf', '.doc', '.docx',                         # Documents
    '.zip', '.tar', '.gz',                           # Archives
    '.pyc', '.pyo', '.pyd',                          # Compiled/Binary
    '.lock',
}

LANGUAGE_MAP: dict[str, str] = {
    '.py': 'python', '.js': 'javascript', '.jsx': 'jsx', '.ts': 'typescript', '.tsx': 'tsx',
    '.java': 'java', '.cpp': 'cpp', '.c': 'c', '.html': 'html', '.css': 'css', '.scss': 'scss',
    '.md': 'markdown', '.json': 'json', '.yaml': 'yaml', '.yml': 'yaml', '.sh': 'bash', '.sql': 'sql',
    '.rs': 'rust', '.go': 'go', '.rb': 'ruby', '.php': 'php'
}

def should_process_path(path: Path) -> bool:
    """Determine if a path should be processed based on ignore rules."""
    return (
        not path.name.startswith('.') and  # Ignore hidden files/directories
        path.name not in IGNORED_DIRS and  # Ignore specific directories
        path.suffix.lower() not in IGNORED_FILE_EXTENSIONS  and # Ignore specific file types
        path.name not in IGNORED_FILES
    )

def get_language_from_path(file_path: Path) -> str:
    """Get the syntax highlighting language for a file based on its extension."""
    return LANGUAGE_MAP.get(file_path.suffix.lower(), '')

def process_file(file_path: Path, output_file: TextIO, root_path: Path) -> None:
    """Read a file and append its content to the markdown output."""
    try:
        relative_path = file_path.relative_to(root_path)
        language = get_language_from_path(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        output_file.write(f"\nfile path: {relative_path}\n\n")
        output_file.write(f"```{language}\n{content}\n```")
    except UnicodeDecodeError:
        print(f"Skipping binary or non-readable file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_directory(dir_path: Path, output_file: TextIO, root_path: Path) -> None:
    """Recursively process a directory and write its content to the markdown output."""
    try:
        for entry in sorted(dir_path.iterdir()):
            if not should_process_path(entry):
                continue

            if entry.is_dir():
                process_directory(entry, output_file, root_path)
            elif entry.is_file():
                process_file(entry, output_file, root_path)
    except Exception as e:
        print(f"Error processing directory {dir_path}: {e}")

def generate_documentation(project_path: Path, output_file_path: Path) -> None:
    """Generate a markdown file documenting the content of a project folder."""
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"# Project Documentation\n\nGenerated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        process_directory(project_path, output_file, project_path)

    print(f"Documentation generated successfully at {output_file_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a markdown file documenting a project's file contents.")
    parser.add_argument("project_path", type=str, nargs="?", default=".", help="Path to the project folder (default: current directory).")
    parser.add_argument("output_file", type=str, nargs="?", default="project_documentation.md", help="Path to the output markdown file (default: project_documentation.md).")
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    output_file_path = Path(args.output_file).resolve()

    if not project_path.is_dir():
        print(f"Error: The provided project path '{project_path}' is not a valid directory.")
        return

    print(f"Starting documentation generation for: {project_path}")
    generate_documentation(project_path, output_file_path)

if __name__ == "__main__":
    main()
