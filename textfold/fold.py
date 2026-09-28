"""textfold.fold —— 折叠键的实现。

对外签名已定死（`fold(s, *, width=False) -> str`），README 的「对外契约」
一节给出全部语义。当前实现只覆盖其中的小写化与去首尾空白两部分。
"""

from __future__ import annotations


def fold(s: str, *, width: bool = False) -> str:
    """返回 ``s`` 的折叠键。"""
    return s.lower().strip()
