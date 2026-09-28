#!/usr/bin/env python3
"""textfold 的固定验收程序。

场景（9 个）：case 2 + mark 2 + idem 2 + width 2 + other 1。

本文件属于固定判据，解题者不得修改。全部判据都是硬编码的期望值：
不依赖墙钟、机器速度、`dict` 迭代顺序、`locale` 或随机源。
"""

import argparse
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from textfold import fold  # noqa: E402


def _verdict(ok, expected, actual):
    return (bool(ok), expected, actual)


# --------------------------------------------------------------------------
# case group：大小写折叠（含展开与土耳其 i 边界）
# --------------------------------------------------------------------------

def scenario_case_expansions():
    pairs = (
        ("Straße", "strasse"),
        ("GROSS", "gross"),
        ("ﬁne", "fine"),
        ("ﬀi", "ffi"),
        ("ﬂow", "flow"),
    )
    problems = []
    for src, want in pairs:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "全部展开正确", "通过" if ok else ";".join(problems))


def scenario_case_dotted_i_boundary():
    checks = (
        ("İ", "i"),
        ("I", "i"),
        ("ı", "ı"),
        ("İSTANBUL", "istanbul"),
        ("DİYARBAKIR", "diyarbakir"),
    )
    problems = []
    for src, want in checks:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "带点/不带点的 i 都归一", "通过" if ok else ";".join(problems))


# --------------------------------------------------------------------------
# mark group：变音符号去除
# --------------------------------------------------------------------------

def scenario_mark_removes_combining():
    cases = (
        ("caf\u00e9", "cafe"),
        ("cafe\u0301", "cafe"),
        ("A\u0300\u0308B", "ab"),
        ("na\u0308ive", "naive"),
        ("\u0301", ""),
    )
    problems = []
    for src, want in cases:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "组合符号被去除", "通过" if ok else ";".join(problems))


def scenario_mark_nfc_roundtrip():
    cases = (
        ("\u00e9\u0301", "e"),
        ("\u0041\u030a", "a"),
        ("\u1e63\u0323", "s"),
        ("한국어", "한국어"),
        ("\u00f1", "n"),
    )
    problems = []
    for src, want in cases:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "去符号后重新合成", "通过" if ok else ";".join(problems))


# --------------------------------------------------------------------------
# idem group：幂等
# --------------------------------------------------------------------------

_IDEM_INPUTS = (
    "Straße",
    "e\u0301",
    "\uff21\uff22\uff11\uff12\uff13",
    "\uff21\uff22\u3000\uff23",
    "\ufb03",
    "\u01f0",
    "中🌊",
    "",
    "  X  ",
    "\u0130",
)


def scenario_idem_any_input():
    problems = []
    for src in _IDEM_INPUTS:
        once = fold(src)
        twice = fold(once)
        if twice != once:
            problems.append("%r: %r→%r" % (src, once, twice))
    ok = not problems
    return _verdict(ok, "fold∘fold == fold", "通过" if ok else ";".join(problems))


def scenario_idem_second_pass_stable():
    problems = []
    for src in ("\u01f0", "\ufb03", "e\u0301"):
        once = fold(src)
        twice = fold(once)
        if twice != once:
            problems.append("%r: 二次折叠变了 %r→%r" % (src, once, twice))
    # 第一次折叠就必须越过组合符号这一层，否则第二次还会继续变
    canonical = (
        ("M\u00fcnchen", "munchen"),
        ("\u01f0", "j"),
    )
    for src, want in canonical:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "一次折叠即到规范形式", "通过" if ok else ";".join(problems))


# --------------------------------------------------------------------------
# width group：全角 / 半角
# --------------------------------------------------------------------------

def scenario_width_on_folds_fullwidth():
    cases = (
        ("ＡＢＣ", "abc"),
        ("１２３", "123"),
        ("ＡＢ　Ｃ", "ab c"),
        ("！＃＄", "!#$"),
        ("！Ａ１", "!a1"),
        ("ﾊﾝｶｸ", "ﾊﾝｶｸ"),
    )
    problems = []
    for src, want in cases:
        got = fold(src, width=True)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "全角折成半角（含 U+3000）", "通过" if ok else ";".join(problems))


def scenario_width_off_keeps_fullwidth():
    cases = (
        ("ＡＢ", "ａｂ"),
        ("１２３", "１２３"),
        ("！＃", "！＃"),
        ("ＡＢ　Ｃ", "ａｂ　ｃ"),
        ("ＡＢC", "ａｂc"),
    )
    problems = []
    for src, want in cases:
        got = fold(src, width=False)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "width=False 不动全角", "通过" if ok else ";".join(problems))


# --------------------------------------------------------------------------
# other group：非拉丁字符原样保留
# --------------------------------------------------------------------------

def scenario_other_keeps_non_latin():
    cases = (
        ("中文测试", "中文测试"),
        ("🌊🎉", "🌊🎉"),
        ("مرحبا", "مرحبا"),
        ("Ab中文🌊", "ab中文🌊"),
        ("日本語テスト", "日本語テスト"),
    )
    problems = []
    for src, want in cases:
        got = fold(src)
        if got != want:
            problems.append("%r→%r(期望 %r)" % (src, got, want))
    ok = not problems
    return _verdict(ok, "非拉丁字符原样", "通过" if ok else ";".join(problems))


SCENARIOS = (
    ("case", "expansions", scenario_case_expansions),
    ("case", "dotted-i-boundary", scenario_case_dotted_i_boundary),
    ("mark", "removes-combining", scenario_mark_removes_combining),
    ("mark", "nfc-roundtrip", scenario_mark_nfc_roundtrip),
    ("idem", "any-input", scenario_idem_any_input),
    ("idem", "second-pass-stable", scenario_idem_second_pass_stable),
    ("width", "on-folds-fullwidth", scenario_width_on_folds_fullwidth),
    ("width", "off-keeps-fullwidth", scenario_width_off_keeps_fullwidth),
    ("other", "keeps-non-latin", scenario_other_keeps_non_latin),
)


def main(argv=None):
    parser = argparse.ArgumentParser(prog="check.py")
    parser.add_argument("-list", dest="list_scenarios", action="store_true",
                        help="列出全部场景后退出")
    parser.add_argument("--only", dest="only", default=None,
                        help="只运行指定组")
    args = parser.parse_args(argv)

    if args.list_scenarios:
        for group, name, _func in SCENARIOS:
            print("%s/%s" % (group, name))
        return 0

    selected = [s for s in SCENARIOS if args.only is None or s[0] == args.only]
    passed = 0
    for group, name, func in selected:
        try:
            ok, expected, actual = func()
        except NotImplementedError:
            ok, expected, actual = False, "已实现", "NotImplementedError"
        except Exception as exc:  # noqa: BLE001
            ok, expected, actual = False, "无异常", "%s: %s" % (type(exc).__name__, exc)
        if ok:
            passed += 1
            print("PASS %s/%s" % (group, name))
        else:
            print("FAIL %s/%s  期望=%s 实际=%s" % (group, name, expected, actual))

    print("结果：通过 %d/%d" % (passed, len(selected)))
    return 0 if selected and passed == len(selected) else 1


if __name__ == "__main__":
    sys.exit(main())
