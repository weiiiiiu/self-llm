# VitePress 部署说明

本文档说明如何将 self-llm 项目部署到 Cloudflare Pages 或 GitHub Pages。

## 项目结构

```
self-llm/
├── docs/                        # VitePress 文档目录
│   ├── .vitepress/
│   │   └── config.ts           # VitePress 配置
│   ├── index.md                # 首页
│   ├── guide/                  # 通用指南
│   ├── models -> ../models/    # 软链接到模型目录
│   ├── examples -> ../examples/# 软链接到示例目录
│   └── images -> ../images/    # 软链接到图片目录
├── package.json                # Node.js 依赖
└── .nojekyll                   # 禁用 Jekyll
```

## 本地开发

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run docs:dev
```

访问 http://localhost:5173 查看效果。

### 3. 构建生产版本

```bash
npm run docs:build
```

构建产物位于 `docs/.vitepress/dist/`。

### 4. 预览生产版本

```bash
npm run docs:preview
```

## 部署到 Cloudflare Pages（推荐）

### 方法一：通过 Cloudflare Dashboard

1. **登录 Cloudflare**

   - 访问 https://dash.cloudflare.com/
   - 选择 Workers & Pages

2. **创建新项目**

   - 点击 "Create application"
   - 选择 "Pages" 标签
   - 点击 "Connect to Git"

3. **连接 GitHub 仓库**

   - 授权 Cloudflare 访问 GitHub
   - 选择 `self-llm` 仓库
   - 点击 "Begin setup"

4. **配置构建设置**

   ```
   项目名称：self-llm（或自定义）
   生产分支：master
   框架预设：VitePress
   构建命令：npm run docs:build
   构建输出目录：docs/.vitepress/dist
   根目录：/（默认）
   Node.js 版本：18+
   ```

5. **保存并部署**
   - 点击 "Save and Deploy"
   - 首次构建约 2-3 分钟
   - 完成后获得域名：`https://self-llm.pages.dev`

### 方法二：使用 Wrangler CLI

```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 构建
npm run docs:build

# 部署
wrangler pages deploy docs/.vitepress/dist --project-name=self-llm
```

## 部署到 GitHub Pages

### 方法一：GitHub Actions（自动部署）

创建 `.github/workflows/deploy.yml`：

\`\`\`yaml
name: Deploy VitePress site to Pages

on:
push:
branches: [master]
workflow_dispatch:

permissions:
contents: read
pages: write
id-token: write

concurrency:
group: pages
cancel-in-progress: false

jobs:
build:
runs-on: ubuntu-latest
steps: - name: Checkout
uses: actions/checkout@v4
with:
fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build with VitePress
        run: npm run docs:build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

deploy:
environment:
name: github-pages
url: ${{ steps.deployment.outputs.page_url }}
needs: build
runs-on: ubuntu-latest
name: Deploy
steps: - name: Deploy to GitHub Pages
id: deployment
uses: actions/deploy-pages@v4
\`\`\`

### 方法二：手动部署

```bash
# 构建
npm run docs:build

# 进入构建产物目录
cd docs/.vitepress/dist

# 初始化 git
git init
git add -A
git commit -m 'deploy'

# 推送到 gh-pages 分支
git push -f git@github.com:YOUR-USERNAME/self-llm.git master:gh-pages

cd -
```

然后在 GitHub 仓库设置中：

1. Settings > Pages
2. Source: Deploy from a branch
3. Branch: gh-pages / root

## 已知问题及解决方案

### 问题 1：构建失败 - HTML 属性错误

**错误信息：**

```
Unquoted attribute value cannot contain U+0022 ("), U+0027 ('), U+003C (<), U+003D (=), and U+0060 (`)
```

**原因：**
某些 markdown 文档中的 HTML 标签格式不正确。

**已发现的问题文件：**

- `models/InternLM2/04-InternLM2-7B-chat Xtuner Qlora 微调.md` (第 261 行)
  - 错误：`<img ... width=1100" />`
  - 应改为：`<img ... width="1100" />`

**临时解决方案：**
在配置中排除有问题的文件，或修复原文件。

### 问题 2：软链接在 Windows 上无法工作

**解决方案：**
在 Windows 上，使用管理员权限创建软链接，或将文件复制到 docs 目录。

```powershell
# PowerShell（管理员权限）
New-Item -ItemType SymbolicLink -Path docs\models -Target ..\models
New-Item -ItemType SymbolicLink -Path docs\examples -Target ..\examples
New-Item -ItemType SymbolicLink -Path docs\images -Target ..\images
```

### 问题 3：图片无法加载

**解决方案：**
确保图片路径正确。VitePress 会自动处理相对路径，但跨目录引用需要验证。

### 问题 4：中文路径问题

**解决方案：**
某些文档使用了中文路径或文件名，在 URL 中会被编码。建议使用英文路径。

## 配置说明

### base 路径配置

**Cloudflare Pages：**

```typescript
base: "/";
```

**GitHub Pages：**

```typescript
base: "/self-llm/"; // 仓库名
```

在 `docs/.vitepress/config.ts` 中修改。

### 自定义域名

**Cloudflare Pages：**

1. 在 Cloudflare Pages 项目设置中
2. Custom domains > Add a custom domain
3. 按提示添加 CNAME 记录

**GitHub Pages：**

1. Settings > Pages > Custom domain
2. 输入域名
3. 在 DNS 提供商添加 CNAME 记录

## 性能优化

### 1. 构建优化

- 使用 npm ci 而非 npm install（CI 环境）
- 启用构建缓存（GitHub Actions 或 Cloudflare）
- 压缩图片资源

### 2. 运行时优化

- 启用 Cloudflare CDN 加速
- 使用 WebP 图片格式
- 配置浏览器缓存

### 3. SEO 优化

- 配置 meta 标签（已在 config.ts 中）
- 生成 sitemap.xml
- 添加 robots.txt

## 维护建议

### Fork 仓库同步

```bash
# 添加上游仓库
git remote add upstream https://github.com/datawhalechina/self-llm.git

# 同步更新
git fetch upstream
git merge upstream/master
git push origin master
```

Cloudflare Pages 会自动检测到 push 并重新构建部署。

### 监控构建状态

- **Cloudflare Pages**：在 Dashboard 查看部署历史和日志
- **GitHub Pages**：在 Actions 标签查看工作流运行状态

## 故障排查

### 构建失败

1. 检查 Node.js 版本（需要 18+）
2. 清除缓存：`rm -rf node_modules package-lock.json && npm install`
3. 查看详细错误日志

### 部署失败

1. 检查构建产物是否正确生成
2. 验证 GitHub/Cloudflare 权限设置
3. 检查分支名称是否正确

### 页面 404

1. 检查 base 路径配置
2. 验证软链接是否正确
3. 检查文件名和路径大小写

## 联系支持

如有问题，请：

1. 查看 [VitePress 官方文档](https://vitepress.dev/)
2. 提交 [GitHub Issue](https://github.com/datawhalechina/self-llm/issues)
3. 联系项目维护者

---

最后更新：2025-11-27
