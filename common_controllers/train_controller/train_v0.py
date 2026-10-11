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

    # Add a timestamp to the repo_id
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_repo_id = f"{cfg['model']['base_repo_id']}-{timestamp}"

    # --- Determine whether it is standard training, resumed training, or fine-tuning ---
    argv = ["lerobot-train"]

    # Resume training
    if cfg["resume"]["enable"]:
        argv += [
            "--resume=true",
            f"--config_path={cfg['resume']['config_path']}",
        ]
    # Fine-tuning
    elif cfg["finetune"]["enable"]:
        if cfg["finetune"]["repo_type"] == "hub":
            local_dir = snapshot_download(
                repo_id=cfg["finetune"]["pretrained_model_path"],
                local_dir=cfg["finetune"]["local_download_dir"],
                local_dir_use_symlinks=False
            )
        else:
            local_dir = cfg["finetune"]["pretrained_model_path"]

        argv += [
            f"--policy.path={local_dir}",
        ]

        # Add LoRA settings only if they exist in the YAML config
        if "peft_method_type" in cfg["finetune"]:
            argv += [
                f"--peft.method_type={cfg['finetune']['peft_method_type']}",
                f"--peft.r={cfg['finetune']['peft_r']}",
            ]
            # Add target modules only if they exist
            if "peft_target_modules" in cfg["finetune"]:
                target_modules = cfg["finetune"]["peft_target_modules"]
                argv += [f"--peft.target_modules={','.join(target_modules)}"]
    # Standard training
    else:
        argv += [
            f"--policy.type={cfg['train']['policy_type']}",
        ]

    # Basic settings
    argv += [
        f"--policy.repo_id={model_repo_id}",
        f"--policy.device={cfg['train']['device']}",
        f"--steps={cfg['train']['steps']}",
        f"--save_freq={cfg['train']['save_freq']}",
        f"--dataset.repo_id={cfg['dataset']['repo_id']}",
        f"--wandb.enable={str(cfg['wandb']['enable']).lower()}",
        f"--wandb.mode={cfg['wandb']['mode']}",
    ]

    # Rewrite sys.argv and call main()
    sys.argv = argv

    print("=== Running lerobot-train ===")
    print(" ".join(argv))

    main()  # Run directly without subprocess


if __name__ == "__main__":
    main_wrapper()