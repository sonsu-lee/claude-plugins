# Research Plugin 하네스 설계 검증

> **Mode**: validate
> **Date**: 2026-03-29
> **Sources**: 22개 발견 → 16개 스크리닝 → 18개 포함 (2개 에이전트 병렬 수집)
> **Harness**: 자체 검증 (meta-analysis)

## Research Protocol

- **Core Question**: 현재 5-에이전트 7-단계 리서치 플러그인의 하네스 구조가 Anthropic/OpenAI 하네스 원칙에 부합하는가? 코딩 도메인에서 검증된 패턴이 리서치 워크플로우에도 적합한가?
- **Sub-questions**: Generator/Evaluator 분리 적합성, 에이전트 수 적정성, 평가 기준 구체성, 피드백 루프 설계, 컨텍스트 관리, 아키텍처 제약, 단순화 가능성
- **Inclusion**: Anthropic/OpenAI 공식 블로그 (2025-2026), arxiv 논문, Martin Fowler 분석, 플러그인 소스 코드
- **Exclusion**: 2024년 이전 문서, 단순 뉴스 요약, 마케팅 자료

## 결론: Partially Validated (부분 적합)

핵심 패턴(Generator/Evaluator 분리, 스프린트 계약)은 원칙에 부합하나, **3가지 영역에서 조정이 필요**하고 **단순화 가능성**이 확인됨.

## Validation Results

| 항목 | 현재 구현 | 권장 패턴 | 상태 | 증거 등급 |
|------|-----------|-----------|------|-----------|
| Generator/Evaluator 분리 | synthesizer(생성) ↔ evaluator(평가) 독립 에이전트 | "자체 평가 시 작업을 자신 있게 칭찬하는 경향" — 분리 필수 [^1] | ✅ ALIGNED | HIGH |
| 스프린트 계약 | 프로토콜 = "완료" 기준 사전 정의 | "코드 작성 전 '완료'의 정의에 합의" [^1] | ✅ ALIGNED | HIGH |
| 3-에이전트 코어 | 5개 에이전트 (planner, researcher, evaluator, synthesizer, evaluator) | 정규: Planner, Generator, Evaluator [^1] | ⚠️ PARTIAL | MODERATE |
| 컨텍스트 관리 | 에이전트 간 구조화된 핸드오프, 명시적 예산 없음 | "컨텍스트 사용률 40% 초과 시 성능 저하" [^5]; "구조화된 핸드오프와 컨텍스트 리셋" [^1] | ❌ GAP | MODERATE |
| 평가 기준 구체성 | Groundedness, Logical Validity, Protocol Completeness + CRAAP+, GRADE | 4개 구체적 평가 차원 (Design Quality, Originality, Craft, Functionality) [^1] | ✅ ALIGNED | HIGH |
| 피드백 루프 | 정적 재시도 (synthesis 3회, collection 2회) | "에이전트 실수 시 AGENTS.md 동적 업데이트" [^3] | ⚠️ PARTIAL | LOW |
| 아키텍처 제약 | 프롬프트 지침만으로 행동 제약 | "커스텀 린터 에러 = 에이전트 수정 지침" [^3] | ❌ GAP | LOW |
| 과잉 구조 리스크 | PRISMA + CRAAP+ + GRADE + meta-narrative 중첩 | "추가 프로세스 레이어가 벤치마크 실제 수용 기준과 괴리될 수 있음" [^6] | ⚠️ WARNING | MODERATE |
| 단순화 원칙 | 7단계, 5에이전트 | "가능한 가장 단순한 해결책, 필요할 때만 복잡도 증가" [^1] | ⚠️ NEEDS REVIEW | MODERATE |

## 핵심 발견사항

### 1. Generator/Evaluator 분리: 완전 부합 `[HIGH]`

Anthropic의 가장 핵심 원칙과 정확히 일치. "에이전트가 자신의 작업을 평가할 때 자신 있게 칭찬하는 경향이 있다" [^1] — 이 문제를 research-synthesizer(생성)와 research-evaluator(평가)의 독립 에이전트 분리로 정확히 해결.

### 2. 5-에이전트 구조: 정당한 도메인 분해 `[MODERATE]`

| 정규 역할 | 플러그인 에이전트 | 정당화 |
|-----------|------------------|--------|
| Planner | research-planner | 1:1 매핑 |
| Generator | doc-researcher + source-evaluator + research-synthesizer | 리서치 고유의 3단계: 수집 → 품질평가 → 종합 |
| Evaluator | research-evaluator | 1:1 매핑 |

