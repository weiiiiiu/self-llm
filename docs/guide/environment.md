# 环境配置指南

本指南介绍如何配置大模型开发所需的基础环境，包括 pip、conda 换源和 AutoDL 端口配置。

## pip 换源

在国内使用 pip 安装包时，使用镜像源可以大幅提升下载速度。

更多详细内容可移步至 [MirrorZ Help](https://help.mirrors.cernet.edu.cn/) 查看。

### 临时使用镜像源

安装单个包时临时使用镜像源：

```bash
pip install -i https://mirrors.cernet.edu.cn/pypi/web/simple some-package
```

::: tip 提示
将 `some-package` 替换为你需要安装的包名。
:::

### 设置默认镜像源

升级 pip 到最新版本（>=10.0.0）后进行配置：

```bash
# 升级 pip
python -m pip install --upgrade pip

# 设置默认镜像源
pip config set global.index-url https://mirrors.cernet.edu.cn/pypi/web/simple
```

如果 pip 默认源的网络连接较差，可以临时使用镜像源升级：

```bash
python -m pip install -i https://mirrors.cernet.edu.cn/pypi/web/simple --upgrade pip
```

### 常用镜像源

| 镜像源 | 地址 |
|--------|------|
| 清华大学 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple/ |
| 中国科技大学 | https://pypi.mirrors.ustc.edu.cn/simple/ |
| 教育网 | https://mirrors.cernet.edu.cn/pypi/web/simple |

## conda 换源

镜像站提供了 Anaconda 仓库与第三方源（conda-forge、pytorch 等）。各系统都可以通过修改用户目录下的 `.condarc` 文件来使用镜像站。

### .condarc 文件位置

不同系统下的 `.condarc` 目录：

- **Linux**: `${HOME}/.condarc`
- **macOS**: `${HOME}/.condarc`
- **Windows**: `C:\Users\<YourUserName>\.condarc`

::: warning 注意
Windows 用户无法直接创建名为 `.condarc` 的文件，可先执行 `conda config --set show_channel_urls yes` 生成该文件之后再修改。
:::

### 快速配置

```bash
cat <<'EOF' > ~/.condarc
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
EOF
```

### 验证配置

```bash
# 查看当前配置
conda config --show-sources

# 清除索引缓存
conda clean -i

# 测试安装
conda install numpy
```

## AutoDL 端口配置

在 AutoDL 平台上开发时，需要将容器内的端口映射到本地浏览器访问。

### 端口映射步骤

1. 在 AutoDL 控制台找到"自定义服务"
2. 输入容器内端口（如 6006）
3. 获取映射后的 URL（如 `http://localhost:6006` 或 AutoDL 提供的公网地址）

![端口映射示意图](/models/General-Setting/pic/端口映射.png)

### 常用端口

| 服务类型 | 默认端口 | 用途 |
|---------|---------|------|
| Streamlit | 6006 | WebDemo 部署 |
| Gradio | 7860 | 交互式界面 |
| FastAPI | 8000/6006 | API 服务 |
| Jupyter | 8888 | Notebook |
| TensorBoard | 6006 | 训练可视化 |

### 在代码中指定端口

**Streamlit:**
```bash
streamlit run app.py --server.port 6006
```

**FastAPI:**
```python
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=6006)
```

**Gradio:**
```python
demo.launch(server_name="0.0.0.0", server_port=6006)
```

::: tip 提示
在 AutoDL 上开发时，推荐统一使用 6006 端口，这是 AutoDL 默认开放的端口。
:::

## GPU 环境检查

配置完环境后，验证 GPU 是否可用：

```bash
# 检查 CUDA 版本
nvidia-smi

# Python 中检查
python -c "import torch; print(torch.cuda.is_available())"
python -c "import torch; print(torch.cuda.device_count())"
python -c "import torch; print(torch.cuda.get_device_name(0))"
```

## 下一步

环境配置完成后，继续学习：

- [模型下载](/guide/download) - 了解如何下载各种开源模型
- [模型教程](/models/) - 开始部署和使用模型
- [贡献指南](/guide/contribute) - 参与项目贡献
