import argparse
import yaml
import tkinter as tk

from lerobot.cameras.opencv import OpenCVCameraConfig
from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
from lerobot.teleoperators.so_leader.config_so_leader import SO101LeaderConfig
from lerobot.teleoperators.so_leader.so_leader import SO101Leader

from lerobot.utils.keyboard_input import init_keyboard_listener
from lerobot.utils.utils import log_say
from lerobot.utils.visualization_utils import init_visualization


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    return parser.parse_args()

stop_flag = False

def stop():
    global stop_flag
    stop_flag = True

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

    # --- Initialize ---
    follower = SO101Follower(robot_config)
    leader = SO101Leader(teleop_config)

    # --- Keyboard Listener & Visualization ---
    _, events = init_keyboard_listener()

    if cfg.get("visualization", {}).get("enable", True):
        init_visualization("rerun", session_name="teleop_follow")

    # --- Connect ---
    log_say("Connecting follower...")
    follower.connect()

    log_say("Connecting leader...")
    leader.connect()

    log_say("Leader-Follower teleoperation started.")
    log_say("Press ESC to exit.")

    root = tk.Tk()
    tk.Button(root, text="STOP", command=stop).pack()

    # --- Teleoperation Loop ---
    while not stop_flag:
        action = leader.get_action()      # leader の操作を取得
        follower.send_action(action)      # follower に送信
        root.update()

    # --- Disconnect ---
    log_say("Stopping teleoperation...")
    leader.disconnect()
    follower.disconnect()
    log_say("Teleoperation stopped.")


if __name__ == "__main__":
    main()
