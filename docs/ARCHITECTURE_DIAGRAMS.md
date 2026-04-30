# Harness Engineering - 架构可视化 📊

> **使用Mermaid图表直观展示系统架构**

---

## 1. 整体架构图

```mermaid
graph TB
    subgraph "用户层"
        A[用户输入需求]
    end
    
    subgraph "编排层 - harness.py"
        B[Harness Orchestrator]
        B1[Plan阶段]
        B2[Contract协商]
        B3[Build-Evaluate循环]
        B4[REFINE/PIVOT决策]
    end
    
    subgraph "Agent层 - agents.py"
        C1[Planner 🧠]
        C2[Builder 🔨]
        C3[Evaluator ✅]
        C4[ContractProposer 📝]
        C5[ContractReviewer 🔍]
    end
    
    subgraph "基础设施层"
        D1[Context Manager 🧠]
        D2[Tool Executor 🛠️]
        D3[Skill Registry 🎓]
        D4[Profile Config 🎭]
        D5[Middleware 🔧]
    end
    
    subgraph "外部服务"
        E1[LLM API<br/>OpenAI/OpenRouter/Ollama]
        E2[FileSystem]
        E3[Browser<br/>Playwright]
        E4[Shell]
    end
    
    A --> B
    B --> B1
    B --> B2
    B --> B3
    B --> B4
    
    B1 --> C1
    B2 --> C4
    B2 --> C5
    B3 --> C2
    B3 --> C3
    
    C1 --> D1
    C2 --> D1
    C2 --> D2
    C2 --> D3
    C3 --> D2
    C3 --> D5
    
    D2 --> E2
    D2 --> E3
    D2 --> E4
    
    C1 --> E1
    C2 --> E1
    C3 --> E1
    
    style B fill:#ff6b6b,stroke:#333,stroke-width:3px
    style C1 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style C2 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style C3 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style D1 fill:#96ceb4,stroke:#333,stroke-width:2px
    style D2 fill:#96ceb4,stroke:#333,stroke-width:2px
```

---

## 2. Agent执行流程图

```mermaid
sequenceDiagram
    participant U as User
    participant H as Harness
    participant P as Planner
    participant B as Builder
    participant E as Evaluator
    participant C as ContextMgr
    participant T as Tools
    participant L as LLM
    
    U->>H: 输入需求
    activate H
    
    H->>P: 生成规格
    activate P
    P->>L: 调用LLM
    L-->>P: 返回spec.md
    P-->>H: 规格文档
    deactivate P
    
    H->>B: 开始构建
    activate B
    
    loop 迭代循环 (max 50次)
        B->>C: 检查上下文
        activate C
        alt Token > 80K 或焦虑
            C->>C: 硬重置
        else Token > 50K
            C->>C: 压缩消息
        else
            C->>C: 保持现状
        end
        C-->>B: 更新后的messages
        deactivate C
        
        B->>L: 调用LLM
        activate L
        L-->>B: 响应(tool_calls或完成)
        deactivate L
        
        alt 有工具调用
            B->>T: 执行工具
            activate T
            T-->>B: 工具结果
            deactivate T
            B->>B: 添加工具结果到messages
        else 无工具调用
            B-->>H: 完成构建
            deactivate B
            
            H->>E: 评估质量
            activate E
            E->>L: 调用LLM评分
            L-->>E: 分数+反馈
            E-->>H: feedback.md + score
            deactivate E
            
            alt score >= 85
                H-->>U: ✅ 任务成功
                deactivate H
            else score < 85
                H->>H: REFINE或PIVOT决策
                H->>B: 新一轮迭代
                activate B
            end
        end
    end
```

---

## 3. Context管理策略

