# Claude Plugins

Personal Claude Code plugin marketplace — frontend development and governance workflows.

## Structure

- **`/plugins`** - All plugins in this marketplace

## Plugins

| Plugin | Description | Category |
|--------|-------------|----------|
| [frontend](./plugins/frontend) | CSS debugging with live DOM inspection, design system token compliance, and component architecture guidance | development |
| [governance](./plugins/governance) | Orchestration runbooks, security risk gates, and SOP policy enforcement | productivity |

## Installation

To install, run `/plugin install {plugin-name}@claude-plugins`

or browse for the plugin in `/plugin > Discover`

## Plugin Structure

Each plugin follows the standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── commands/            # Slash commands (optional)
├── agents/              # Agent definitions (optional)
├── skills/              # Skill definitions (optional)
└── README.md            # Documentation
```
