# recode_controller

このディレクトリは、SO-ARM101 を含むロボット制御において  
**「Recode（再符号化）ベースのコントローラ」** です。

中心となるスクリプトは `recode_v0.py` で、  
外部設定ファイル（YAML）を読み込み、ロボット・テレオペ・カメラ・データ収集・記録処理を統合した制御ループを構築します。

---

## 1. recode_v0.py の概要

`recode_v0.py` は、以下の機能を提供する汎用ロボット制御スクリプトです。

- YAML 設定ファイルの読み込み  
- follower_arm（ロボット）の初期化  
- leader_arm（テレオペ側）の初期化  
- カメラ設定の読み込み  
- データセット保存設定の適用  
- エピソード記録（回数・時間・リセット時間）  
- ログ出力・デバッグ情報の記録  

### 処理フロー（概要）
1. YAML 設定ファイルを読み込む  
2. follower_arm を初期化  
3. leader_arm を初期化  
4. カメラを設定し同期開始  
5. データセット保存設定を適用  
6. エピソード記録ループを開始  
7. 必要に応じてリセット処理を実行  

---

## 2. configs/ 以下の YAML ファイルについて

`configs/` ディレクトリには、`recode_v0.py` が読み込む **制御設定ファイル（YAML）** が配置されています。  
以下は、YAML の内容とその説明です。

---

## 3. YAML の内容と役割

### robot セクション

```yaml
robot:
  port: <COM port>
  id: <follower arm ID>
  cameras:
    <camera name 1>:
      index_or_path: <path ID>
      width: <pix>
      height: <pix>
      fps: <fps>
    <camera name 2>:
      index_or_path: <path ID>
      width: <pix>
      height: <pix>
      fps: <fps>
```

### teleop セクション

```yaml
teleop:
  port: <COM port>
  id: <follower arm ID>
```

### dataset セクション

```yaml
dataset:
  repo_id: <Dataset repository ID on Hugging Face Hub>
  fps: <fps>
```

### record セクション

```yaml
record:
  num_episodes: <Number of episodes to record>
  episode_time_s: <Duration of each episode in seconds>
  reset_time_s: <Reset time between episodes>
  task_description: "<Description of the task (stored in the dataset)>"
```

---

## 4. recode_v0.py の実行方法（YAML を引数で指定）

`recode_v0.py` を実行する際は、  
**必ず `--config` 引数で `configs/` 以下の YAML ファイルを指定します。**

実行例
```bash
python recode_v0.py --config configs/recode_default.yaml
```
