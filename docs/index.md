---
layout: home

hero:
  name: "开源大模型食用指南"
  text: "Open Source LLM User Guide"
  tagline: 针对国内初学者、基于 Linux 平台的大模型教程，涵盖 49+ 主流开源模型的部署、微调与应用
  image:
    src: /images/head-img.png
    alt: 开源大模型
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/environment
    - theme: alt
      text: 查看教程
      link: /models/
    - theme: alt
      text: GitHub
      link: https://github.com/datawhalechina/self-llm

features:
  - icon: 🚀
    title: 快速部署
    details: 提供 FastAPI、vLLM、WebDemo 等多种部署方式，支持命令行调用、在线 Demo 部署、API 服务搭建

  - icon: 🎯
    title: 高效微调
    details: 包含 LoRA、QLoRA、全量微调等多种方法，详细讲解参数设置、数据准备、训练流程

  - icon: 📚
    title: 丰富教程
    details: 涵盖 49+ 主流开源模型（Qwen、GLM、InternLM、LLaMA等），242+ 篇详细教程文档

  - icon: 🔧
    title: 实战案例
    details: 提供 Chat-嬛嬛、Tianji、AMChat 等完整应用案例，展示从数据到部署的全流程

  - icon: 🌏
    title: 国内优化
    details: 针对国内环境优化，提供模型下载镜像、pip 换源、AutoDL 平台配置等实用技巧

  - icon: 🤝
    title: 社区驱动
    details: 77+ 位核心贡献者，持续更新最新模型，欢迎所有人提出 Issue 和 PR
---

## 项目特点

本项目是一个围绕开源大模型、针对国内初学者、基于 Linux 平台的中国宝宝专属大模型教程。项目旨在简化开源大模型的部署、使用和应用流程，让更多的普通学生、研究者更好地使用开源大模型。

### 🎓 学习建议

建议学习路径：**环境配置 → 模型部署 → 模型微调**

- 环境配置是基础，模型部署是入门，微调是进阶
- 初学者推荐优先学习：**Qwen1.5**、**InternLM2**、**MiniCPM** 等模型
- 每个模型教程独立完整，可根据需求选择学习

### 📖 主要内容

1. **环境配置指南** - Linux 平台开源 LLM 环境配置，针对不同模型提供详细步骤
2. **部署教程** - 主流开源 LLM 的部署使用，包括 LLaMA、ChatGLM、InternLM 等
3. **应用指导** - 命令行调用、在线 Demo、LangChain 框架集成等
4. **微调方法** - 全量微调、LoRA、QLoRA、ptuning 等高效微调技术

### 🌟 项目亮点

- **标准化流程**：每个模型遵循统一的教程结构（FastAPI → WebDemo → LangChain → 微调）
- **详细文档**：每篇教程包含完整代码、配置说明、运行截图
- **配套资源**：提供数据集、参考代码、Docker 镜像
- **持续更新**：跟进最新开源模型，社区贡献者持续维护

## 快速导航

<div class="vp-card-grid">

### 🎯 通用设置
- [pip/conda 换源](/guide/environment)
- [模型下载方法](/guide/download)
- [贡献指南](/guide/contribute)

### 🔥 热门模型
- [Qwen 系列](/models/Qwen/)
- [GLM-4](/models/GLM-4/)
- [InternLM3](/models/InternLM3/)
- [Qwen3](/models/Qwen3/)

### 💡 示例项目
- [Chat-嬛嬛](/examples/Chat-嬛嬛/)
- [Tianji-天机](/examples/Tianji-天机/)
- [AMChat-高等数学](/examples/AMchat-高等数学/)

</div>

## 相关项目

如果您在学习完本项目后，希望进一步深入学习，可以参考 Datawhale 的其他项目：

- **[Happy-LLM](https://github.com/datawhalechina/happy-llm)** - 从零开始的大语言模型原理与实践
- **[Tiny-Universe](https://github.com/datawhalechina/tiny-universe)** - 手写 RAG、Agent 和 Eval
- **[llm-universe](https://github.com/datawhalechina/llm-universe)** - 动手学大模型应用开发
- **[so-large-llm](https://github.com/datawhalechina/so-large-lm)** - 大模型理论基础课程

## 贡献者

特别感谢 77+ 位核心贡献者对本项目的贡献！

项目负责人：宋志学（不要葱姜蒜）、邹雨衡

**项目的主要内容就是教程，让更多的学生和未来的从业者了解和熟悉开源大模型的食用方法！任何人都可以提出 issue 或是提交 PR，共同构建维护这个项目。**

想要深度参与的同学可以联系我们，我们会将你加入到项目的维护者中。

---

<div style="text-align: center; margin-top: 40px;">
  <p>⭐ 如果这个项目对你有帮助，请给我们一个 Star！</p>
  <a href="https://github.com/datawhalechina/self-llm" target="_blank">
    <img src="https://img.shields.io/github/stars/datawhalechina/self-llm?style=social" alt="GitHub stars">
  </a>
</div>
