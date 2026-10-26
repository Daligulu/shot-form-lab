# 🏀 Shot Form Lab · 投篮姿势动态跟踪

用一段普通手机视频分析投篮姿势：**MediaPipe 姿态估计 + 出手片段自动检测 + 关节角度规则引擎**，全部在浏览器本地运行，视频不上传任何服务器。

**在线演示**：见下方「运行方式」——因为 MediaPipe 模型需本地托管，建议直接本地运行。

## 功能

- 📤 上传投篮视频（支持 iPhone `.mov` / `.mp4`，iOS Safari 兼容）
- 🔍 **自动检测出手片段**：在全片（运球、跑动、多人画面）中定位每一次投篮出手
  - 候选帧：手腕显著抬高（< 全片中位高度 82%）且肘角 > 150°
  - 确认：前 2 秒内存在「下沉蓄力 → 急速上举」V 型手腕轨迹，且肘角张开速度 > 120°/s
  - 去重：0.8s 内连续帧合并为同一次出手
- 📐 逐次出手输出指标：**出手肘角 / 出手膝角 / 出手点高度（占画幅）**
- 🦴 实时骨架叠加可视化（33 关键点）
- 💡 基于 BEEF 原则（Balance / Eyes / Elbow / Follow-through）的改进建议

## 技术方案（为什么这么选）

| 组件 | 选择 | 理由 |
|---|---|---|
| 姿态估计 | MediaPipe Pose Landmarker (lite) | 手机浏览器可实时跑，33 关键点，免训练 |
| 目标检测（规划） | YOLO | 球/篮筐检测，颜色法在复杂灯光下失效 |
| 动作判定 | 关键点规则引擎 | 几何可解释、零训练成本；比 ST-GCN 等动作识别模型轻得多 |
| 部署 | 纯静态页面 | 模型本地托管（`cdn/`），不依赖被墙 CDN |

## 运行

```bash
git clone https://github.com/Daligulu/shot-form-lab.git
cd shot-form-lab
python3 gz_server.py        # 或 python3 -m http.server 8791（无 gzip，模型加载略慢）
# 打开 http://127.0.0.1:8791
```

> `cdn/` 内已包含 MediaPipe wasm 与 pose_landmarker_lite 模型（Apache-2.0，Google MediaPipe），无需外网。

## 目录结构

```
├── index.html        # 单页应用：界面 + MediaPipe 管线 + 出手检测规则引擎
├── gz_server.py      # 带 gzip 的静态服务器（wasm 传输量 -70%）
├── cdn/              # 本地托管的 MediaPipe wasm + 模型
├── test/             # 合成测试视频与检测逻辑验证
├── tunnel_sup.sh     # 免费隧道看门狗（开发期对外演示用）
└── keepwarm.sh       # 隧道保活心跳
```

## 调研参考的开源项目

- [chonyy/AI-basketball-analysis](https://github.com/chonyy/AI-basketball-analysis) — Faster R-CNN + OpenPose，经典但重
- [knolen923/ai-basketball-shot-trainer](https://github.com/knolen923/ai-basketball-shot-trainer) — MediaPipe 实时肘角检测
- [Ez-C99/my-computer-vision-jumpshot](https://github.com/Ez-C99/my-computer-vision-jumpshot) — MediaPipe + Norfair 跳投分析
- [rayford295/swingform-ai](https://github.com/rayford295/swingform-ai) — 关键点 + 光流，MIT
- [mpJunot/ShotPrediction](https://github.com/mpJunot/ShotPrediction) — 投篮阶段检测 + 轨迹预测

## Roadmap

- [ ] YOLO 接入球/篮筐检测（进球判定、前臂倾角 45–55°）
- [ ] 阶段细分：持球 / 下沉 / 上举 / 出手 / 跟随
- [ ] 跨视频对比（训练前后姿势变化）
- [ ] 3D 姿态（MediaPipe BlazePose Depth）

## License

MIT（项目代码）。`cdn/` 内 MediaPipe 资源遵循 [Apache-2.0](https://github.com/google-ai-edge/mediapipe/blob/master/LICENSE)。
