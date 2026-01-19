# Claude Code Plugins

A collection of plugins for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Available Plugins

| Plugin | Description |
|--------|-------------|
| [frontend-conventions](./frontend-conventions) | React/TypeScript/CSS frontend development conventions |

## Installation

### From GitHub

```bash
claude /install-plugin https://github.com/sonsu/claude-plugins/tree/main/[plugin-name]
```

### Local Development

```bash
claude --plugin-dir /path/to/plugin
```

## Plugin Structure

Each plugin follows the standard Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin manifest
├── skills/              # Auto-activating knowledge
├── agents/              # Specialized subagents
├── commands/            # Slash commands
└── README.md            # Plugin documentation
```

## Contributing

1. Fork this repository
2. Create a new plugin directory
3. Follow the [plugin development guide](https://docs.anthropic.com/en/docs/claude-code/plugins)
4. Submit a pull request

## License

MIT