```mermaid
flowchart TD
    Start[开始迭代] --> Count[计算Token数量]
    Count --> Check1{Token > 80K?}
    
    Check1 -->|是| Anxiety[检测焦虑信号]
    Check1 -->|否| Check2{Token > 50K?}
    
    Anxiety --> CheckAnxiety{有焦虑?}
    CheckAnxiety -->|是| Reset[硬重置]
    CheckAnxiety -->|否| Check2
    
    Check2 -->|是| Compact[压缩旧消息]
    Check2 -->|否| Keep[保持现状]
    
    Reset --> Checkpoint[创建Checkpoint]
    Checkpoint --> NewContext[清空messages<br/>从Checkpoint恢复]
    NewContext --> End[继续迭代]
    
    Compact --> Summarize[摘要历史消息]
    Summarize --> KeepRecent[保留最近消息]
    KeepRecent --> End
    
    Keep --> End
    
    style Reset fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Compact fill:#ffe66d,stroke:#333,stroke-width:2px
    style Keep fill:#96ceb4,stroke:#333,stroke-width:2px
```

---

## 4. Profile系统架构

```mermaid
classDiagram
    class BaseProfile {
        <<abstract>>
        +name: str
        +description: str
        +planner() AgentConfig
        +builder() AgentConfig
        +evaluator() AgentConfig
        +contract_proposer() AgentConfig
        +contract_reviewer() AgentConfig
        +pass_threshold() float
        +max_rounds() int
    }
    
    class AppBuilderProfile {
        +name = "app-builder"
        +description = "Web应用开发"
        +planner() AgentConfig
        +builder() AgentConfig
        +evaluator() AgentConfig
    }
    
    class TerminalProfile {
        +name = "terminal"
        +description = "终端任务"
        +builder() AgentConfig
        +evaluator() AgentConfig
    }
    
    class SWEBenchProfile {
        +name = "swe-bench"
        +description = "GitHub Issue修复"
        +builder() AgentConfig
        +evaluator() AgentConfig
    }
    
    class ReasoningProfile {
        +name = "reasoning"
        +description = "知识问答"
        +planner() AgentConfig
        +builder() AgentConfig
    }
    
    class AgentConfig {
        +enabled: bool
        +system_prompt: str
        +tool_schemas: list
        +middlewares: list
        +time_budget: int
    }
    
    BaseProfile <|-- AppBuilderProfile
    BaseProfile <|-- TerminalProfile
    BaseProfile <|-- SWEBenchProfile
    BaseProfile <|-- ReasoningProfile
    
    BaseProfile ..> AgentConfig : returns
    
    note for AppBuilderProfile "注重视觉设计\n浏览器测试"
    note for TerminalProfile "短超时\n无浏览器测试"
    note for SWEBenchProfile "代码阅读\nBug修复"
    note for ReasoningProfile "技能驱动\n无规划阶段"
```

---

## 5. 技能加载流程

```mermaid
sequenceDiagram
    participant A as Agent
    participant SR as SkillRegistry
    participant FS as FileSystem
    participant C as Context
    
    A->>A: 分析当前任务
    A->>SR: search(keywords)
    activate SR
    
    SR->>SR: 扫描skills目录
    SR->>SR: 解析SKILL.md frontmatter
    SR->>SR: 匹配相关技能
    
    SR-->>A: 返回技能列表
    deactivate SR
    
    A->>A: 选择需要的技能
    
    loop 每个选中的技能
        A->>SR: load(skill_name)
        activate SR
        SR->>FS: 读取SKILL.md
        FS-->>SR: 文件内容
        SR-->>A: 技能文档
        deactivate SR
        
        A->>C: 添加到messages
        activate C
        C-->>A: 更新后的context
        deactivate C
    end
    
    A->>A: 参考技能生成代码
    
    A->>C: 释放技能（可选）
    activate C
    C-->>A: 清理后的context
    deactivate C
```

---

## 6. 工具执行流程

```mermaid
flowchart LR
    subgraph "Agent"
        A[Agent决定调用工具]
    end
    
    subgraph "工具执行器"
        B[解析tool_calls]
        C[安全检查<br/>_resolve路径]
        D{工具类型?}
        
        E1[read_file]
        E2[write_file]
        E3[edit_file]
        E4[run_bash]
        E5[browser_test]
        E6[git_commit]
        E7[read_skill_file]
    end
    
    subgraph "执行环境"
        F1[FileSystem]
        F2[Subprocess]
        F3[Playwright]
        F4[Git]
        F5[Skills Dir]
    end
    
    subgraph "结果返回"
        G[格式化结果]
        H[限制长度]
        I[返回给Agent]
    end
    
    A --> B
    B --> C
    C --> D
    
    D -->|file操作| E1
    D -->|file操作| E2
    D -->|file操作| E3
    D -->|shell命令| E4
    D -->|浏览器| E5
    D -->|git操作| E6
    D -->|技能加载| E7
    
    E1 --> F1
    E2 --> F1
    E3 --> F1
    E4 --> F2
    E5 --> F3
    E6 --> F4
    E7 --> F5
    
    F1 --> G
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G
    
    G --> H
    H --> I
    I --> A
    
    style C fill:#ff6b6b,stroke:#333,stroke-width:2px
    style H fill:#ffe66d,stroke:#333,stroke-width:2px
```

