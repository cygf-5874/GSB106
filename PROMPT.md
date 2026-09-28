搜索那边的同事要一套「折叠」规则：大小写、变音符号、全角半角都要能对上。
textfold 是 Python 3 的文本折叠库，只用标准库（`unicodedata`），构建不需要额外步骤，
自检走 `scripts/check.sh`（`check/` 是固定验收程序，别改），既有用例走
`python3 -m unittest discover -s tests`。

任务：按 README「本次要补的一层」，把变音符号、幂等、宽度三块做出来，让固定件全过。

验收：
- python3 -m unittest discover -s tests 全绿；
- python3 check/check.py 退出码 0，9 个场景全过（case 2 + mark 2 + idem 2 + width 2 + other 1）。

约束：
1. 不改 `check/`；可以新增模块。
2. 对外函数名与签名不许改；`tests/test_fold.py` 里的既有用例一条都不许删或改。
3. 只用标准库，不许引入任何第三方包，不许用 `locale`。
4. 折叠结果必须幂等。
