"""Verify the FR-1 installation by resetting and stepping a small simulation."""

import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", choices=("none", "rgb_array", "human"), default="none")
    args = parser.parse_args()
    if args.render != "human":
        os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    import numpy as np
    import pygame
    from pyquaticus.envs.pyquaticus import PyQuaticusEnv

    env = PyQuaticusEnv(
        team_size=1,
        config_dict={"gps_env": False, "max_time": 2.0},
        render_mode=None if args.render == "none" else args.render,
    )
    try:
        observations, _ = env.reset(seed=7)
        if len(observations) != 2:
            raise RuntimeError(f"Expected two agents, received {list(observations)}")
        for index, agent in enumerate(observations):
            env.action_space(agent).seed(7 + index)

        # Bound the check independently of the simulator's episode limit.
        for step in range(1, 101):
            actions = {agent: env.action_space(agent).sample() for agent in observations}
            observations, _, terminated, truncated, _ = env.step(actions)
            if not all(np.isfinite(obs).all() for obs in observations.values()):
                raise RuntimeError("Non-finite observation encountered")
            if all(terminated[agent] or truncated[agent] for agent in observations):
                break
        else:
            raise RuntimeError("The two-second episode did not finish within 100 steps")

        if args.render == "rgb_array":
            env.render()
            # This upstream revision draws to a surface and returns None.
            frame = pygame.surfarray.array3d(env.screen).transpose(1, 0, 2)
            output = Path("runs/fr1/frame.png")
            output.parent.mkdir(parents=True, exist_ok=True)
            pygame.image.save(env.screen, output)
            print(f"Frame: {output.resolve()} ({frame.shape})")

        print(f"PASS: import, 1v1 reset, {step} steps, episode completion; render={args.render}")
    finally:
        env.close()


if __name__ == "__main__":
    main()