코딩에서는 "코드 생성"이 하나의 행위지만, 리서치에서는 "소스 수집 → 소스 품질 평가 → 종합"이 본질적으로 다른 작업. 단, Anthropic도 "단일 범용 에이전트가 최선인지, 멀티 에이전트가 나은지 아직 불명확" [^2]이라고 인정.

### 3. 컨텍스트 관리: 가장 큰 갭 `[MODERATE]`

학술 연구에 따르면 "컨텍스트 사용률 40% 초과 시 성능 저하" [^5]. 현재 플러그인에는:
- 에이전트 간 핸드오프 시 컨텍스트 크기 측정/모니터링 없음
- 수집 결과가 많을 때 synthesizer에게 전달되는 양 제어 없음
- 요약/압축 메커니즘 없음

**권장**: 에이전트 간 핸드오프 시 구조화된 요약(adapter) 도입 검토

### 4. 과잉 구조 리스크: 주의 필요 `[MODERATE]`

NLAH 논문의 경고: "추가 프로세스 레이어가 국소적으로 구조화되고 설득력 있어 보이면서 실제 벤치마크 수용 기준과 괴리될 수 있다" [^6]

PRISMA + CRAAP+ + GRADE + meta-narrative — 각각은 의미 있지만 중첩 시:
- 모델이 방법론 준수에 컨텍스트/주의력을 소비
- 실질적 인사이트보다 형식적 완성에 집중할 위험

**평가**: 현재 모델 수준에서는 구체적 평가 기준이 추상적 "품질" 평가보다 나음. 하지만 Anthropic 원칙대로 "하네스 공간은 모델 개선으로 축소되지 않고 이동할 뿐" [^1] — 모델 업그레이드 시 재검토 필요.

## 단순화 분석

**현재 7단계 → 최소 4단계로 축소 가능**:

| 현재 단계 | 병합 가능? | 이유 |
|-----------|-----------|------|
| 1. Protocol | ❌ 유지 | 스프린트 계약; 모든 작업에 선행 필수 [^1] |
| 2. Collection | ✅ 2+3+4 병합 | 수집, 품질 평가, 커버리지 보정은 하나의 수집 에이전트 내부 로직으로 |
| 3. Quality Eval | ✅ 위와 병합 | 수집 중 인라인 평가가 별도 패스보다 효율적 |
| 4. Coverage Correction | ✅ 위와 병합 | 수집 에이전트의 재시도 로직으로 흡수 |
| 5. Synthesis | ✅ 5+7 병합 | 문서 생성은 종합의 마지막 단계 |
| 6. Harness Verification | ❌ 유지 | 핵심 evaluator; generator와 반드시 분리 [^1] |
| 7. Doc Generation | ✅ 위와 병합 | 출력 포맷팅은 종합의 일부 |

**최소 구성**: 4단계 (Protocol → Collection+Eval+Correction → Synthesis+Doc → Verification), 3에이전트 (Planner, Generator, Evaluator)

## 의견 갈림점

### 멀티 에이전트 vs. 단일 에이전트

| OpenAI 입장 | Anthropic 입장 |
|-------------|---------------|
| "환경, 피드백 루프, 제어 시스템 설계가 가장 어려운 과제" [^3] — 멀티 에이전트 오케스트레이션의 가치 인정 | "단일 범용 에이전트가 최선인지 멀티 에이전트가 나은지 불명확" [^2] |
| **맥락**: 1M 라인, 5개월 규모 프로덕션 | **맥락**: 연구/실험 환경 |

> **Meta-narrative**: 시간/능력 갭을 반영한 의견 차이. OpenAI는 현 세대 모델에서의 프로덕션 경험, Anthropic은 미래 모델 능력까지 고려한 전향적 시각. 리서치 플러그인의 경우, 2026년 현재 모델에서는 5에이전트가 유효하나, 모델 업그레이드 시 주기적으로 재평가해야 함.

### 구조 = 품질 향상 vs. 구조 = 거짓 엄밀성

| 구조가 돕는다 | 구조가 해칠 수 있다 |
|--------------|------------------|
| Anthropic: 4개 구체적 평가 차원 + 전담 evaluator [^1] | "추가 프로세스 레이어가 구조화되어 보이지만 실제 수용 기준과 괴리 가능" [^6] |
| **전제**: 구조가 솔루션 공간을 생산적으로 제약 | **전제**: 구조가 오도하는 방식으로 제약할 수 있음 |

