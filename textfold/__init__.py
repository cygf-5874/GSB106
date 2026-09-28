"""textfold — 文本折叠键（Python 3 标准库，无第三方依赖）。

对外只暴露一个函数 :func:`fold`，其契约写在仓库 README 的「对外契约」一节。
"""

from .fold import fold

__all__ = ["fold"]
