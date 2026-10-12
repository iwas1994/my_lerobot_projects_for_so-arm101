# my_lerobot_projects_for_so-arm101

## 1. プロジェクト概要（About This Repository）
このリポジトリ **my_lerobot_projects_for_so-arm101** は、  
Hugging Face LeRobot を用いて **SO-ARM101 ロボットアームの制御・データ収集・学習・実機適用を行う技術者向けプロジェクト集**です。

LeRobotは、ロボティクス研究者・開発者向けに設計された統合フレームワークであり、  
本リポジトリはその標準ワークフローを SO-ARM101 に最適化して実装しています。

LeRobot公式リポジトリ（仕様引用）：  
https://github.com/huggingface/lerobot

---

## 2. LeRobotとは（About LeRobot）
LeRobotは、ロボット制御・データセット管理・模倣学習・強化学習を統合的に扱う  
**Pythonネイティブのロボティクスライブラリ**です。

### 主な特徴
- **ハードウェア非依存 API**  
  統一された Robot クラスにより、異なるロボットを同一コードで扱える。
- **データセット形式（Parquet + MP4）**  
  高速・軽量なロボットデータ管理を実現。
- **SOTAポリシーの提供**  
  Diffusion Policy など実機転移可能なモデルを標準サポート。
- **Hugging Face Hub との連携**  
  データセット・モデルの公開・共有が容易。

詳細は公式READMEを参照：  
https://github.com/huggingface/lerobot

---

## 3. 対応ロボット：SO-ARM101（Supported Hardware）
SO-ARM101は、教育・研究用途向けの軽量6DoFロボットアームで、  
LeRobotの Robot API を通じて制御可能です。

### 公式仕様（URL引用）
https://wiki.seeedstudio.com/sensecraft_robotics_so_arm101/

### 本リポジトリで扱う内容
SO-ARM101 を対象とした、模倣学習のためのデータ収集・学習・推論を実行するためのPythonスクリプトを展開・整備する。

---

## 4. プロジェクト構成（Repository Structure）
リポジトリのディレクトリ構成は以下の通り。

~/my_repository/
    |-common_controllers/
        |-recode_controller/
        |-rollout_controller/
        |-teleope_controller/
        |-train_controller/

---

## 8. プロジェクト詳細（Project Details）

### common_controllers/recode_controller/
LeRobotDataset形式でデータを収集するためのスクリプト。
- パラメータをYAMLファイルで管理。

### common_controllers/rollout_controller/
学習済みモデルを SO-ARM101 に適用するためのスクリプト。
- パラメータをYAMLファイルで管理。

### common_controllers/teleope_controller/
SO-ARM101 を遠隔操作するためのスクリプト。 
- パラメータをYAMLファイルで管理。

### common_controllers/train_controller/
模倣学習・強化学習のためのCLIコマンドを実行するスクリプト。   
- パラメータをYAMLファイルで管理。
- 追学習、fine-tuning に対応。

---

## 9. トラブルシューティング（Troubleshooting）
整備中

---

## 10. 今後の展望（Future Work）
環境立ち上げ手順等の詳細を整理。

---

## 11. ライセンス（License）
本リポジトリは Apache 2.0 ライセンス（LeRobot準拠）を予定しています。
