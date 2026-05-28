#!/bin/bash
# DeepSeek Cache Optimization Skill 安装脚本
# 使用方法: bash install.sh

set -e

echo "🚀 开始安装 DeepSeek Cache Optimization Skill..."

# 检查 Hermes Agent 是否安装
if [ ! -d "$HOME/.hermes" ]; then
    echo "❌ 错误: 未找到 Hermes Agent"
    echo "请先安装 Hermes Agent: https://hermes-agent.nousresearch.com"
    exit 1
fi

# 创建技能目录
SKILL_DIR="$HOME/.hermes/skills/mlops/deepseek-cache-optimization"
mkdir -p "$SKILL_DIR/scripts"

# 复制文件
echo "📦 复制文件..."
cp SKILL.md "$SKILL_DIR/"
cp scripts/quick_reference.py "$SKILL_DIR/scripts/"

echo "✅ 安装完成!"
echo ""
echo "📖 使用方法:"
echo "  1. 在 Hermes Agent 对话中说: 加载 deepseek-cache-optimization 技能"
echo "  2. 或运行快速参考: python3 $SKILL_DIR/scripts/quick_reference.py"
echo ""
echo "📚 文档位置: $SKILL_DIR/SKILL.md"
echo ""
echo "💰 预期效果: 缓存命中率提升至 85%+，节省 70%+ 成本"
