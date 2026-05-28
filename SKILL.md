---
name: deepseek-cache-optimization
description: DeepSeek API 缓存命中率优化与成本降低 - 提高缓存命中率至 90%+，节省 70%+ 成本
version: 1.0.0
tags: [deepseek, cache, cost-optimization, api, llm]
triggers:
  - deepseek 缓存
  - deepseek 成本优化
  - API 缓存命中率
  - 降低 LLM 成本
  - deepseek cache
---

# DeepSeek 缓存命中率优化与成本降低

## 核心原则

### 1. 稳定前缀原则 ⭐⭐⭐

**核心思想**：保持请求的前缀部分完全一致

```python
# ❌ 错误方式 - 每次请求前缀不同
messages = [
    {"role": "system", "content": f"你是助手，当前时间：{datetime.now()}"},
    {"role": "user", "content": user_input}
]

# ✅ 正确方式 - 稳定的 system prompt
messages = [
    {"role": "system", "content": "你是一个专业的AI助手。"},
    {"role": "user", "content": user_input}
]
```

### 2. 消息顺序优化

```python
# ❌ 错误 - 动态内容在前
messages = [
    {"role": "system", "content": f"时间: {now()}, 用户: {user_id}"},  # 动态
    {"role": "system", "content": "你是AI助手"},  # 静态
    {"role": "user", "content": question}
]

# ✅ 正确 - 静态内容在前
messages = [
    {"role": "system", "content": "你是AI助手"},  # 静态 - 可缓存
    {"role": "system", "content": "请用中文回答"},  # 静态 - 可缓存
    {"role": "user", "content": f"时间: {now()}, 问题: {question}"}  # 动态放后面
]
```

### 3. System Prompt 设计

```python
# ❌ 避免 - 包含动态内容
system_prompt = f"""
你是助手。
当前时间：{datetime.now()}  # ❌ 每次都变
用户ID：{user_id}  # ❌ 每个用户不同
会话ID：{session_id}  # ❌ 每次都变
"""

# ✅ 推荐 - 静态内容放前面
system_prompt = """
你是一个专业的AI助手，擅长回答技术问题。
请用中文回答，保持简洁专业。
"""  # ✅ 完全静态，可缓存

# 动态内容放在用户消息中
user_message = f"""
当前时间：{datetime.now()}
用户问题：{user_input}
"""
```

## 价格结构（DeepSeek V4 Pro）

| 类型 | 价格（元/百万tokens） | 节省比例 |
|------|----------------------|----------|
| **输入（缓存命中）** | **0.025** | 97.5% |
| **输入（缓存未命中）** | 3 | - |
| **输出** | 6 | - |

**关键发现**：缓存命中价格是未命中的 **1/120**！

## 降低输出成本

### 1. 限制输出长度

```python
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    max_tokens=500,  # ✅ 限制输出长度
)
```

### 2. 使用 JSON Output

```python
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    response_format={"type": "json_object"},
)
```

### 3. 优化 Prompt

```python
# ❌ 模糊指令
prompt = "解释什么是机器学习"

# ✅ 明确指令
prompt = "用 3 句话解释什么是机器学习，每句话不超过 20 个字"
```

### 4. 思考模式控制

```python
# 非思考模式 - 更快更便宜
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    thinking={"type": "disabled"},
)

# 思考模式 - 使用低推理深度
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    thinking={"type": "enabled"},
    reasoning_effort="low",
)
```

## 监控缓存命中率

```python
def call_api_with_monitoring(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
    )
    
    usage = response.usage
    cache_hit_tokens = usage.prompt_cache_hit_tokens
    cache_miss_tokens = usage.prompt_cache_miss_tokens
    
    hit_rate = cache_hit_tokens / (cache_hit_tokens + cache_miss_tokens)
    
    print(f"缓存命中率: {hit_rate:.2%}")
    print(f"命中 tokens: {cache_hit_tokens}, 未命中: {cache_miss_tokens}")
    
    return response
```

## 成本计算公式

```
月成本 = (输入tokens × 缓存命中率 × 0.025 + 
         输入tokens × (1-缓存命中率) × 3 + 
         输出tokens × 6) / 1,000,000
```

## 实战案例

### 客服系统优化

**优化前**：
```python
system = f"你是客服助手。当前时间：{datetime.now()}"
# 缓存命中率：~10%
# 月成本：¥3000
```

**优化后**：
```python
system = "你是客服助手。请用专业友好的语气回答用户问题。"
user = f"[{datetime.now()}] {user_message}"
# 缓存命中率：~85%
# 月成本：¥450
```

**节省**：85%

## 检查清单

### ✅ 缓存优化检查

- [ ] System Prompt 是否完全静态？
- [ ] 动态内容是否放在用户消息中？
- [ ] 消息顺序是否：静态 → 动态？
- [ ] 是否监控了缓存命中率？

### ✅ 输出优化检查

- [ ] 是否设置了合理的 max_tokens？
- [ ] 是否使用了 JSON 格式约束输出？
- [ ] Prompt 是否明确指定了输出格式？
- [ ] 是否使用了合适的思考模式？

## 常见问题

### Q1: 缓存多久失效？
A: DeepSeek 的缓存通常在 **1-2 小时** 内有效。

### Q2: 如何查看缓存命中率？
A: 通过 `usage.prompt_cache_hit_tokens` 和 `usage.prompt_cache_miss_tokens` 字段。

### Q3: 思考模式会影响缓存吗？
A: 是的，思考模式的输出会被缓存，但思考过程的 tokens 不会。

## 参考资料

- [DeepSeek API 文档](https://api-docs.deepseek.com/zh-cn/)
- [DeepSeek 价格说明](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)
