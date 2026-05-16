#!/usr/bin/env bash
# Initialize a standalone Git repo for Home Credit raw CSVs on YOUR machine.
# Commit author/committer are set locally so they are only you (no Cursor co-author).
set -euo pipefail

TARGET_DIR="${1:-./home-credit-default-risk-raw}"
AUTHOR_NAME="${GIT_AUTHOR_NAME:-xiyingchen}"
AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-xiyingchen1@gmail.com}"

mkdir -p "${TARGET_DIR}"
cd "${TARGET_DIR}"

if [[ ! -d .git ]]; then
  git init -b main
fi

git config user.name "${AUTHOR_NAME}"
git config user.email "${AUTHOR_EMAIL}"

if [[ ! -f README.md ]]; then
  cat > README.md << 'EOF'
# Home Credit Default Risk — raw data mirror

原始数据来自 Kaggle：
https://www.kaggle.com/competitions/home-credit-default-risk/data

请将 `home-credit-default-risk (1)` 目录中的文件放在本仓库根目录后再提交。
EOF
fi

echo ""
echo "============================================================"
echo "  目标目录: $(pwd)"
echo "  下一步：把本机「home-credit-default-risk (1)」里的全部文件复制到此目录。"
echo "  若 CSV 单文件超过 ~100MB，请先配置 Git LFS（见 raw_data_publish/README.md）。"
echo "  然后执行："
echo "    git add ."
echo "    git status"
echo "    git commit -m \"Add Home Credit Default Risk raw files\""
echo "    gh repo create <你的仓库名> --public --source=. --remote=origin --push"
echo "    # 或: git remote add origin <url> && git push -u origin main"
echo "============================================================"
echo ""