---

## 7. Middleware责任链

```mermaid
flowchart LR
    subgraph "Agent执行前"
        A[Agent准备调用LLM]
    end
    
    subgraph "Middleware Chain - Before"
        B1[TimeoutMiddleware<br/>记录开始时间]
        B2[PerformanceMonitor<br/>计数+1]
        B3[CustomMiddleware<br/>自定义逻辑]
    end
    
    subgraph "LLM调用"
        C[OpenAI API]
    end
    
    subgraph "Middleware Chain - After"
        D1[PerformanceMonitor<br/>记录Token用量]
        D2[TimeoutMiddleware<br/>检查剩余时间]
        D3[RetryMiddleware<br/>错误处理]
    end
    
    subgraph "Agent执行后"
        E[Agent处理响应]
    end
    
    A --> B1
    B1 --> B2
    B2 --> B3
    B3 --> C
    
    C --> D1
    D1 --> D2
    D2 --> D3
    D3 --> E
    
    D2 -->|时间不足| F[注入警告消息]
    F --> E
    
    D3 -->|发生错误| G[指数退避重试]
    G -->|超过最大重试| H[抛出异常]
    G -->|重试成功| C
    
    style B1 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style D2 fill:#ff6b6b,stroke:#333,stroke-width:2px
    style D3 fill:#ffe66d,stroke:#333,stroke-width:2px
```

---

## 8. Contract协商流程

```mermaid
sequenceDiagram
    participant H as Harness
    participant CP as ContractProposer
    participant CR as ContractReviewer
    participant B as Builder
    participant E as Evaluator
    
    H->>CP: Round N: 提议下一步
    activate CP
    
    CP->>CP: 分析当前状态
    CP->>CP: 制定本轮计划
    
    CP-->>H: builder_plan
    deactivate CP
    
    H->>CR: 审核计划
    activate CR
    
    CR->>CR: 评估可行性
    CR->>CR: 设定验收标准
    
    CR-->>H: acceptance_criteria
    deactivate CR
    
    H->>H: 形成Contract
    H->>H: 写入contract.md
    
    H->>B: 执行Contract
    activate B
    
    B->>B: 实现功能
    
    B-->>H: 完成
    deactivate B
    
    H->>E: 根据Contract评估
    activate E
    
    E->>E: 检查验收标准
    E-->>H: score + feedback
    deactivate E
    
    Note over H,E: Contract确保双方目标一致
```

---

## 9. 数据流向图

```mermaid
graph LR
    subgraph "输入"
        A[用户需求]
        B[.env配置]
        C[Profile选择]
    end
    
    subgraph "处理"
        D[Harness.run]
        E[Agent执行]
        F[Context管理]
        G[Tool执行]
        H[Skill加载]
    end
    
    subgraph "输出"
        I[spec.md]
        J[contract.md]
        K[生成的代码]
        L[feedback.md]
        M[trace files]
        N[logs]
    end
    
    subgraph "存储"
        O[workspace/]
        P[logs/]
    end
    
    A --> D
    B --> D
    C --> D
    
    D --> E
    E --> F
    E --> G
    E --> H
    
    F --> E
    G --> E
    H --> E
    
    E --> I
    E --> J
    E --> K
    E --> L
    E --> M
    E --> N
    
    I --> O
    J --> O
    K --> O
    L --> O
    M --> O
    N --> P
    
    style D fill:#ff6b6b,stroke:#333,stroke-width:3px
    style E fill:#4ecdc4,stroke:#333,stroke-width:2px
    style O fill:#96ceb4,stroke:#333,stroke-width:2px
```

