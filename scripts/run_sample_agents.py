"""Run short FR-2 demonstrations with PyQuaticus's existing sample policies."""

import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example", choices=("random", "attack-defend", "combined"), default="attack-defend")
    parser.add_argument("--render", choices=("none", "rgb_array", "human"), default="none")
    parser.add_argument("--seconds", type=float, default=120.0)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--config", type=Path, help="JSON defaults; command-line arguments override them")
    parser.add_argument("--output", type=Path, help="Directory for this run's artifacts")
    parser.add_argument("--record", action="store_true", help="Save a video at 10 frames per second")
    preliminary, _ = parser.parse_known_args()
    if preliminary.config:
        settings = json.loads(preliminary.config.read_text())
        allowed = {"example", "render", "seconds", "seed", "record"}
        if not isinstance(settings, dict) or settings.keys() - allowed:
            parser.error(f"Config must be an object using only: {sorted(allowed)}")
        if settings.get("example", "attack-defend") not in ("random", "attack-defend", "combined"):
            parser.error("Invalid example in config")
        if settings.get("render", "none") not in ("none", "rgb_array", "human"):
            parser.error("Invalid render mode in config")
        if type(settings.get("seed", 7)) is not int or type(settings.get("record", False)) is not bool:
            parser.error("Config seed must be an integer and record must be a boolean")
        if type(settings.get("seconds", 120.0)) not in (int, float):
            parser.error("Config seconds must be a number")
        parser.set_defaults(**settings)
    args = parser.parse_args()
    if not 0 < args.seconds <= 600:
        parser.error("--seconds must be between 0 and 600 (exclusive of zero)")
    if args.record and args.render == "none":
        parser.error("Recording requires --render rgb_array or human")
    if args.render != "human":
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    import numpy as np
    import pygame
    from pyquaticus.base_policies.base_attack import BaseAttacker
    from pyquaticus.base_policies.base_combined import Heuristic_CTF_Agent
    from pyquaticus.base_policies.base_defend import BaseDefender
    from pyquaticus.config import config_dict_std
    from pyquaticus.envs.pyquaticus import PyQuaticusEnv

    team_size = 2 if args.example == "combined" else 1
    config = copy.deepcopy(config_dict_std)
    config.update(gps_env=False, max_time=args.seconds, sim_speedup_factor=10, render_agent_ids=True)
    if args.example == "combined":
        config["dynamics"] = "si"
    env = PyQuaticusEnv(
        team_size=team_size,
        action_space="discrete",
        config_dict=config,
        render_mode=None if args.render == "none" else args.render,
    )
    output = args.output or Path("runs/fr2") / args.example / f"{args.render}-seed{args.seed}-{args.seconds:g}s"
    output.mkdir(parents=True, exist_ok=True)
    writer = None
    trajectory = []
    try:
        observations, info = env.reset(seed=args.seed)
        if args.record:
            import cv2

            writer = cv2.VideoWriter(
                str(output / "demo.mp4"), cv2.VideoWriter_fourcc(*"mp4v"),
                10, (env.screen_width + env.screen_width % 2, env.screen_height + env.screen_height % 2),
            )
            if not writer.isOpened():
                raise RuntimeError("MP4 writer could not be opened")
        if args.example == "attack-defend":
            policies = {
                "agent_0": BaseAttacker("agent_0", env, mode="medium"),
                "agent_1": BaseDefender("agent_1", env, mode="medium"),
            }
        elif args.example == "combined":
            policies = {
                agent: Heuristic_CTF_Agent(agent, env, mode="hard")
                for agent in observations
            }
        else:
            policies = {}

        for index, agent in enumerate(observations):
            env.action_space(agent).seed(args.seed + index)
        assignments = {
            agent: type(policies[agent]).__name__ if agent in policies else "random"
            for agent in observations
        }
        print(f"Running {args.example}: {assignments}", flush=True)

        for step in range(1, env.max_cycles + 2):
            actions = {
                agent: policies[agent].compute_action(observations, info)
                if agent in policies else env.action_space(agent).sample()
                for agent in observations
            }
            for agent, action in actions.items():
                if not env.action_space(agent).contains(action):
                    raise RuntimeError(f"Invalid action for {agent}: {action}")
            observations, _, terminated, truncated, info = env.step(actions)
            if not all(np.isfinite(obs).all() for obs in observations.values()):
                raise RuntimeError("Non-finite observation encountered")
            trajectory.append({
                "step": step,
                "actions": {agent: int(action) for agent, action in actions.items()},
                "positions": {agent: env.players[agent].pos.tolist() for agent in observations},
                "captures": [int(value) for value in env.state["captures"]],
                "tags": [int(value) for value in env.state["tags"]],
            })
            if writer is not None:
                frame = pygame.surfarray.array3d(env.screen).transpose(1, 0, 2)
                # MPEG needs even dimensions; preserve the full field with padding.
                frame = cv2.copyMakeBorder(frame, 0, frame.shape[0] % 2, 0, frame.shape[1] % 2, cv2.BORDER_CONSTANT)
                writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            if all(terminated[agent] or truncated[agent] for agent in observations):
                break
        else:
            raise RuntimeError("Episode exceeded its configured step limit")

        if args.render != "none":
            pygame.image.save(env.screen, output / "frame.png")
        summary = {
            "example": args.example,
            "seed": args.seed,
            "team_size": team_size,
            "config": config,
            "policies": assignments,
            "mode": "hard" if args.example == "combined" else "medium" if policies else None,
            "render": args.render,
            "steps": step,
            "simulated_seconds": env.current_time,
            "end_reason": "terminated" if all(terminated[a] for a in observations) else "truncated",
            "team_order": ["blue", "red"],
            "captures": [int(value) for value in env.state["captures"]],
            "grabs": [int(value) for value in env.state["grabs"]],
            "tags": [int(value) for value in env.state["tags"]],
        }
        root = Path(__file__).resolve().parents[1]
        upstream = root / ".local/pyquaticus"
        metadata = {
            "upstream_commit": subprocess.check_output(
                ["git", "-C", str(upstream), "rev-parse", "HEAD"], text=True,
            ).strip(),
            "python": sys.version,
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "upstream_diff_sha256": hashlib.sha256(subprocess.check_output(
                ["git", "-C", str(upstream), "diff", "--binary"],
            )).hexdigest(),
            "packages": dict(sorted(
                (dist.metadata["Name"], dist.version) for dist in importlib.metadata.distributions()
            )),
            "patch_sha256": {
                patch.name: hashlib.sha256(patch.read_bytes()).hexdigest()
                for patch in sorted((root / "patches").glob("*.patch"))
            },
            "recording_fps": 10 if args.record else None,
        }
        (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
        (output / "trajectory.json").write_text(json.dumps(trajectory, indent=2) + "\n")
        (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary, indent=2))
        print(f"PASS: {args.example}; results in {output.resolve()}")
    finally:
        if writer is not None:
            writer.release()
        env.close()


if __name__ == "__main__":
    main()
