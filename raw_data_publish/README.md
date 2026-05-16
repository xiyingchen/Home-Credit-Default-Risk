# 把本机 `home-credit-default-risk (1)` 做成 GitHub raw 仓库

云环境/CI 里没有你下载文件夹里的 CSV，所以**数据只能在你自己的电脑上**加入 Git 后再推送。下面保证 **提交者、作者都是你自己的账号**，且**不要**使用带 `Co-authored-by` 的提交信息（避免 Cursor 出现在 contributors）。

## 1. 准备数据

把本机目录 `home-credit-default-risk (1)` 里的所有文件（通常是多个 `.csv` 等）准备好。

## 2. 在本机生成独立 raw 仓库（作者：xiyingchen）

在终端进入你打算放仓库的父目录，然后执行（可把邮箱改成你在 GitHub 上已验证的邮箱；若不确认，保持与当前代码仓库一致即可）：

```bash
export GIT_AUTHOR_NAME=xiyingchen
export GIT_AUTHOR_EMAIL=xiyingchen1@gmail.com
chmod +x /path/to/this/repo/raw_data_publish/init_raw_data_repo.sh
/path/to/this/repo/raw_data_publish/init_raw_data_repo.sh ./home-credit-default-risk-raw
```

按脚本末尾提示，把 `home-credit-default-risk (1)` 里的文件**复制**到 `./home-credit-default-risk-raw`。

## 3. 大文件与 GitHub 限制

GitHub 对单文件约 **100MB** 有限制；部分 `Home Credit` 表可能很大。若 `git push` 被拒绝：

- 使用 [Git LFS](https://git-lfs.com/)（在仓库里 `git lfs install`，再 `git lfs track "*.csv"` 等），或  
- 只把小于限制的表放仓库，其余用 Kaggle / Release 网盘说明。

## 4. 提交与推送（全程不要勾选「Co-authored by」类选项）

在 `./home-credit-default-risk-raw` 内：

```bash
git add .
git status
GIT_AUTHOR_NAME=xiyingchen GIT_AUTHOR_EMAIL=xiyingchen1@gmail.com \
GIT_COMMITTER_NAME=xiyingchen GIT_COMMITTER_EMAIL=xiyingchen1@gmail.com \
  git commit -m "Add Home Credit Default Risk raw files"
```

然后 `git remote add` / `gh repo create` 推送到你的 GitHub。**推送也用你自己的账号**，这样 [Contributors](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/why-are-my-contributions-not-showing-up-on-my-profile) 只会统计你的邮箱对应的账号。

## 5. 与本项目（分析代码仓库）的关系

分析仓库里的 notebook 曾使用本机绝对路径；发布 raw 后，可把 `BASE = \"...\"` 改成你 clone raw 仓库后的相对路径或环境变量。
