"""textfold.fold —— 折叠键的实现。

对外签名已定死（`fold(s, *, width=False) -> str`），README 的「对外契约」
一节给出全部语义：

1. 大小写折叠走 ``str.casefold()``（含 ``ß → ss``、``ﬁ → fi`` 等展开）；
2. 变音符号去除：NFD 分解后删掉全部组合记号（``unicodedata.combining`` 非零），
   再 NFC 合成回来；
3. ``width=True`` 时把全角 ASCII（``U+FF01..U+FF5E``）与全角空格 ``U+3000``
   折成半角；``width=False`` 时全角字符原样保留；
4. 保留内部标点与空白，仅去除首尾空白（既有冻结行为）。

整个管线对其自身的输出是幂等的：``fold(fold(s)) == fold(s)``。
"""

from __future__ import annotations

import unicodedata

# U+FF01..U+FF5E（全角 ASCII 可打印区）一一对应到 U+0021..U+007E，
# 另加 U+3000 全角空格 → U+0020。str.translate 的码位表，构建一次即可复用。
_FULLWIDTH_MAP = {0xFF01 + offset: 0x0021 + offset for offset in range(0x5E)}
_FULLWIDTH_MAP[0x3000] = 0x0020
_FULLWIDTH_TABLE = str.maketrans(_FULLWIDTH_MAP)


def _fold_width(s: str) -> str:
    """全角 → 半角：全角 ASCII 与 U+3000，其余字符不动。"""
    return s.translate(_FULLWIDTH_TABLE)


def _strip_marks(s: str) -> str:
    """NFD 分解后删除组合记号，再 NFC 合成回来。"""
    decomposed = unicodedata.normalize("NFD", s)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return unicodedata.normalize("NFC", stripped)


def fold(s: str, *, width: bool = False) -> str:
    """返回 ``s`` 的折叠键。"""
    if width:
        s = _fold_width(s)
    s = s.casefold()
    s = _strip_marks(s)
    return s.strip()
