import sys
import yaml
from deepdiff import DeepDiff
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def diff_yaml(file1, file2):
    yaml1 = load_yaml(file1)
    yaml2 = load_yaml(file2)

    diff = DeepDiff(yaml1, yaml2, ignore_order=True)
    return diff

def format_diff(diff):
    console = Console()

    for diff_type, changes in diff.items():
        console.print(f"[bold underline]{diff_type}:[/bold underline]")
        for key, change in changes.items():
            console.print(f"\n[bold]{key}:[/bold]")
            if isinstance(change, dict):
                old_value = change.get('old_value', '')
                new_value = change.get('new_value', '')
                diff_text = change.get('diff', '')

                # Convert non-string values to strings
                if not isinstance(old_value, str):
                    old_value = str(old_value)
                if not isinstance(new_value, str):
                    new_value = str(new_value)
                if not isinstance(diff_text, str):
                    diff_text = str(diff_text)

                if old_value:
                    console.print(Panel(Syntax(old_value, 'yaml', theme="monokai"), title="Old Value", border_style="red"))
                if new_value:
                    console.print(Panel(Syntax(new_value, 'yaml', theme="monokai"), title="New Value", border_style="green"))
                if diff_text:
                    console.print(Panel(Syntax(diff_text, 'diff', theme="monokai"), title="Diff", border_style="yellow"))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <file1.yaml> <file2.yaml>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    try:
        differences = diff_yaml(file1, file2)
        format_diff(differences)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)