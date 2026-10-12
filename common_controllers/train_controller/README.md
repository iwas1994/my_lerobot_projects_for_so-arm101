# train_controller

このディレクトリは、LeRobot の学習処理を簡潔に実行するための
**「学習ラッパースクリプト（Training Wrapper）」** を提供します。

中心となるスクリプトは `train_v0.py` で、  
外部設定ファイル（YAML）を読み込み、
標準学習・再開学習（resume）・ファインチューニング（finetune）を統合的に扱い、
lerobot-train を直接呼び出す実行環境を構築します。

---

## 1. train_v0.py の概要

`train_v0.py` は、LeRobot の学習を簡単に実行するための「コマンド生成＋実行ラッパー」です。

- YAML 設定ファイルの読み込み  
- 標準学習 / 再開学習 / ファインチューニングの自動判定  
- LoRA ファインチューニング設定の自動挿入  
- Hugging Face Hub からモデルを snapshot_download  
- repo_id にタイムスタンプを付与して重複を防止  
- lerobot-train の sys.argv を書き換えて直接 main() を実行  

### 処理フロー（概要）
1. YAML 設定ファイルを読み込む  
2. model.base_repo_id にタイムスタンプを付与して新しい repo_id を生成  
3. resume / finetune / standard のどれで学習するか判定  
4. 必要に応じて Hub からモデルをダウンロード  
5. LoRA 設定があればコマンドに追加  
6. 学習ステップ・デバイス・WandB 設定などを追加  
7. sys.argv を書き換えて lerobot-train を実行  

---

## 2. configs/ 以下の YAML ファイルについて

`configs/` ディレクトリには、`train_v0.py` が読み込む **制御設定ファイル（YAML）** が配置されています。  
以下は、YAML の内容とその説明です。

---

## 3. YAML の内容と役割

### train セクション

```yaml
train:
  policy_type: <Specifies the policy to use (e.g., act, diffusion)>
  device: <The training device (cuda or cpu)>
  steps: <Number of training steps>
  save_freq: <Frequency at which the model is saved>
```

### dataset セクション

```yaml
dataset:
  repo_id: <The dataset to be used for training (stored on Hugging Face Hub).>
```

### model セクション

```yaml
model:
  base_repo_id: <The base name of the model repository where training outputs will be saved>
```

実行時にタイムスタンプが付与され、
例：Iwas-6127/act-model-script-test-20261012_202000
のような repo_id が自動生成される

### resume セクション

```yaml
resume:
  enable: <true or false (If true, training will resume from a previous checkpoint)>
  config_path: <Path to the config.yaml used in the previous training run>
```

### finetune セクション

```yaml
finetune:
  enable: <true or false (If true, fine-tuning will be performed using an existing pretrained model)>
  repo_type: <hub or local (If "hub", the pretrained model is downloaded from Hugging Face Hub using snapshot_download)>
  pretrained_model_path: <Path to the pretrained model, or a Hugging Face repo_id>
  local_download_dir: <Local directory where the model will be downloaded when using Hub>

  # ------------------------------------------------------------
  # LoRA を使って軽量ファインチューニングする場合は、
  # 以下の設定をコメントインしてください。
  #
  # If you want to perform lightweight fine-tuning using LoRA,
  # uncomment the following settings.
  # 
  # ※ ACTPolicy は自動で LoRA を挿入できないため、
  #    peft_target_modules の指定が必須です。
  #
  # ACTPolicy does NOT support automatic LoRA module detection,
  # so specifying peft_target_modules is required.
  # ------------------------------------------------------------

  # peft_method_type: <LoRA method type (e.g., "lora")>
  # peft_r: <Rank value for LoRA>

  # peft_target_modules:
  #   # Vision backbone（ResNet）
  #   - "model.backbone.layer3.0.conv1"
  #   - "model.backbone.layer3.0.conv2"
  #   - "model.backbone.layer4.0.conv1"
  #   - "model.backbone.layer4.0.conv2"

  #   # Transformer encoder（LoRA が挿入可能なのは out_proj のみ）
  #   - "model.encoder.layers.0.self_attn.out_proj"
  #   - "model.encoder.layers.1.self_attn.out_proj"
  #   - "model.encoder.layers.2.self_attn.out_proj"
  #   - "model.encoder.layers.3.self_attn.out_proj"
```

### wandb セクション

```yaml
wandb:
  enable: <true or false (Whether to enable logging with Weights & Biases)>
  mode: <online or offline>
```

---

## 4. train_v0.py の実行方法（YAML を引数で指定）

`train_v0.py` を実行する際は、  
**必ず `--config` 引数で `configs/` 以下の YAML ファイルを指定します。**

実行例
```bash
python train_v0.py --config configs/train_default.yaml
```
