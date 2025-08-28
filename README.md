<div align="center">
  <p>
    <a href="https://ultralytics.com/" target="_blank">
      <img width="1024", src="https://github.com/ultralytics/assets/raw/main/logo/Ultralytics_Logotype_Reverse.svg"></a>
  </p>

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja-JP.md) | [한국어](README.ko-KR.md) | [العربية](README.ar-EG.md) | [Deutsch](README.de-DE.md) | [Français](README.fr-FR.md) | [Español](README.es-ES.md) | [Português](README.pt-BR.md) | [Türkçe](README.tr-TR.md) | [Tiếng Việt](README.vi-VN.md) | [हिंदी](README.hi-IN.md) | [עברית](README.he-IL.md)

<br>
  <a href="https://github.com/ultralytics/profile/actions/workflows/ci.yaml"><img src="https://github.com/ultralytics/profile/actions/workflows/ci.yaml/badge.svg" alt="Ultralytics CI"></a>
  <a href="https://zenodo.org/badge/latestdoi/264818686"><img src="https://zenodo.org/badge/264818686.svg" alt="Ultralytics Profile Citation"></a>
  <a href="https://hub.docker.com/r/ultralytics/ultralytics"><img src="https://img.shields.io/docker/pulls/ultralytics/ultralytics?logo=docker" alt="Docker Pulls"></a>
  <a href="https://ultralytics.com/discord"><img alt="Discord" src="https://img.shields.io/discord/1089800235347353640?logo=discord&logoColor=white&label=Discord&color=blue"></a>
  <br>
  <a href="https://console.paperspace.com/github/ultralytics/profile"><img src="https://assets.paperspace.io/img/gradient-badge.svg" alt="Run on Gradient"></a>
  <a href="https://colab.research.google.com/github/ultralytics/profile"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
  <a href="https://www.kaggle.com/ultralytics/profile"><img src="https://kaggle.com/static/images/open-in-kaggle.svg" alt="Open In Kaggle"></a>
</div>

# Ultralytics Profile 🚀

A simple, powerful tool for profiling any Python code or command execution with detailed performance analysis.

## 📦 Installation

```bash
pip install -e .
```

## 🚀 Usage

### Command Line

```bash
# Profile Python scripts
profile python script.py

# Profile Python modules
profile python -c "import ultralytics; print('done')"

# Profile CLI tools
profile yolo predict model=yolo11n.pt source=image.jpg

# Profile bash scripts
profile bash script.sh
```

### Python API

```python
from ultralytics_profile import profile_command

# Profile any command
timings = profile_command("python script.py")

# Profile with custom analysis depth
timings = profile_command("yolo predict model=yolo11n.pt", top_n=20)
```

## ✨ Features

- **🌐 Universal profiling**: Works with any Python code or bash commands
- **📊 Detailed analysis**: Shows execution time, call counts, and averages
- **🎯 Clean output**: Organized performance reports with hotspot identification
- **🔄 No circular imports**: Runs commands in separate processes to avoid conflicts
- **⚡ Simple CLI**: Just prefix any command with `profile`

## 💡 Examples

```bash
# Profile YOLO11 inference
profile yolo predict model=yolo11n.pt source=https://ultralytics.com/images/bus.jpg

# Profile custom Python code  
profile python -c "import torch; x = torch.randn(1000, 1000); y = x @ x.T"

# Profile installation
profile pip install numpy

# Profile tests
profile python -m pytest tests/
```

## 📈 Output

The profiler provides detailed performance analysis including:

- **🐌 Slowest functions**: Functions consuming the most execution time
- **🔥 Most called functions**: Functions with highest call frequency  
- **⏱️ Timing details**: Cumulative time, self time, call counts, and averages
- **📁 File context**: Source file and line number information

## 🤝 Contribute

We love your input! We want to make contributing to Ultralytics Profile as easy and transparent as possible. Please see our [Contributing Guide](CONTRIBUTING.md) to get started, and fill out our [survey](https://ultralytics.com/survey?utm_source=github&utm_medium=social&utm_campaign=Survey) to send us feedback on your experiences. Thank you 🙏 to all our contributors!

<a href="https://github.com/ultralytics/profile/graphs/contributors">
<img width="100%" src="https://github.com/ultralytics/profile/graphs/contributors">
</a>

## 📄 License

Ultralytics offers two licensing options to accommodate diverse use cases:

- **AGPL-3.0 License**: This [OSI-approved](https://opensource.org/licenses/) open-source license is ideal for students and enthusiasts, promoting open collaboration and knowledge sharing. See the [LICENSE](https://github.com/ultralytics/profile/blob/main/LICENSE) file for more details.
- **Enterprise License**: Designed for commercial use, this license permits seamless integration of Ultralytics software and AI models into commercial goods and services, bypassing the open-source requirements of AGPL-3.0. If your scenario involves embedding our solutions into a commercial offering, reach out through [Ultralytics Licensing](https://ultralytics.com/license).

## 📞 Contact

For Ultralytics bug reports and feature requests please visit [GitHub Issues](https://github.com/ultralytics/profile/issues), and join our [Discord](https://ultralytics.com/discord) community for questions and discussions!

<br>
<div align="center">
  <a href="https://github.com/ultralytics" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-github.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://www.linkedin.com/company/ultralytics" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-linkedin.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://twitter.com/ultralytics" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-twitter.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://youtube.com/ultralytics" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-youtube.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://www.tiktok.com/@ultralytics" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-tiktok.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://www.instagram.com/ultralytics/" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-instagram.png" width="2%" alt="" /></a>
  <img src="https://github.com/ultralytics/assets/raw/main/social/logo-transparent.png" width="2%" alt="" />
  <a href="https://ultralytics.com/discord" style="text-decoration:none;">
    <img src="https://github.com/ultralytics/assets/raw/main/social/logo-social-discord.png" width="2%" alt="" /></a>
</div>
