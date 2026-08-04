# 周公解梦 · 梦境解读技能 v1.0

> 基于传统《周公解梦》意象体系，结合现代心理分析视角，对梦境情景进行双轨解读。覆盖 600+ 高频梦境意象。

## 功能特性

- **双轨解读**：传统周公寓意（吉凶预兆）+ 现代心理视角（潜意识映射）
- **意象提取**：自动从自然语言梦境中提取关键意象（最长子串优先）
- **600+ 意象库**：动物 / 人物 / 自然 / 建筑 / 器物 / 身体 / 行为 / 数字 / 颜色 / 神话
- **结构化输出**：梦境摘要 → 意象拆解 → 综合建议（传统宜忌 + 心理行动）
- **零外部依赖**：纯 Python 标准库，开箱即用

## 安装

```bash
# 克隆仓库到 Marvis skills 目录
git clone https://github.com/buyaodaohao/zhougong-dream-skill.git
cp -r zhougong-dream-skill ~/Marvis/skills/zhougong-dream/
```

零外部依赖，无需 pip install 任何包。

## 使用方法

```bash
# 整段梦境解读
python scripts/dream.py --text "我梦见一条蛇追我，然后掉进河里，看到一条大鱼"

# 单意象查询
python scripts/dream.py --word 蛇

# JSON 输出（便于程序调用）
python scripts/dream.py --text "梦见大火" --json
```

## 版本历史

### v1.0 (2026-08-04)
- 初版发布，覆盖 600+ 梦境意象
- 双轨解读（传统寓意 + 心理视角）
- 自动意象提取与综合建议生成

## 免责声明

本工具仅供学习和研究传统文化、自我觉察之用，梦境解读不构成任何医疗、心理或决策建议。
