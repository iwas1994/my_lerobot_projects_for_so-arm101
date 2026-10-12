# teleope_controller

このディレクトリは、SO-ARM101 を含むロボット制御において
**「Leader–Follower（テレオペ）方式のコントローラ」** を提供します。

中心となるスクリプトは `teleope_v0.py` で、
外部設定ファイル（YAML）を読み込み、ロボット（Follower）・テレオペ側（Leader）・カメラ・可視化・操作ループを統合した
リアルタイム・テレオペレーション制御ループを構築します。

---

## 1. teleope_v0.py の概要

`teleope_v0.py` は、Leader（操作者）から取得した操作入力を
Follower（ロボット）へリアルタイムに送信するシンプルなテレオペ制御スクリプトです。

- YAML 設定ファイルの読み込み  
- follower_arm（ロボット）の初期化  
- leader_arm（テレオペ側）の初期化  
- カメラ設定の読み込み  
- キーボード入力の初期化 
- Rerun による可視化（任意）  
- Leader → Follower の操作伝達ループ  
- STOP ボタンによる安全停止  
- ログ出力  

### 処理フロー（概要）
1. YAML 設定ファイルを読み込む  
2. follower_arm を初期化  
3. leader_arm を初期化  
4. カメラ設定を構築  
5. キーボードリスナー・可視化を初期化  
6. follower / leader を接続  
7. Leader の操作を Follower にリアルタイム送信するループを開始  
8. STOP ボタンまたは ESC キーで停止  
9. 切断処理を実行

---

## 2. configs/ 以下の YAML ファイルについて

`configs/` ディレクトリには、`teleope_v0.py` が読み込む **制御設定ファイル（YAML）** が配置されています。  
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

### visualization セクション

```yaml
visualization:
  enable: <Display inference data and images (True or False)>
```

---

## 4. teleope_v0.py の実行方法（YAML を引数で指定）

`teleope_v0.py` を実行する際は、  
**必ず `--config` 引数で `configs/` 以下の YAML ファイルを指定します。**

実行例
```bash
python teleope_v0.py --config configs/teleop_default.yaml
```
