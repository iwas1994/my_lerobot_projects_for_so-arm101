import sys
from datetime import datetime
from huggingface_hub import snapshot_download
from lerobot.scripts.lerobot_train import main
import yaml
import argparse


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    return parser.parse_args()


def main_wrapper():
    args = parse_args()
    cfg = load_config(args.config)

    # repo_id に日時を付ける
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_repo_id = f"{cfg['model']['base_repo_id']}-{timestamp}"

    # --- 通常学習 / 追学習 / ファインチューニングを判定 ---
    argv = ["lerobot-train"]

    # 追学習（resume）
    if cfg["resume"]["enable"]:
        argv += [
            "--resume=true",
            f"--config_path={cfg['resume']['config_path']}",
        ]
    # ファインチューニング
    elif cfg["finetune"]["enable"]:
        if cfg["finetune"]["repo_type"] == "hub":
            local_dir = snapshot_download(
                repo_id=cfg["finetune"]["pretrained_model_path"],
                local_dir=cfg["finetune"]["local_download_dir"],
                local_dir_use_symlinks=False
            )
        else:
            local_dir = cfg['finetune']['pretrained_model_path']

        argv += [
            f"--policy.path={local_dir}",
        ]

        # LoRA を使う設定が YAML に存在する場合だけ追加する
        if "peft_method_type" in cfg["finetune"]:
            argv += [
                f"--peft.method_type={cfg['finetune']['peft_method_type']}",
                f"--peft.r={cfg['finetune']['peft_r']}",
            ]
            # target_modules がある場合だけ追加
            if "peft_target_modules" in cfg["finetune"]:
                target_modules = cfg["finetune"]["peft_target_modules"]
                argv += [f"--peft.target_modules={','.join(target_modules)}"]
    # 通常学習
    else:
        argv += [
            f"--policy.type={cfg['train']['policy_type']}",
        ]

    # 基本設定
    argv += [
        f"--policy.repo_id={model_repo_id}",
        f"--policy.device={cfg['train']['device']}",
        f"--steps={cfg['train']['steps']}",
        f"--save_freq={cfg['train']['save_freq']}",
        f"--dataset.repo_id={cfg['dataset']['repo_id']}",
        f"--wandb.enable={str(cfg['wandb']['enable']).lower()}",
        f"--wandb.mode={cfg['wandb']['mode']}",
    ]

    # sys.argv を書き換えて main() を呼ぶ
    sys.argv = argv

    print("=== Running lerobot-train ===")
    print(" ".join(argv))

    main()  # ← subprocess なしで実行


if __name__ == "__main__":
    main_wrapper()
