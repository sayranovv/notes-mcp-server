# 📝 Notes MCP Server

A Model Context Protocol (MCP) server for managing notes in Markdown format. Built with Python and the FastMCP SDK.

<a href="https://glama.ai/mcp/servers/@sayranovv/notes-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@sayranovv/notes-mcp-server/badge" alt="Notes Server MCP server" />
</a>

## 🌟 Features

- **Create Notes**: Create new Markdown notes with titles, content, and tags
- **List & Filter**: View all notes or filter by specific tags
- **Search**: Full-text search across all notes with context preview
- **Update**: Append content to existing notes with timestamps
- **Delete**: Remove notes when no longer needed
- **Resources**: Access all notes as a single MCP resource
- **AI Prompts**: Built-in prompt for analyzing and summarizing notes

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Install uv

```bash
# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### Install Dependencies

```bash
# Using uv (recommended)
uv pip install mcp

# Or using pip
pip install mcp
```

## 🚀 Quick Start

### 1. Save the Server

Save `notes_server.py` in your desired directory.

### 2. Run the Server

```bash
# Using uv (recommended)
uv run notes_server.py

# Or using python directly
python notes_server.py
```

### 3. Configure in Claude Desktop

Add to your `claude_desktop_config.json`:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "notes": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/notes-mcp-server",
        "run",
        "notes_server.py"
      ]
    }
  }
}
```

**Alternative with Python:**
```json
{
  "mcpServers": {
    "notes": {
      "command": "python",
      "args": ["/absolute/path/to/notes_server.py"]
    }
  }
}
```

### 4. Restart Claude Desktop

After adding the configuration, restart Claude Desktop to load the MCP server.

## 🛠️ Available Tools

### `create_note`
Create a new note with title, content, and optional tags.

**Parameters:**
- `title` (string): Note title
- `content` (string): Note content in Markdown
- `tags` (string, optional): Comma-separated tags

**Example:**
```
Create a note titled "Project Ideas" with content "1. Build MCP server\n2. Add search" and tags "work, ideas"
```

### `list_notes`
List all notes with their titles and creation dates.

**Parameters:**
- `tag` (string, optional): Filter by specific tag

**Example:**
```
List all notes
List notes with tag "work"
```

### `read_note`
Read the full content of a specific note.

**Parameters:**
- `filename` (string): The filename of the note (e.g., `20241106_120000_project_ideas.md`)

**Example:**
```
Read note "20241106_120000_project_ideas.md"
```

### `search_notes`
Search for notes containing specific text.

**Parameters:**
- `query` (string): Search query

**Example:**
```
Search notes for "Python"
```

### `update_note`
Append content to an existing note with timestamp.

**Parameters:**
- `filename` (string): The filename of the note
- `content` (string): Content to append

**Example:**
```
Update note "20241106_120000_project_ideas.md" with "3. Implement testing"
```

### `delete_note`
Delete a note permanently.

**Parameters:**
- `filename` (string): The filename of the note

**Example:**
```
Delete note "20241106_120000_old_note.md"
```

## 📚 Resources

### `notes://all`
Access all notes as a combined resource. Useful for context-aware operations.

## 💡 Prompts

### `summarize_notes_prompt`
Generates a prompt for AI to analyze all notes and provide:
1. Summary of main themes
2. Recurring ideas or patterns
3. Important action items
4. Recommendations for organization

## 📁 File Structure

Notes are stored in the `notes/` directory with the following format:

```
notes/
├── 20241106_120000_project_ideas.md
├── 20241106_130000_shopping_list.md
└── 20241106_140000_python_notes.md
```

### Note Format

Each note is a Markdown file with metadata:

```markdown
# Project Ideas

**Created:** 2024-11-06 12:00:00
**Tags:** work, ideas

---

1. Build MCP server
2. Add search functionality
3. Implement testing
```

## 🧪 Testing

A test script is included to verify functionality without connecting to an LLM:

```bash
python test_notes_server.py
```

The test script will:
- Create sample notes
- List and filter notes
- Search for content
- Update and delete notes
- Test all features

## 🔧 Configuration

### Notes Directory

By default, notes are stored in `./notes/`. To change the location, modify the `NOTES_DIR` variable in `notes_server.py`:

```python
NOTES_DIR = os.path.join(os.path.dirname(__file__), "notes")
```

### Filename Generation

Notes are saved with timestamps and sanitized titles:
- Format: `YYYYMMDD_HHMMSS_sanitized_title.md`
- Max title length: 100 characters
- Special characters are removed
- Spaces converted to underscores

## 📝 Usage Examples

### Create a Note
```
"Create a note titled 'Meeting Notes' with content 'Discussed Q4 goals' and tags 'work, meetings'"
```

### Find Related Notes
```
"Search my notes for anything related to 'Python'"
```

### Review Notes by Category
```
"List all notes tagged with 'personal'"
```

### Summarize Notes
```
"Use the summarize_notes_prompt to analyze all my notes"
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop](https://claude.ai/download)

## ⚠️ Limitations

- Text-based notes only (no file attachments)
- No note encryption
- Single notes directory (no subdirectories)
- UTF-8 encoding only

## 💬 Support

For issues or questions:
1. Check the test script output for debugging
2. Review the notes directory permissions
3. Ensure Python 3.10+ is installed
4. Verify MCP SDK installation

---

Made with ❤️ using [FastMCP](https://github.com/modelcontextprotocol/python-sdk)