> **Meta-narrative**: 정밀도-재현율 트레이드오프. PRISMA/CRAAP+/GRADE는 정밀도를 높이지만, 재현율(실질적 인사이트 발견)을 낮출 수 있음. **핵심 판단 기준**: 방법론적으로 건전하고 동시에 실질적으로 유용하면 정당화됨. 방법론적으로 완벽하지만 내용이 공허하면 해로움.

## Evidence Gap Map

충분한 근거를 찾지 못한 영역:

- [ ] **3-에이전트 vs 5-에이전트 리서치 하네스 직접 비교 실험 데이터**: 이론적 분석만 존재, 실증 비교 없음
- [ ] **OpenAI 1차 소스**: openai.com 403 차단으로 2차 출처(InfoQ, Martin Fowler)에 의존
- [ ] **리서치 도메인 비용-편익 분석**: Anthropic의 $200 vs $9 비교는 프론트엔드 개발 기준. 리서치 하네스의 비용 데이터 없음
- [ ] **CRAAP+/GRADE의 AI 에이전트 컨텍스트 실증 효과**: 인간 리서치 방법론을 AI에 적용한 것의 실제 효과 미검증
- [ ] **컨텍스트 사용률 측정**: 현재 플러그인의 실제 컨텍스트 사용 패턴 미측정

**권장 후속 연구**: 동일 리서치 질문을 (1) 현재 7단계 5에이전트, (2) 축소 4단계 3에이전트, (3) 단일 에이전트로 실행하여 품질 비교

## 최종 권장사항

### 즉시 조치 (Quick Wins)
1. **Steps 2+3+4 병합 검토**: doc-researcher에 CRAAP+ 인라인 평가 + 자동 재검색 로직 통합
2. **Steps 5+7 병합 검토**: synthesizer가 최종 문서 포맷까지 담당

### 중기 개선
3. **컨텍스트 예산 관리** 추가: 에이전트 간 핸드오프 시 구조화된 요약 메커니즘
4. **하네스 실패 로깅**: 평가 실패 패턴을 기록하여 프롬프트 개선에 반영 (OpenAI의 동적 AGENTS.md 피드백 원칙)

### 장기 모니터링
5. **모델 업그레이드 시 하네스 재검증**: "하네스 공간은 축소되지 않고 이동할 뿐" [^1] — Opus 5 등 차세대 모델에서 에이전트 수/단계 수 재평가

## Research Metrics

| Metric | Value |
|--------|-------|
| Total sources found | 22 |
| Sources included | 18 |
| Validation items assessed | 9 |
| Items aligned | 3 (33%) |
| Items with gaps | 3 (33%) |
| Items needing review | 3 (33%) |
| Evidence grade distribution | HIGH: 3, MODERATE: 4, LOW: 2 |

## 출처

[^1]: [Anthropic - Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) — "agents tend to confidently praise their own work"; "separating evaluation from generation proves more tractable"; "find the simplest solution possible, only increase complexity when needed"; "not every component in a harness encodes a necessary assumption"

[^2]: [Anthropic - Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — "It's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture"; "A future direction is to generalize these findings to other fields"

[^3]: OpenAI - Harness Engineering (via [InfoQ](https://www.infoq.com/news/2026/02/openai-harness-engineering-codex/), [goddaehee](https://goddaehee.tistory.com/565)) — "Humans steer, agents execute"; AGENTS.md 100줄 이내; "에이전트 실수 시 AGENTS.md 동적 업데이트"; "환경, 피드백 루프, 제어 시스템 설계가 가장 어려운 과제"

[^4]: [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) — Three harness categories: Context Engineering, Architectural Constraints, Entropy Management

[^5]: Alex Lavaee Blog / Academic sources — "Performance degrades beyond ~40% context utilization"; "Better models make harness engineering more important, not less"

[^6]: [arxiv 2603.25723 - Natural-Language Agent Harnesses](https://arxiv.org/html/2603.25723) — "Extra process layers can make a run more structured and locally convincing while still diverging from the benchmark's actual acceptance object"; NLAH framework: Contracts, Roles, Stage structure, Adapters, State semantics, Failure taxonomy

[^7]: [goddaehee.tistory.com/565](https://goddaehee.tistory.com/565) — "하네스는 LLM의 능력을 특정 작업에 맞게 제어하고 방향을 설정하는 도구, 추상화, 내부 구조의 총합"; OpenAI vs Anthropic 비교 분석; 7가지 실전 원칙
