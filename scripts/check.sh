#!/usr/bin/env bash
# textfold 固定验收入口的薄封装。**别改这个文件。**
#
#   bash scripts/check.sh              # 跑全部 9 个场景
#   bash scripts/check.sh -list        # 列出全部场景
#   bash scripts/check.sh --only case
set -uo pipefail

cd "$(dirname "$0")/.."

exec python3 check/check.py "$@"
