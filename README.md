# DeepSeek Cache Optimization Skill

🚀 DeepSeek API 缓存命中率优化与成本降低指南

## 功能特性

- 📊 详细的价格分析和成本计算
- 🎯 5 大核心优化策略
- 💻 可直接使用的代码模板
- ✅ 实战检查清单
- 📈 预期节省 70%+ 成本

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/deepseek-cache-optimization.git
cd deepseek-cache-optimization
```

### 2. 安装到 Hermes Agent

```bash
# 创建技能目录
mkdir -p ~/.hermes/skills/mlops/deepseek-cache-optimization

# 复制文件
cp SKILL.md ~/.hermes/skills/mlops/deepseek-cache-optimization/
cp -r scripts ~/.hermes/skills/mlops/deepseek-cache-optimization/
```

### 3. 使用技能

在 Hermes Agent 对话中：
```
加载 deepseek-cache-optimization 技能
```

或运行快速参考脚本：
```bash
python3 ~/.hermes/skills/mlops/deepseek-cache-optimization/scripts/quick_reference.py
```

## 核心优化策略

### 1. 稳定前缀原则

```python
# ❌ 错误 - 动态 System Prompt
system = f"你是助手，当前时间：{datetime.now()}"

# ✅ 正确 - 静态 System Prompt
system = "你是专业的AI助手"
user = f"时间：{datetime.now()}，问题：{question}"
```

### 2. 消息顺序优化

```python
messages = [
    {"role": "system", "content": STATIC_PROMPT},  # 静态 - 可缓存
    {"role": "user", "content": dynamic_content}   # 动态 - 放后面
]
```

### 3. 输出控制

```python
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    max_tokens=500,  # 限制输出长度
    response_format={"type": "json_object"},  # JSON 格式更紧凑
)
```

## 价格结构

| 类型 | 价格（元/百万tokens） |
|------|----------------------|
| 输入（缓存命中） | **0.025** |
| 输入（缓存未命中） | 3 |
| 输出 | 6 |

**缓存命中价格是未命中的 1/120！**

## 成本节省示例

假设每月 100M 输入 tokens + 20M 输出 tokens：

| 缓存命中率 | 月成本 | 节省 |
|-----------|--------|------|
| 10%（优化前） | ¥390 | - |
| 85%（优化后） | ¥167 | **57%** |

## 文件结构

```
deepseek-cache-optimization/
├── SKILL.md              # 主文档
├── scripts/
│   └── quick_reference.py  # 快速参考脚本
└── README.md             # 本文件
```

## 相关资源

- [DeepSeek API 文档](https://api-docs.deepseek.com/zh-cn/)
- [DeepSeek 价格说明](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)

## License

MIT
