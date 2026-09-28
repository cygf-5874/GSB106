# textfold

`textfold` 是一个纯标准库的**文本折叠键**库：把同一段文本在不同写法下的差异抹平，
产出一个用于查表 / 去重的「折叠键」。

- 语言 / 运行：Python 3，只用标准库（`unicodedata`；`unittest` 跑用例），无第三方依赖。
- 自检：`bash scripts/check.sh`（内部调用 `check/check.py`，那是固定验收程序，**别改**）。
- 既有用例：`python3 -m unittest discover -s tests`。

## 怎么跑

```bash
python3 -m unittest discover -s tests   # 既有用例
bash scripts/check.sh                    # 固定验收（9 个场景）
bash scripts/check.sh -list              # 列出全部场景
bash scripts/check.sh --only width       # 只跑一组
```

前提：Python 3.7+（本仓库按 3.13 验证）。不引入任何第三方依赖。

## 目录

```
.
├── .gitattributes
├── .gitignore
├── README.md
├── PROMPT.md             本题的 User Prompt（逐字）
├── textfold/__init__.py  包出口
├── textfold/fold.py      折叠实现
├── tests/test_fold.py    既有 12 个用例（当前全绿）
├── check/check.py        固定验收程序：9 个场景（勿改）
└── scripts/check.sh      薄封装
```

## 对外契约（9 条）

1. `fold(s: str, *, width: bool = False) -> str`：产出**折叠键**，用于查表 / 去重；
2. **大小写折叠**用 `str.casefold()` 的原语语义，但必须覆盖 `ß → ss`、`ﬃ → ffi`、`İ`/`ı` 的边界；
3. **变音符号去除**：NFD 分解后删除 `unicodedata.combining(ch) != 0` 的字符，再 NFC 合成回来；
4. 折叠结果**必须是幂等的**：`fold(fold(s)) == fold(s)` 对任意输入成立；
5. `width=True` 时额外做**全角 → 半角**（含 `U+FF01..U+FF5E` 的宽度映射与 `U+3000` 空格）；
6. `width=False` 时**不得**改动全角字符（保持原样）；
7. 折叠不得改变**非拉丁**字符（中文、阿拉伯文、emoji 原样保留）；
8. 保留标点与空白，只做第 2/3/5 条列出的变换；
9. 结果与 `dict` 迭代顺序无关，不得依赖 `locale`；同一输入任意多次调用结果相同。

## 当前状态 / 本次要补的一层

`fold` 已经能做**小写化 + 去首尾空白**：`tests/test_fold.py` 的 12 个用例全绿，
`check/check.py` 里只依赖这一层的场景也通过。

还缺三块（契约 3 / 4 / 5、6）：

- **变音符号去除**：把带组合符号的写法归一到无符号形式（契约 3）；
- **幂等性**：任意输入折叠一次即落到规范形式，再折不变（契约 4）；
- **宽度折叠**：`width=True` 时全角 → 半角（含 `U+3000`），`width=False` 时不动全角（契约 5 / 6）。

> 首尾空白按既有行为继续去除（`tests/test_fold.py` 已冻结这一行为），本次不动。
> 契约第 8 条指的是**内部**标点与空白不受额外变换影响。

约束：不改 `check/`；对外函数名与签名不许改；`tests/test_fold.py` 里的既有用例一条都不许删或改；
只用标准库，不许引入任何第三方包，不许用 `locale`。

## 验收

`check/` 是固定验收程序，**不要修改**。场景分五组，共 9 个：

| 组 | 场景 | 覆盖 |
| --- | --- | --- |
| `case` | `expansions` | 契约 2：`ß`/`ﬃ`/`ﬂ` 等展开 |
| `case` | `dotted-i-boundary` | 契约 2：`İ`/`ı`/`I` 的边界 |
| `mark` | `removes-combining` | 契约 3：删组合符号 |
| `mark` | `nfc-roundtrip` | 契约 3：去符号后 NFC 合成回来 |
| `idem` | `any-input` | 契约 4：任意输入幂等 |
| `idem` | `second-pass-stable` | 契约 4：一次折叠即到规范形式 |
| `width` | `on-folds-fullwidth` | 契约 5：全角 → 半角（含 `U+3000`） |
| `width` | `off-keeps-fullwidth` | 契约 6：`width=False` 不动全角 |
| `other` | `keeps-non-latin` | 契约 7：中日韩 / 阿拉伯 / emoji 原样保留 |

```bash
python3 -m unittest discover -s tests   # 退出码 0，12 个既有用例全绿
bash scripts/check.sh                    # 退出码 0，9 个场景全过
```

## User Prompt

```
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
```
