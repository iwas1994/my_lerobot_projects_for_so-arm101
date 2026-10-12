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


## 4. 本開発における開発環境
ロボット実機を動かす環境と計算環境（デスクトップ）が離れているため、データ収集・推論は別計算環境（ノートPC）で実行する。  
最終的に使用可能なモデルはノートPCのスペックに依存していることをここで明記しておく。  

### ロボットとセンサ
- leader arm : so-arm101 (leader)
- follower arm : so-arm101 (follower)
- camera1 : ELECOM WEBCAM-101BK (環境俯瞰)
- camera2 :[ InnoMaker 720P USB2.0 UVCカメラ 120° DFOV対応](https://www.amazon.co.jp/dp/B0CLRJZG8D?ref=ppx_yo2ov_dt_b_fed_asin_title)(ハンドカメラ) 

### 収集・推論・実行環境（ノートPC）
- CPU : 13th Gen Intel(R) Core(TM) i5 - 1335U (1.3GHz, 10コア)
- メモリ：16GB LPDDR5
- GPU : Intel(R) Iris(R) Xe Graphics (7.8GB)

### 学習環境（デスクトップPC）
- CPU : Intel(R) Core(TM) i7 - 14700F (2.1GHz, 20コア)
- メモリ：32GB DDR5
- GPU : NVIDIA GeForce RTX 4060 Ti (16GB)

---

## 5. プロジェクト構成（Repository Structure）
リポジトリのディレクトリ構成は以下の通り。

~/my_repository/
    |-common_controllers/
        |-recode_controller/
        |-rollout_controller/
        |-teleope_controller/
        |-train_controller/

---

## 6. プロジェクト詳細（Project Details）

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

## 7. トラブルシューティング（Troubleshooting）
整備中

---

## 8. 今後の展望（Future Work）
- 環境立ち上げ手順等の詳細を整理。
  なお、以下issueに開発状況を記録記録しており、適宜更新している。  
    https://github.com/iwas1994/my_lerobot_projects_for_so-arm101/issues  
- データ収集・推論環境（ノートPC）のアップデート。

---

## 9. ライセンス（License）
本リポジトリは Apache 2.0 ライセンス（LeRobot準拠）を予定しています。