---

## 10. 依赖关系图

```mermaid
graph TD
    harness[harness.py] --> agents[agents.py]
    harness --> profiles[profiles/]
    harness --> skills[skills.py]
    harness --> config[config.py]
    
    agents --> context[context.py]
    agents --> tools[tools.py]
    agents --> middlewares[middlewares.py]
    agents --> logger[logger.py]
    
    profiles --> config
    profiles --> agents
    
    skills --> config
    
    tools --> config
    tools --> playwright[playwright]
    
    context --> tiktoken[tiktoken]
    context --> config
    
    middlewares --> logger
    middlewares --> config
    
    logger --> config
    
    harness -.->|uses| openai[openai SDK]
    agents -.->|uses| openai
    
    style harness fill:#ff6b6b,stroke:#333,stroke-width:3px
    style agents fill:#4ecdc4,stroke:#333,stroke-width:2px
    style openai fill:#ffe66d,stroke:#333,stroke-width:2px
```

---

## 11. 文件结构树状图

```mermaid
graph TD
    Root[Harness_Engineering/]
    
    Core[核心引擎<br/>~2800行]
    Profiles[Profiles<br/>~300行]
    Skills[Skills<br/>37个]
    Support[支持模块<br/>~1200行]
    Runtime[运行时目录]
    
    Root --> Core
    Root --> Profiles
    Root --> Skills
    Root --> Support
    Root --> Runtime
    
    Core --> harness[harness.py<br/>521行]
    Core --> agents[agents.py<br/>427行]
    Core --> context[context.py<br/>310行]
    Core --> tools[tools.py<br/>1075行]
    Core --> prompts[prompts.py]
    
    Profiles --> base[base.py]
    Profiles --> app_builder[app_builder.py]
    Profiles --> terminal[terminal.py]
    Profiles --> swe_bench[swe_bench.py]
    Profiles --> reasoning[reasoning.py]
    
    Skills --> frontend[frontend-design]
    Skills --> password[password-recovery]
    Skills --> video[video-processing]
    Skills --> torch[torch-*]
    Skills --> others[...33 more]
    
    Support --> config[config.py]
    Support --> logger[logger.py]
    Support --> middlewares[middlewares.py<br/>~800行]
    Support --> skills_reg[skills.py]
    
    Runtime --> workspace[workspace/<br/>任务输出]
    Runtime --> logs[logs/<br/>日志文件]
    Runtime --> venv[.venv/<br/>虚拟环境]
    
    style Core fill:#ff6b6b,stroke:#333,stroke-width:2px
    style Profiles fill:#4ecdc4,stroke:#333,stroke-width:2px
    style Skills fill:#96ceb4,stroke:#333,stroke-width:2px
```

---

## 12. 性能监控图

```mermaid
graph LR
    subgraph "监控指标"
        M1[LLM调用次数]
        M2[Token用量]
        M3[工具调用次数]
        M4[错误次数]
        M5[总耗时]
    end
    
    subgraph "收集方式"
        C1[PerformanceMonitor<br/>Middleware]
        C2[TraceWriter<br/>JSONL]
        C3[Logger<br/>日志文件]
    end
    
    subgraph "分析工具"
        A1[scripts/analyze_trace.py]
        A2[jq命令行]
        A3[手动查看]
    end
    
    subgraph "优化决策"
        D1[调整阈值]
        D2[更换模型]
        D3[加载技能]
        D4[简化需求]
    end
    
    M1 --> C1
    M2 --> C1
    M3 --> C2
    M4 --> C3
    M5 --> C1
    
    C1 --> A1
    C2 --> A2
    C3 --> A3
    
    A1 --> D1
    A2 --> D2
    A3 --> D3
    A1 --> D4
    
    style C1 fill:#4ecdc4,stroke:#333,stroke-width:2px
    style A1 fill:#ffe66d,stroke:#333,stroke-width:2px
```

---

<div align="center">

**📊 通过这些图表，你可以直观理解Harness的架构！**

*配合 [ARCHITECTURE.md](ARCHITECTURE.md) 和 [ARCHITECTURE_QUICK.md](ARCHITECTURE_QUICK.md) 使用效果更佳*

</div>