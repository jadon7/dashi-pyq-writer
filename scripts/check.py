#!/usr/bin/env python3
"""大师朋友圈文案检查。

按去 AI 味硬禁令（整理自数字生命卡兹克的 human-writing，MIT）、「我」字指标和微信敏感词逐条检查。
只查形状，判断还得靠人。FAIL 必须清零；WARN 逐条人工判断。
字数口径：去掉空格和换行后的字符数，标点、英文字母、数字都算；建议 200–270，低于 120 或高于 280 给 WARN。

用法:
  python3 check.py posts.json [more.json ...]   # JSON 数组，每项有 text，可选 comment
  python3 check.py drafts.txt                   # 纯文本，多条之间用单独一行 --- 隔开
"""
import json
import re
import sys

HARD_STOPS = ("说白了", "说穿了", "先说结论")
HARD_JARGON = ("赋能", "抓手", "商业闭环", "价值闭环", "能力沉淀", "拉通", "底层逻辑", "顶层设计",
               "认知跃迁", "价值释放", "能力建设", "降本增效", "内容矩阵", "全链路", "组合拳",
               "打开想象空间", "结构性机会", "关键命题", "深层逻辑", "技术底座", "公共底座",
               "技术主权", "单点风险", "主脊柱", "材料锚点", "认知增量", "迭代闭环")
ROAD_SIGNS = ("更微妙的是", "还有一层", "只说对了一半", "值得注意的是", "需要指出的是",
              "从某种意义上说", "总而言之", "综上所述")
CONTEXT_JARGON = ("沉淀", "颗粒度", "对齐", "协同", "链路", "生态位", "心智", "范式", "方法论",
                  "核心变量", "打法", "想象空间", "闭环", "赛道", "痛点")
LYRIC = ("安放", "抵达", "微光", "褶皱", "丰盈", "滚烫", "轻盈", "赤裸", "剥开", "锋利")
SOFT = ("真正", "本质上", "更深层次", "归根结底", "换句话说", "不可否认", "核心是", "关键在于", "这意味着")
SENSITIVE = ("翻墙", "梯子", "VPN", "vpn", "节点", "机场", "中转站", "代充", "虚拟卡", "接码",
             "礼品卡", "美区", "外区", "土区", "KYC", "kyc", "绕过", "不违反")
PROFANITY = ("卧槽", "牛逼", "tm", "他妈", "傻逼")

PIVOTS = [
    r"(?:并)?不是[^。！？\n]{0,90}而是", r"不(?:仅仅|仅|只|单)是[^。！？\n]{0,90}而是",
    r"并非[^。！？\n]{0,90}而是", r"不在于[^。！？\n]{0,90}而在于",
    r"与其说[^。！？\n]{0,90}(?:不如|毋宁|倒不如)", r"[。！？!?]\s*而是",
    r"表面(?:上)?[^。！？\n]{0,90}(?:其实|实际|实则)", r"看似[^。！？\n]{0,90}(?:其实|实际|实则)",
    r"(?:总|一直|曾|都)?以为[^！？\n]{2,60}?(?:其实|才发现|才明白|才知道|后来才)",
    r"回头(?:看|一看)?才(?:发现|明白|知道)", r"(?:并)?不是[^。！？\n]{1,40}，(?:更|才)?是[^，。！？\n]",
    r"从来(?:都)?(?:不是|与[^。！？，\n]{1,12}无关)", r"恰恰相反",
    r"[^，。！？\n]{1,12}不重要，(?:重要|要紧)的是", r"真正[^，。！？\n]{0,16}的(?:，)?是",
    r"说到底", r"你以为",
]
NOMINAL = [
    r"进行(?:了|一次|一场|着)?[^。，！？\n]{0,10}(?:调整|优化|升级|分析|讨论|沟通|梳理|复盘|迭代|探索|尝试|思考|规划|布局)",
    r"实现了?[^。，！？\n]{0,14}的?[^。，！？\n]{0,6}(?:提升|增长|突破|转变|跃升|落地)",
    r"完成了?对[^。，！？\n]{0,16}的", r"起到了?[^。，！？\n]{0,12}的?作用", r"具有[^。，！？\n]{0,10}(?:意义|价值)",
]
OPENERS = [r"在当今[^，。！？\n]{0,16}(?:时代|社会|世界)", r"在这个[^，。！？\n]{0,16}的(?:时代|年代)",
           r"众所周知", r"让我们[^。！？\n]{0,30}吧"]
STRIP = [re.compile(r"https?://\S+"), re.compile(r"`[^`\n]*`")]


def clean(t):
    for p in STRIP:
        t = p.sub(" ", t)
    return t


def check_text(t, body=True):
    fails, warns = [], []
    c = clean(t)
    for w in HARD_STOPS + HARD_JARGON + ROAD_SIGNS:
        if w in c:
            fails.append(f"禁用词「{w}」")
    for ch, name in (("—", "破折号"), ("–", "连接号")):
        if ch in c:
            fails.append(name)
    for m in re.finditer(r"[：:]", c):
        nxt = c[m.end():m.end() + 1]
        if nxt not in "“「\"『":
            fails.append(f"提示性冒号「{c[max(0, m.start() - 8):m.end() + 4]}」")
    for p in PIVOTS:
        for m in re.finditer(p, c):
            fails.append(f"翻案腔「{m.group(0)[:30]}」")
    for p in NOMINAL:
        for m in re.finditer(p, c):
            fails.append(f"名词化「{m.group(0)[:24]}」")
    for p in OPENERS:
        if re.search(p, c):
            fails.append(f"套话「{p}」")
    for w in SENSITIVE:
        if w in c:
            fails.append(f"微信敏感词「{w}」")
    for w in PROFANITY:
        if w in c:
            fails.append(f"粗口「{w}」")
    wo = c.count("我") if body else 0
    if wo > 2:
        fails.append(f"「我」字 {wo} 个，最多 2 个")
    starts = sum(1 for line in c.split("\n") if line.strip().startswith("我")) if body else 0
    if starts > 1:
        fails.append(f"以「我」开头的行 {starts} 行，最多 1 行")
    for w in CONTEXT_JARGON + LYRIC + SOFT:
        if w in c:
            warns.append(f"语境词「{w}」")
    if c.count("「") >= 3:
        warns.append("「」自造短语偏多")
    n = len(re.sub(r"\s", "", clean(t)))
    return fails, warns, n


def load(path):
    raw = open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        items = json.loads(raw)
    else:
        parts = [p.strip() for p in re.split(r"(?m)^---\s*$", raw) if p.strip()]
        items = [{"text": p} for p in parts]
    for i, it in enumerate(items, 1):
        it.setdefault("slot", it.get("time") or i)
    return items


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    total_fail = 0
    for path in paths:
        for it in load(path):
            for field in ("text", "comment"):
                t = it.get(field) or ""
                if not t:
                    continue
                f, w, n = check_text(t, field == "text")
                tag = f"[{it.get('slot')}] {field}"
                if field == "text" and not (120 <= n <= 280):
                    w.append(f"字数 {n}")
                for x in f:
                    print(f"FAIL {tag}: {x}")
                for x in w:
                    print(f"WARN {tag}: {x}")
                total_fail += len(f)
    print(f"== FAIL 合计 {total_fail}")
    return 1 if total_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
