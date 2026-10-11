import argparse
import yaml
import threading

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.utils.keyboard_input import init_keyboard_listener
from lerobot.utils.utils import log_say
from lerobot.utils.visualization_utils import init_visualization
from lerobot.processor import make_default_processors
from lerobot.configs import PreTrainedConfig

from lerobot.rollout import RolloutConfig, build_rollout_context, LinkedEvent
from lerobot.rollout.inference import SyncInferenceConfig
from lerobot.rollout.configs import (
    BaseStrategyConfig, 
    SentryStrategyConfig, 
    HighlightStrategyConfig, 
    EpisodicStrategyConfig, 
    DAggerStrategyConfig,
)
from lerobot.rollout.strategies import (
    BaseStrategy,
    SentryStrategy,
    HighlightStrategy,
    EpisodicStrategy,
    DAggerStrategy,
)


STRATEGY_CONFIG_MAP = {
    "base": BaseStrategyConfig,
    "sentry": SentryStrategyConfig,
    "highlight": HighlightStrategyConfig,
    "episodic": EpisodicStrategyConfig,
    "dagger": DAggerStrategyConfig,
}

STRATEGY_CLASS_MAP = {
    "base": BaseStrategy,
    "sentry": SentryStrategy,
    "highlight": HighlightStrategy,
    "episodic": EpisodicStrategy,
    "dagger": DAggerStrategy,
}


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)

    # --- Robot Cameras ---
    robot_cameras = {
        name: OpenCVCameraConfig(
            index_or_path=cam["index_or_path"],
            width=cam["width"],
            height=cam["height"],
            fps=cam["fps"],
        )
        for name, cam in cfg["robot"]["cameras"].items()
    }

    # --- Robot Config ---
    robot_config = SO101FollowerConfig(
        port=cfg["robot"]["port"],
        id=cfg["robot"]["id"],
        cameras=robot_cameras,
    )
    robot = SO101Follower(robot_config)

    # --- Processors ---
    teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

    # --- Policy Config ---
    policy_cfg = PreTrainedConfig.from_pretrained(cfg["policy"]["pretrained_path"])
    policy_cfg.pretrained_path = cfg["policy"]["pretrained_path"]

    # --- Strategy Config---
    strategy_type = cfg["strategy"]["type"]
    StrategyConfigCls = STRATEGY_CONFIG_MAP[strategy_type]
    strategy_cfg = StrategyConfigCls()

    # --- Rollout Config
    rollout_cfg = RolloutConfig(
        robot=robot_config,
        policy=policy_cfg,
        strategy=strategy_cfg,
        inference=SyncInferenceConfig(),  # 参考コードに合わせるなら追加
        duration=cfg["rollout"]["duration"],
        task=cfg["rollout"]["task"],
        display_data=cfg["rollout"]["display_data"],
    )

    # --- Shutdown event ---
    shutdown_event = threading.Event()
    linked_shutdown = LinkedEvent(shutdown_event)

    # --- Build context ---
    log_say("Building rollout context.")
    ctx = build_rollout_context(rollout_cfg, linked_shutdown)

    # --- Run rollout ---
    try:
        StrategyCls = STRATEGY_CLASS_MAP[strategy_type]
        strategy = StrategyCls(rollout_cfg.strategy)

        log_say("Starting rollout...")
        strategy.setup(ctx)
        strategy.run(ctx)
    except Exception as e:
        print("Error:", e)

    # --- Finally
    finally:
        # robot.disconnect() は ctx.hardware.robot_wrapper が持っている
        try:
            ctx.hardware.robot_wrapper.disconnect()
        except Exception:
            pass

        try:
            strategy.teardown(ctx)
        except Exception:
            pass

        log_say("Rollout finished.")

if __name__ == "__main__":
    main()
