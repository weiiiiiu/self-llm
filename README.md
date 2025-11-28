# VitePress 部署说明

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run docs:dev

# 构建
npm run docs:build

# 预览构建结果
npm run docs:preview
```

## 部署到 Cloudflare Pages

```bash
# 安装 Wrangler（首次）
npm install -g wrangler

# 登录（首次）
wrangler login

# 构建并部署
npm run docs:build
wrangler pages deploy docs/.vitepress/dist --project-name=self-llm
```

## 同步上游仓库

```bash
# 添加上游（首次）
git remote add upstream https://github.com/datawhalechina/self-llm.git

# 同步更新
git fetch upstream
git merge upstream/master
git push origin master
```

最后更新：2025-11-28
