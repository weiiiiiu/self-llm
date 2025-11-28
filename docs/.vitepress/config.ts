import { defineConfig } from "vitepress";
import sidebarConfig from "./sidebar_config.json";

// 处理 sidebar 链接，将 /models/ 和 /examples/ 转换为 /guide/models/ 和 /guide/examples/
function transformSidebarLinks(items: any[]): any[] {
  return items.map((item) => {
    const newItem = { ...item };
    if (newItem.link) {
      if (newItem.link.startsWith("/models/")) {
        newItem.link = "/guide" + newItem.link;
      } else if (newItem.link.startsWith("/examples/")) {
        newItem.link = "/guide" + newItem.link;
      }
    }
    if (newItem.items) {
      newItem.items = transformSidebarLinks(newItem.items);
    }
    return newItem;
  });
}

// https://vitepress.dev/reference/site-config
export default defineConfig({
  // 基础配置
  title: "开源大模型食用指南",
  description:
    "围绕开源大模型、针对国内初学者、基于 Linux 平台的中国宝宝专属大模型教程",
  lang: "zh-CN",

  // 如果部署到 Cloudflare Pages，使用根路径
  base: "/",
  // 如果部署到 GitHub Pages，取消注释下面这行
  // base: '/self-llm/',

  // 路径重写：将 models/ 和 examples/ 重写到 guide/ 下
  rewrites: {
    "models/:path*": "guide/models/:path*",
    "examples/:path*": "guide/examples/:path*",
  },

  // 主题配置
  themeConfig: {
    // Logo
    logo: "/images/head-img.png",

    // 导航栏
    nav: [
      { text: "首页", link: "/" },
      { text: "快速开始", link: "/guide/environment" },
      {
        text: "相关资源",
        items: [
          {
            text: "Tiny-Universe",
            link: "https://github.com/datawhalechina/tiny-universe",
          },
          {
            text: "llm-universe",
            link: "https://github.com/datawhalechina/llm-universe",
          },
          {
            text: "so-large-llm",
            link: "https://github.com/datawhalechina/so-large-lm",
          },
          {
            text: "Happy-LLM",
            link: "https://github.com/datawhalechina/happy-llm",
          },
        ],
      },
    ],

    // 侧边栏 - 统一配置，所有路径使用同一个侧边栏
    sidebar: (() => {
      const commonSidebar = [
        {
          text: "快速开始",
          items: [
            { text: "环境配置", link: "/guide/environment" },
            { text: "模型下载", link: "/guide/download" },
            { text: "贡献指南", link: "/guide/contribute" },
          ],
        },
        {
          text: "模型教程",
          collapsed: false,
          items: transformSidebarLinks(sidebarConfig.models_sidebar),
        },
        {
          text: "示例项目",
          collapsed: true,
          items: [{ text: "示例项目列表", link: "/guide/examples/" }],
        },
      ];
      return {
        "/guide/models/": commonSidebar,
        "/guide/examples/": commonSidebar,
        "/guide/": commonSidebar,
      };
    })(),

    // 社交链接
    socialLinks: [
      { icon: "github", link: "https://github.com/datawhalechina/self-llm" },
    ],

    // 页脚
    footer: {
      message: "基于 Apache-2.0 许可发布",
      copyright: "Copyright © 2023-present Datawhale",
    },

    // 编辑链接
    editLink: {
      pattern: "https://github.com/datawhalechina/self-llm/edit/master/:path",
      text: "在 GitHub 上编辑此页",
    },

    // 最后更新时间
    lastUpdated: {
      text: "最后更新于",
      formatOptions: {
        dateStyle: "short",
        timeStyle: "medium",
      },
    },

    // 本地搜索
    search: {
      provider: "local",
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: "搜索文档",
                buttonAriaLabel: "搜索文档",
              },
              modal: {
                noResultsText: "无法找到相关结果",
                resetButtonTitle: "清除查询条件",
                footer: {
                  selectText: "选择",
                  navigateText: "切换",
                  closeText: "关闭",
                },
              },
            },
          },
        },
      },
    },

    // 文档页脚文本配置
    docFooter: {
      prev: "上一页",
      next: "下一页",
    },

    // 大纲配置
    outline: {
      level: [2, 3],
      label: "页面导航",
    },

    // 返回顶部文本
    returnToTopLabel: "回到顶部",

    // 侧边栏文本
    sidebarMenuLabel: "菜单",

    // 深色模式文本
    darkModeSwitchLabel: "主题",
    lightModeSwitchTitle: "切换到浅色模式",
    darkModeSwitchTitle: "切换到深色模式",
  },

  // Markdown 配置
  markdown: {
    lineNumbers: true, // 代码块显示行号
    theme: {
      light: "github-light",
      dark: "github-dark",
    },
    // 允许 HTML 标签
    html: true,
  },

  // 头部配置（SEO）
  head: [
    ["link", { rel: "icon", href: "/images/head-img.png" }],
    ["meta", { name: "author", content: "Datawhale" }],
    [
      "meta",
      {
        name: "keywords",
        content: "大模型, LLM, Qwen, ChatGLM, InternLM, 教程, 微调, 部署",
      },
    ],
    ["meta", { property: "og:title", content: "开源大模型食用指南" }],
    [
      "meta",
      {
        property: "og:description",
        content:
          "针对国内初学者的开源大模型教程，包含 49+ 主流模型的部署、微调、应用指南",
      },
    ],
    ["meta", { property: "og:type", content: "website" }],
    [
      "meta",
      { name: "viewport", content: "width=device-width, initial-scale=1.0" },
    ],
  ],

  // 构建配置
  cleanUrls: true, // 生成干净的 URL（无 .html 后缀）

  // 忽略死链检查（因为有些文档可能引用外部或临时链接）
  ignoreDeadLinks: true,

  // Vue 编译器选项
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => tag.includes("-"),
      },
    },
  },

  // 构建配置
  vite: {
    build: {
      chunkSizeWarningLimit: 1600,
      rollupOptions: {
        external: [],
        onwarn(warning, warn) {
          // Ignore asset resolution warnings
          if (
            warning.code === "UNRESOLVED_IMPORT" &&
            warning.message.includes("images/")
          ) {
            return;
          }
          warn(warning);
        },
      },
    },
    assetsInclude: [
      "**/*.png",
      "**/*.jpg",
      "**/*.jpeg",
      "**/*.gif",
      "**/*.svg",
    ],
  },
});
