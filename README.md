<div align="center">

<img src="app_icon.png" alt="logo" width="120" height="auto" />

# Project K
### The Ultimate Scrcpy GUI Tool

[![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Scrcpy](https://img.shields.io/badge/Powered%20By-Scrcpy-orange?style=for-the-badge)](https://github.com/Genymobile/scrcpy)

**Control your Android device from your PC with high performance and low latency.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Shortcuts](#-shortcuts) • [Troubleshooting](#-troubleshooting)

</div>

---

## 🚀 Overview

**Project K** is a modern, feature-rich GUI wrapper for [Scrcpy](https://github.com/Genymobile/scrcpy). It simplifies the process of mirroring and controlling your Android device by providing a user-friendly interface for all advanced settings. Whether you are a gamer, a streamer, or a developer, Project K offers the flexibility you need.

## ✨ Features

| Category | Features |
| :--- | :--- |
| **📺 Visuals** | • Support for **H.265** and **AV1** codecs<br>• Resolutions up to **1600p**<br>• Bitrates up to **50 Mbps**<br>• Max FPS up to **120 FPS** (or uncapped) |
| **🎮 Performance** | • **Zero Latency** modes for gaming<br>• **OpenGL** & **Direct3D** rendering options<br>• Configurable buffering (0ms - 400ms) |
| **🔊 Audio** | • Stream audio to PC<br>• Duplicate audio (PC + Phone)<br>• Mute device while mirroring |
| **🛠 Tools** | • **Screen Recording** to MP4<br>• Turn screen off on launch<br>• Stay Awake mode<br>• Always on Top |
| **🔌 Connectivity** | • Auto-detect connected devices<br>• Wireless support (via TCP/IP setup in ADB)<br>• "Kill ADB" emergency switch |

## � Installation

### Option 1: Standalone Executable (Recommended)
1.  Download the latest release.
2.  Extract the folder.
3.  Run `ProjectK.exe`.
    *   *Note: Ensure `adb.exe` and `scrcpy.exe` are in the same folder (included in the release).*

## 🎮 Usage Guide

### Quick Presets
Don't want to mess with settings? Use the **Quick Presets** in the "Quality" tab:

*   🔴 **YouTube/Stream**: Stable 1080p, 60 FPS, 8 Mbps (Best for consistency).
*   🟢 **Gaming**: 720p, 90 FPS, Low Latency, No Buffer (Best for responsiveness).
*   🟠 **Low End PC**: 480p, 30 FPS, Low Bitrate (Best for older hardware).

### Recording
1.  Go to the **Tools** tab.
2.  Check **"Record Screen to File"**.
3.  Click "Launch".
4.  Choose where to save the `.mp4` file.

## ⌨️ Common Shortcuts (Scrcpy)

| Action | Shortcut (PC) |
| :--- | :--- |
| **Switch Fullscreen** | `Alt` + `f` |
| **Resize to Fit** | `Alt` + `w` |
| **Home Button** | `Alt` + `h` |
| **Back Button** | `Alt` + `b` |
| **App Switcher** | `Alt` + `s` |
| **Turn screen off** | `Alt` + `o` |
| **Volume Up/Down** | `Alt` + `↑` / `Alt` + `↓` |

## ❓ Troubleshooting

*   **No Devices Found?**
    *   Ensure **USB Debugging** is enabled on your phone.
    *   Connect via USB usage data cable (not just charging).
    *   Click "Refresh Devices" in the Dashboard.

*   **Lag or High Latency?**
    *   Try the "Gaming" preset.
    *   Reduce Resolution to 720p or 1080p.
    *   Switch "Video Codec" to H.264 if your PC struggles with H.265.

## 👤 Author

**@piyushkadam96k**

---

<div align="center">
  <sub>Built with ❤️ using Python & CustomTkinter</sub>
</div>
