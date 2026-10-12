# recode_controller

このディレクトリは、SO-ARM101 を含むロボット制御において
**「学習済みポリシーをロボットへ実行（Rollout）させるコントローラ」**です。

中心となるスクリプトは `rollout.py` で、
外部設定ファイル（YAML）を読み込み、ロボット・カメラ・ポリシー（学習済みモデル）を統合した
推論ベースの制御ループを構築します。

---

## 1. recode_v0.py の概要

`rollout.py` は、以下の機能を提供する汎用ロボット推論スクリプトです。

- YAML 設定ファイルの読み込み  
- follower_arm（ロボット）の初期化  
- カメラ設定の読み込み  
- 学習済みポリシーの読み込み  
- 推論ループの実行（観測 → 推論 → アクション送信）  
- ログ出力・デバッグ情報の記録  

### 処理フロー（概要）
1. YAML 設定ファイルを読み込む  
2. follower_arm を初期化  
3. カメラを初期化  
4. 学習済みポリシーを読み込む  
5. rollout（推論）ループを開始  
6. 指定時間経過または中断で終了  
7. 必要に応じてロボットを初期位置へ戻す  

---

## 2. configs/ 以下の YAML ファイルについて

`configs/` ディレクトリには、`rollout.py` が読み込む「推論設定ファイル（YAML）」が配置されています。  
以下は、YAML の内容とその説明です。

---

## 3. YAML の内容と役割

### strategy セクション

```yaml
strategy:
  type: <strategy type>
```

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

### policy セクション

```yaml
policy:
  pretrained_path: <model path from Hugging Face Hub>
```

### rollout セクション

```yaml
rollout:
  duration: <rollout duration>
  task: "<task name>"
  display_data: <Display inference data and images (True or False)>
```

---

## 4. rollout_v0.py の実行方法（YAML を引数で指定）

`rollout_v0.py` を実行する際は、  
**必ず `--config` 引数で `configs/` 以下の YAML ファイルを指定します。**

実行例
```bash
python rollout_v0.py --config configs/rollout_default.yaml
```
