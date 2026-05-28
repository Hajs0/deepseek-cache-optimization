#!/usr/bin/env python3
"""
DeepSeek 缓存优化快速参考
使用方法: python3 quick_reference.py
"""

# 1. 最佳实践模板
BEST_PRACTICE_TEMPLATE = """
# DeepSeek 缓存优化最佳实践

## 1. System Prompt 设计
```python
# ✅ 正确 - 静态 System Prompt
system_prompt = """
你是一个专业的AI助手，擅长回答技术问题。
请用中文回答，保持简洁专业。
"""

# ❌ 错误 - 动态 System Prompt
system_prompt = f"""
你是助手。
当前时间：{datetime.now()}  # 每次都变，破坏缓存
"""
```

## 2. 消息顺序
```python
messages = [
    {"role": "system", "content": STATIC_SYSTEM_PROMPT},  # 静态 - 可缓存
    {"role": "system", "content": "请用中文回答"},        # 静态 - 可缓存
    {"role": "user", "content": f"时间: {now()}, 问题: {question}"}  # 动态放后面
]
```

## 3. 监控缓存命中率
```python
def call_api_with_monitoring(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
    )
    
    usage = response.usage
    cache_hit = usage.prompt_cache_hit_tokens
    cache_miss = usage.prompt_cache_miss_tokens
    hit_rate = cache_hit / (cache_hit + cache_miss)
    
    print(f"缓存命中率: {hit_rate:.2%}")
    return response
```

## 4. 成本计算
月成本 = (输入tokens × 缓存命中率 × 0.025 + 
         输入tokens × (1-缓存命中率) × 3 + 
         输出tokens × 6) / 1,000,000
"""

# 2. 代码模板
CODE_TEMPLATE = """
from openai import OpenAI
from datetime import datetime

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.deepseek.com"
)

# 静态 System Prompt（可缓存）
SYSTEM_PROMPT = \"\"\"
你是一个专业的AI助手。
规则：
1. 用中文回答
2. 保持简洁
3. 引用来源
\"\"\"

def chat(user_message, history=None):
    \"\"\"缓存友好的对话函数\"\"\"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},  # 固定前缀
    ]
    
    if history:
        messages.extend(history)
    
    # 动态内容放在用户消息中
    messages.append({
        "role": "user", 
        "content": f"当前时间：{datetime.now()}\\n问题：{user_message}"
    })
    
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        max_tokens=500,  # 限制输出长度
    )
    
    # 监控缓存命中率
    usage = response.usage
    cache_hit = usage.prompt_cache_hit_tokens
    cache_miss = usage.prompt_cache_miss_tokens
    hit_rate = cache_hit / (cache_hit + cache_miss)
    print(f"缓存命中率: {hit_rate:.2%}")
    
    return response.choices[0].message.content
"""

# 3. 检查清单
CHECKLIST = """
## 缓存优化检查清单

### ✅ 缓存优化
- [ ] System Prompt 是否完全静态？
- [ ] 动态内容是否放在用户消息中？
- [ ] 消息顺序是否：静态 → 动态？
- [ ] 是否监控了缓存命中率？

### ✅ 输出优化
- [ ] 是否设置了合理的 max_tokens？
- [ ] 是否使用了 JSON 格式约束输出？
- [ ] Prompt 是否明确指定了输出格式？
- [ ] 是否使用了合适的思考模式？
"""

def main():
    print("=" * 60)
    print("DeepSeek 缓存优化快速参考")
    print("=" * 60)
    
    print("\n📊 价格结构（DeepSeek V4 Pro）:")
    print("-" * 40)
    print("输入（缓存命中）: 0.025 元/百万tokens")
    print("输入（缓存未命中）: 3 元/百万tokens")
    print("输出: 6 元/百万tokens")
    print("\n💡 缓存命中价格是未命中的 1/120!")
    
    print("\n" + "=" * 60)
    print("📝 最佳实践模板")
    print("=" * 60)
    print(BEST_PRACTICE_TEMPLATE)
    
    print("\n" + "=" * 60)
    print("💻 代码模板")
    print("=" * 60)
    print(CODE_TEMPLATE)
    
    print("\n" + "=" * 60)
    print("✅ 检查清单")
    print("=" * 60)
    print(CHECKLIST)
    
    print("\n" + "=" * 60)
    print("💰 成本计算示例")
    print("=" * 60)
    print("""
假设：
- 每月输入 tokens：100M
- 每月输出 tokens：20M

优化前（缓存命中率 10%）：
  月成本 = (100M × 10% × 0.025 + 100M × 90% × 3 + 20M × 6) / 1M
         = (0.25 + 270 + 120) / 1
         = ¥390.25

优化后（缓存命中率 85%）：
  月成本 = (100M × 85% × 0.025 + 100M × 15% × 3 + 20M × 6) / 1M
         = (2.125 + 45 + 120) / 1
         = ¥167.125

节省：¥223.125/月 (57%)
    """)

if __name__ == "__main__":
    main()
