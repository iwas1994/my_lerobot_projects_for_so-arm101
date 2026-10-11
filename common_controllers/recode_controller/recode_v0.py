import argparse
import yaml
from datetime import datetime

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.feature_utils import hw_to_dataset_features
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so_leader.config_so_leader import SO101LeaderConfig
from lerobot.teleoperators.so_leader.so_leader import SO101Leader
from lerobot.utils.keyboard_input import init_keyboard_listener
from lerobot.utils.utils import log_say
from lerobot.utils.visualization_utils import init_visualization
from lerobot.scripts.lerobot_record import record_loop
from lerobot.processor import make_default_processors


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to YAML config file"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cfg = load_config(args.config)

    # --- Robot Config ---
    robot_cameras = {
        name: OpenCVCameraConfig(
            index_or_path=cam["index_or_path"],
            width=cam["width"],
            height=cam["height"],
            fps=cam["fps"],
        )
        for name, cam in cfg["robot"]["cameras"].items()
    }

    robot_config = SO101FollowerConfig(
        port=cfg["robot"]["port"],
        id=cfg["robot"]["id"],
        cameras=robot_cameras,
    )

    # --- Teleop Config ---
    teleop_config = SO101LeaderConfig(
        port=cfg["teleop"]["port"],
        id=cfg["teleop"]["id"],
    )

    # --- Initialize Robot & Teleop ---
    robot = SO101Follower(robot_config)
    teleop = SO101Leader(teleop_config)

    # --- Dataset Features ---
    action_features = hw_to_dataset_features(robot.action_features, "action")
    obs_features = hw_to_dataset_features(robot.observation_features, "observation")
    dataset_features = {**action_features, **obs_features}

    # --- Dataset ---
    # ベース名（YAML）
    base_repo_id = cfg["dataset"]["repo_id"]

    # 日時を付ける
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    repo_id = f"{base_repo_id}_{timestamp}"

    dataset = LeRobotDataset.create(
        repo_id=repo_id,
        fps=cfg["dataset"]["fps"],
        features=dataset_features,
        robot_type=robot.name,
        use_videos=True,
        image_writer_threads=4,
    )

    # --- Keyboard Listener & Visualization ---
    _, events = init_keyboard_listener()
    init_visualization("rerun", session_name="recording")

    # --- Connect Robot & Teleop ---
    robot.connect()
    teleop.connect()

    # --- Processors ---
    teleop_action_processor, robot_action_processor, robot_observation_processor = make_default_processors()

    # --- Recording Loop ---
    num_episodes = cfg["record"]["num_episodes"]
    episode_time_s = cfg["record"]["episode_time_s"]
    reset_time_s = cfg["record"]["reset_time_s"]
    task_description = cfg["record"]["task_description"]

    episode_idx = 0
    while episode_idx < num_episodes and not events["stop_recording"]:
        log_say(f"Recording episode {episode_idx + 1} of {num_episodes}")

        record_loop(
            robot=robot,
            events=events,
            fps=cfg["dataset"]["fps"],
            teleop_action_processor=teleop_action_processor,
            robot_action_processor=robot_action_processor,
            robot_observation_processor=robot_observation_processor,
            teleop=teleop,
            dataset=dataset,
            control_time_s=episode_time_s,
            single_task=task_description,
            display_data=True,
        )

        # Reset
        if not events["stop_recording"] and (episode_idx < num_episodes - 1 or events["rerecord_episode"]):
            log_say("Reset the environment")
            record_loop(
                robot=robot,
                events=events,
                fps=cfg["dataset"]["fps"],
                teleop_action_processor=teleop_action_processor,
                robot_action_processor=robot_action_processor,
                robot_observation_processor=robot_observation_processor,
                teleop=teleop,
                control_time_s=reset_time_s,
                single_task=task_description,
                display_data=True,
            )

            if events["rerecord_episode"]:
                log_say("Re-recording episode")
                events["rerecord_episode"] = False
                events["exit_early"] = False
                dataset.clear_episode_buffer()
                continue

        dataset.save_episode()
        episode_idx += 1

    # --- Finalize ---
    log_say("Finalizing dataset...")
    dataset.finalize()

    robot.disconnect()
    teleop.disconnect()
    dataset.push_to_hub()


if __name__ == "__main__":
    main()
