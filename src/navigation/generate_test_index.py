#!/usr/bin/env python3
"""Generate TEST_INDEX.md with links to all test files.

Scans the tests directory and creates a markdown index with:
- Organized sections for smoke, endpoints, and scenarios
- Links to each test file
- Brief descriptions from module docstrings
"""
import os
import sys
from pathlib import Path


def get_module_docstring(file_path: str) -> str:
    """Extract module-level docstring from a Python file.
    
    Args:
        file_path: Path to Python file.
    
    Returns:
        First line of module docstring, or filename if no docstring.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        # Look for docstring in first few lines
        in_docstring = False
        docstring_lines = []
        
        for line in lines[:20]:  # Check first 20 lines
            stripped = line.strip()
            
            # Skip empty lines and comments before docstring
            if not in_docstring and (not stripped or stripped.startswith('#')):
                continue
            
            # Start of docstring
            if not in_docstring and (stripped.startswith('"""') or stripped.startswith("'''")):
                in_docstring = True
                # Extract text after opening quotes
                content = stripped[3:]
                if content.endswith('"""') or content.endswith("'''"):
                    # Single-line docstring
                    return content[:-3].strip()
                if content:
                    docstring_lines.append(content)
                continue
            
            # End of docstring
            if in_docstring and (stripped.endswith('"""') or stripped.endswith("'''")):
                # Extract text before closing quotes
                content = stripped[:-3].strip()
                if content:
                    docstring_lines.append(content)
                break
            
            # Inside docstring
            if in_docstring:
                docstring_lines.append(stripped)
        
        if docstring_lines:
            # Return first non-empty line
            for line in docstring_lines:
                if line.strip():
                    return line.strip()
        
        # Fallback to filename
        return Path(file_path).stem.replace('_', ' ').title()
    
    except Exception:
        return Path(file_path).stem.replace('_', ' ').title()


def scan_tests_directory(tests_dir: str) -> dict:
    """Scan tests directory and organize test files.
    
    Args:
        tests_dir: Path to tests directory.
    
    Returns:
        Dictionary organized by section (smoke, endpoints, scenarios).
    """
    tests_path = Path(tests_dir)
    
    result = {
        'smoke': [],
        'endpoints': {},
        'scenarios': []
    }
    
    # Scan smoke tests
    smoke_dir = tests_path / 'smoke'
    if smoke_dir.exists():
        for test_file in sorted(smoke_dir.glob('test_*.py')):
            rel_path = test_file.relative_to(tests_path.parent)
            description = get_module_docstring(str(test_file))
            result['smoke'].append({
                'path': str(rel_path),
                'name': test_file.stem,
                'description': description
            })
    
    # Scan endpoint tests
    endpoints_dir = tests_path / 'endpoints'
    if endpoints_dir.exists():
        for section_dir in sorted(endpoints_dir.iterdir()):
            if section_dir.is_dir() and not section_dir.name.startswith('__'):
                section_name = section_dir.name
                result['endpoints'][section_name] = []
                
                for test_file in sorted(section_dir.glob('test_*.py')):
                    rel_path = test_file.relative_to(tests_path.parent)
                    description = get_module_docstring(str(test_file))
                    result['endpoints'][section_name].append({
                        'path': str(rel_path),
                        'name': test_file.stem,
                        'description': description
                    })
    
    # Scan scenario tests
    scenarios_dir = tests_path / 'scenarios'
    if scenarios_dir.exists():
        for test_file in sorted(scenarios_dir.glob('test_*.py')):
            rel_path = test_file.relative_to(tests_path.parent)
            description = get_module_docstring(str(test_file))
            result['scenarios'].append({
                'path': str(rel_path),
                'name': test_file.stem,
                'description': description
            })
    
    return result


def generate_index_markdown(test_data: dict) -> str:
    """Generate markdown content for test index.
    
    Args:
        test_data: Dictionary of test files organized by section.
    
    Returns:
        Markdown content string.
    """
    lines = []
    
    # Header
    lines.append("# Test Index")
    lines.append("")
    lines.append("Auto-generated index of all test files in the GanttPRO API test suite.")
    lines.append("")
    lines.append("## Smoke Tests")
    lines.append("")
    
    if test_data['smoke']:
        for test in test_data['smoke']:
            lines.append(f"* [{test['name']}]({test['path']}) - {test['description']}")
    else:
        lines.append("* No smoke tests found")
    
    lines.append("")
    lines.append("## Endpoint Tests")
    lines.append("")
    
    if test_data['endpoints']:
        for section, tests in sorted(test_data['endpoints'].items()):
            lines.append(f"### {section.title()}")
            lines.append("")
            if tests:
                for test in tests:
                    lines.append(f"* [{test['name']}]({test['path']}) - {test['description']}")
            else:
                lines.append(f"* No tests in {section}")
            lines.append("")
    else:
        lines.append("* No endpoint tests found")
        lines.append("")
    
    lines.append("## Scenario Tests")
    lines.append("")
    
    if test_data['scenarios']:
        for test in test_data['scenarios']:
            lines.append(f"* [{test['name']}]({test['path']}) - {test['description']}")
    else:
        lines.append("* No scenario tests found")
    
    lines.append("")
    lines.append("*This index is automatically generated. Run `python src/navigation/generate_test_index.py` to update.*")
    lines.append("")
    
    return '\n'.join(lines)


def main():
    """Main function to generate test index."""
    # Determine project root (script is in src/navigation/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    tests_dir = project_root / 'tests'
    output_file = script_dir / 'TEST_INDEX.md'
    
    if not tests_dir.exists():
        print(f"Error: Tests directory not found at {tests_dir}")
        sys.exit(1)
    
    print(f"Scanning tests directory: {tests_dir}")
    test_data = scan_tests_directory(str(tests_dir))
    
    print("Generating index markdown...")
    markdown_content = generate_index_markdown(test_data)
    
    print(f"Writing index to: {output_file}")
    with open(output_file, 'w') as f:
        f.write(markdown_content)
    
    # Print summary
    total_tests = (
        len(test_data['smoke']) +
        sum(len(tests) for tests in test_data['endpoints'].values()) +
        len(test_data['scenarios'])
    )
    
    print(f"\nTest Index Generated Successfully!")
    print(f"Total test files indexed: {total_tests}")
    print(f"  - Smoke tests: {len(test_data['smoke'])}")
    print(f"  - Endpoint sections: {len(test_data['endpoints'])}")
    print(f"  - Scenario tests: {len(test_data['scenarios'])}")
    print(f"\nIndex saved to: {output_file}")


if __name__ == '__main__':
    main()
