#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周公解梦 v1.0 - 梦境意象提取与双轨解读
零外部依赖，仅使用标准库。

用法:
  python dream.py --word 蛇
  python dream.py --text "我梦见一条蛇追我，然后掉进河里"
  python dream.py --text "梦见考试迟到" --json
"""

import argparse
import json
import os
import re
import sys

# 词典路径：与脚本同级的 references/dream-dict.md
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(SCRIPT_DIR, "..", "references", "dream-dict.md")


def load_dict(path=DICT_PATH):
    """解析 dream-dict.md，返回 {意象词: {traditional, psychology, category}}"""
    if not os.path.exists(path):
        return {}
    entries = {}
    current = None
    section = None  # 'traditional' | 'psychology' | 'category'
    buf = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            # 词条标题: ## 蛇
            m = re.match(r"^##\s+(.+)$", line)
            if m:
                if current is not None:
                    entries[current][section] = "\n".join(buf).strip()
                current = m.group(1).strip()
                entries[current] = {"traditional": "", "psychology": "", "category": ""}
                section = None
                buf = []
                continue
            # 小节标题
            sm = re.match(r"^###\s+(传统寓意|心理视角|分类)$", line)
            if sm and current is not None:
                if section is not None:
                    entries[current][section] = "\n".join(buf).strip()
                label = sm.group(1)
                section = {"传统寓意": "traditional", "心理视角": "psychology", "分类": "category"}[label]
                buf = []
                continue
            if current is not None and section is not None:
                buf.append(line)
    if current is not None and section is not None:
        entries[current][section] = "\n".join(buf).strip()
    return entries


def extract_words(text, dictionary):
    """从文本中提取词典中存在的意象词，按出现顺序去重返回"""
    found = []
    seen = set()
    # 长词优先匹配，避免 '蛇' 抢在 '大蛇' 前
    words = sorted(dictionary.keys(), key=len, reverse=True)
    for w in words:
        if w in text and w not in seen:
            # 子意象去重：若已匹配的意象中包含当前词（如已匹配'大鱼'则跳过'鱼'）
            if any(w in f for f in found):
                continue
            found.append(w)
            seen.add(w)
    return found


def interpret(word, dictionary):
    """返回单条解读 dict"""
    if word in dictionary:
        d = dictionary[word]
        return {
            "word": word,
            "category": d.get("category", ""),
            "traditional": d.get("traditional", ""),
            "psychology": d.get("psychology", ""),
            "found": True,
        }
    return {
        "word": word,
        "category": "",
        "traditional": "",
        "psychology": "",
        "found": False,
    }


def render_text(text, dictionary):
    words = extract_words(text, dictionary)
    if not words:
        return "未能从梦境中识别到已知意象。请补充更多梦境细节，或描述具体的人、物、场景。"
    lines = []
    lines.append("## 梦境摘要")
    lines.append(f"梦境中识别到 {len(words)} 个关键意象：{ '、'.join(words) }。\n")
    lines.append("## 关键意象拆解")
    for w in words:
        r = interpret(w, dictionary)
        lines.append(f"\n### 意象：{w}（{r['category']}）")
        if r["found"]:
            lines.append(f"- 传统寓意：{r['traditional']}")
            lines.append(f"- 心理视角：{r['psychology']}")
        else:
            lines.append("- 暂无标准解读，建议从近期情绪与压力源角度自我觉察。")
    lines.append("\n## 综合建议")
    lines.append("- 传统宜忌：结合上述意象的吉凶倾向综合判断（详见各意象传统寓意）。")
    lines.append("- 心理行动：关注近期情绪与压力源；反复出现的意象往往指向未处理的现实议题，可尝试记录并梳理。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="周公解梦 - 梦境意象双轨解读")
    parser.add_argument("--word", help="查询单个意象词")
    parser.add_argument("--text", help="整段梦境文本，自动提取意象")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    dictionary = load_dict()
    if not dictionary:
        print("错误：未找到词典文件 references/dream-dict.md", file=sys.stderr)
        sys.exit(1)

    if args.word:
        r = interpret(args.word, dictionary)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            if r["found"]:
                print(f"【{r['word']}】（{r['category']}）")
                print(f"传统寓意：{r['traditional']}")
                print(f"心理视角：{r['psychology']}")
            else:
                print(f"【{r['word']}】暂无标准解读。")
        return

    if args.text:
        if args.json:
            words = extract_words(args.text, dictionary)
            print(json.dumps(
                {"words": [interpret(w, dictionary) for w in words]},
                ensure_ascii=False, indent=2
            ))
        else:
            print(render_text(args.text, dictionary))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
