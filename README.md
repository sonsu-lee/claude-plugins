# Claude Plugins

Claude Code 플러그인 마켓플레이스.

## Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [research](./research) | 체계적 기술 리서치 (출처 검증, CRAAP 품질 평가, 하네스 기반 QA) | 0.1.0 |

## Setup

```bash
# 마켓플레이스 등록
claude marketplace add ~/dev/personal/claude-plugins

# 플러그인 설치
claude plugin install research
```

## Structure

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json    # 마켓플레이스 메타데이터 + 플러그인 레지스트리
└── <plugin-name>/          # 각 플러그인 디렉토리
    ├── .claude-plugin/
    │   └── plugin.json
    ├── commands/
    ├── skills/
    ├── agents/
    ├── hooks/
    ├── .mcp.json
    └── README.md
```

## Adding a New Plugin

1. 플러그인 디렉토리 생성 (`<plugin-name>/`)
2. `.claude-plugin/plugin.json` 작성
3. 필요한 컴포넌트 추가 (commands, skills, agents, hooks, .mcp.json)
4. 루트 `marketplace.json`의 `plugins` 배열에 등록
