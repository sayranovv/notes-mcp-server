from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime
from pathlib import Path
import re

mcp = FastMCP("Notes Manager")

NOTES_DIR = os.path.join(os.path.dirname(__file__), "notes")

def ensure_notes_dir():
    """Creates the notes directory if it does not exist"""
    Path(NOTES_DIR).mkdir(exist_ok=True)

def sanitize_filename(title: str) -> str:
    """Converts a note title into a safe filename"""
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'\s+', '_', safe_title)
    return safe_title.lower()[:100]

@mcp.tool()
def create_note(title: str, content: str, tags: str = "") -> str:
    """
    Create a new Markdown note
    
    Args:
        title: Note title
        content: Note content
        tags: Optional comma-separated list of tags
    
    Returns:
        Confirmation message of note creation
    """
    ensure_notes_dir()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{sanitize_filename(title)}.md"
    filepath = os.path.join(NOTES_DIR, filename)
    
    note_content = f"# {title}\n\n"
    note_content += f"**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    if tags:
        note_content += f"**Tags:** {tags}\n"
    note_content += f"\n---\n\n{content}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(note_content)
    
    return f"Note '{title}' created: {filename}"

@mcp.tool()
def list_notes(tag: str = "") -> str:
    """
    Get a list of all notes
    
    Args:
        tag: Optional tag filter
    
    Returns:
        List of notes with titles and dates
    """
    ensure_notes_dir()
    
    notes = []
    for filename in sorted(os.listdir(NOTES_DIR), reverse=True):
        if filename.endswith('.md'):
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else filename
                
                if tag:
                    tags_match = re.search(r'\*\*Tags:\*\* (.+)$', content, re.MULTILINE)
                    if not tags_match or tag.lower() not in tags_match.group(1).lower():
                        continue
                
                date_match = re.search(r'\*\*Created:\*\* (.+)$', content, re.MULTILINE)
                date = date_match.group(1) if date_match else "Unknown"
                
                notes.append(f"- [{filename}] {title} (Created: {date})")
    
    if not notes:
        return "No notes found" + (f" with tag '{tag}'" if tag else "")
    
    return "\n".join(notes)

@mcp.tool()
def read_note(filename: str) -> str:
    """
    Read the contents of a note
    
    Args:
        filename: Note filename (with .md extension)
    
    Returns:
        Note content
    """
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, filename)
    
    if not os.path.exists(filepath):
        return f"Note '{filename}' not found"
    
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def search_notes(query: str) -> str:
    """
    Search for text within notes
    
    Args:
        query: Search query
    
    Returns:
        List of notes containing the query
    """
    ensure_notes_dir()
    
    results = []
    query_lower = query.lower()
    
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if query_lower in content.lower():
                    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                    title = title_match.group(1) if title_match else filename
                    
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if query_lower in line.lower():
                            context = line[:100] + "..." if len(line) > 100 else line
                            results.append(f"- [{filename}] {title}\n  → {context}")
                            break
    
    if not results:
        return f"No matches found for '{query}'"
    
    return "\n\n".join(results)

@mcp.tool()
def update_note(filename: str, content: str) -> str:
    """
    Update the content of an existing note
    
    Args:
        filename: Note filename
        content: New content (will be appended)
    
    Returns:
        Confirmation message of update
    """
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, filename)
    
    if not os.path.exists(filepath):
        return f"Note '{filename}' not found"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"\n\n**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{content}\n")
    
    return f"Note '{filename}' updated"

@mcp.tool()
def delete_note(filename: str) -> str:
    """
    Delete a note
    
    Args:
        filename: Note filename
    
    Returns:
        Confirmation message of deletion
    """
    ensure_notes_dir()
    filepath = os.path.join(NOTES_DIR, filename)
    
    if not os.path.exists(filepath):
        return f"Note '{filename}' not found"
    
    os.remove(filepath)
    return f"Note '{filename}' deleted"

@mcp.resource("notes://all")
def get_all_notes() -> str:
    """
    Retrieve all notes as a single resource
    
    Returns:
        Combined contents of all notes
    """
    ensure_notes_dir()
    
    all_content = []
    for filename in sorted(os.listdir(NOTES_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                all_content.append(f"## {filename}\n\n{f.read()}\n\n---\n")
    
    return "\n".join(all_content) if all_content else "No notes available"

@mcp.prompt()
def summarize_notes_prompt() -> str:
    """
    Create a summarization prompt for all notes
    
    Returns:
        A prompt containing all notes for analysis
    """
    ensure_notes_dir()
    
    all_notes = []
    for filename in sorted(os.listdir(NOTES_DIR)):
        if filename.endswith('.md'):
            filepath = os.path.join(NOTES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                all_notes.append(f.read())
    
    if not all_notes:
        return "No notes available for analysis"
    
    combined = "\n\n---\n\n".join(all_notes)
    
    return f"""Analyze the following notes and provide:
1. A brief summary of key topics
2. Repeated ideas or patterns
3. Important action items or tasks
4. Recommendations for organizing the notes

Notes:

{combined}
"""

if __name__ == "__main__":
    mcp.run()