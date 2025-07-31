# Taskmaster AI (Astrotask) MCP Server Setup

Taskmaster AI is a Model Context Protocol (MCP) server that provides comprehensive task management capabilities for AI agents like Cline.

## Overview

The `@astrotask/mcp` package implements an MCP server that exposes task management tools to AI agents, allowing them to:
- Create and manage tasks with hierarchies
- Track task dependencies
- Update task statuses
- Add context information to tasks
- Query and filter tasks

## Setup Instructions

### 1. Configure MCP Server in Cline

To use Taskmaster AI with Cline, you need to add it to your MCP server configuration:

1. Open Cline Settings in VSCode
2. Navigate to the MCP Servers section
3. Add a new server configuration:

```json
{
  "astrotask": {
    "command": "npx",
    "args": ["@astrotask/mcp"],
    "env": {
      "DATABASE_URI": "./data/astrotask.db",
      "LOG_LEVEL": "info"
    }
  }
}
```

### 2. Alternative: Manual Configuration

You can also manually edit your MCP configuration file:

**Location:** `~/.config/Code/User/globalStorage/cline/settings/cline_mcp_settings.json`

Add the Astrotask configuration to the `mcpServers` object.

## Available Tools

Once configured, Cline will have access to these task management tools:

### 1. `getNextTask`
Get the next available task to work on based on priority and status.

### 2. `addTasks`
Create multiple tasks with hierarchies and dependencies in a single operation.

### 3. `listTasks`
List tasks with optional filtering by:
- Status (pending, in-progress, done, cancelled)
- Parent task ID
- Include/exclude subtasks

### 4. `addTaskContext`
Add context information to existing tasks for better AI understanding.

### 5. `addDependency`
Create dependency relationships between tasks.

### 6. `updateStatus`
Update task status (pending, in-progress, done, etc.).

## Example Usage

Once configured, you can ask Cline to:

- "Create a task to implement user authentication"
- "List all pending tasks"
- "Mark task A as complete"
- "Add a subtask for database migration under task B"
- "Show me the next high-priority task to work on"

## Database Location

By default, tasks are stored in:
- `./data/astrotask.db` (SQLite database)

You can change this location by modifying the `DATABASE_URI` environment variable in the configuration.

## Configuration Options

### Environment Variables

- `DATABASE_URI`: Path to the SQLite database file
- `LOG_LEVEL`: Logging level (debug, info, warn, error)
- `DB_VERBOSE`: Enable verbose database logging (true/false)
- `DATABASE_ENCRYPTED`: Enable database encryption
- `DATABASE_KEY`: Encryption key for database

## Troubleshooting

### Server Not Starting
1. Check that npx is available in your PATH
2. Verify the database path is writable
3. Check Cline's MCP server logs for errors

### Tasks Not Persisting
1. Ensure the database file path is correct
2. Check file permissions on the database directory
3. Verify no other process is locking the database

### Connection Issues
1. Restart VSCode after configuration changes
2. Check that the MCP server is running (visible in Cline's status)
3. Review logs for any error messages

## Benefits

- **Persistent Task Management**: Tasks are stored in a local database
- **Hierarchical Organization**: Support for subtasks and complex task relationships
- **AI-Optimized**: Designed specifically for AI agent interaction
- **Type-Safe**: Full input validation and type checking
- **Real-time Updates**: Immediate feedback on task operations

## Next Steps

1. Configure the MCP server in Cline
2. Test by asking Cline to create a sample task
3. Use task management for your project workflow
4. Integrate task tracking into your development process

Now you can use natural language to manage your project tasks through Cline!
