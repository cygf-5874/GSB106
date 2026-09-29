"""textfold.fold —— 折叠键的实现。

对外签名已定死（`fold(s, *, width=False) -> str`），README 的「对外契约」
一节给出全部语义：大小写折叠（`str.casefold()`）、变音符号去除
（NFD 后删组合符号再 NFC）、可选的全角 → 半角宽度折叠，以及首尾空白去除。

折叠管线（顺序即幂等的保证）：

1. ``width=True`` 时做宽度映射（U+FF01..U+FF5E → U+0021..U+007E，
   U+3000 → U+0020）；
2. ``str.casefold()``：小写化并展开连字（``ß → ss``、``ﬃ → ffi``），
   ``İ`` 在此变成 ``i + U+0307``，交给第 3 步清掉；
3. NFD 分解，删除所有 ``unicodedata.combining(ch) != 0`` 的字符，再 NFC
   合成回来——结果只含 starter（谚文 jamo 的 ccc 为 0，会被原样保留并
   确定性重组），所以再折一次不会变化；
4. ``str.strip()`` 去首尾空白（既有冻结行为）。
"""

from __future__ import annotations

import unicodedata

_FULLWIDTH_LOW = 0xFF01
_FULLWIDTH_HIGH = 0xFF5E
_FULLWIDTH_OFFSET = 0xFEE0
_IDEOGRAPHIC_SPACE = "\u3000"


def _fold_width(s: str) -> str:
    """全角 ASCII（U+FF01..U+FF5E）→ 半角，U+3000 → 普通空格。

    刻意只做契约点名的两段映射；半角片假名（U+FF65 起）等保持原样。
    """
    chars = []
    for ch in s:
        code = ord(ch)
        if _FULLWIDTH_LOW <= code <= _FULLWIDTH_HIGH:
            chars.append(chr(code - _FULLWIDTH_OFFSET))
        elif ch == _IDEOGRAPHIC_SPACE:
            chars.append(" ")
        else:
            chars.append(ch)
    return "".join(chars)


def _strip_marks(s: str) -> str:
    """NFD 分解后删除组合符号，再 NFC 合成回来。"""
    decomposed = unicodedata.normalize("NFD", s)
    stripped = "".join(
        ch for ch in decomposed if unicodedata.combining(ch) == 0
    )
    return unicodedata.normalize("NFC", stripped)


def fold(s: str, *, width: bool = False) -> str:
    """返回 ``s`` 的折叠键。"""
    if width:
        s = _fold_width(s)
    s = s.casefold()
    s = _strip_marks(s)
    return s.strip()
