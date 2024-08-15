import argparse

import torch
from data_loader import get_loader
from data_preprocessing import preprocess_data
from solver import Solver
from torch.backends import cudnn
from util.config import Config
from util.logging import Logger


def main(config: Config, args: argparse.Namespace):
    # For fast training.
    cudnn.benchmark = True
    torch.multiprocessing.set_sharing_strategy("file_system")
    torch.multiprocessing.set_start_method("spawn")
    preprocess_data(config)
    data_loader = get_loader(config)
    solver = Solver(data_loader, args, config)
    solver.train()


if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--config_name", type=str, default="spsp2-large")
    # fmt: on
    args = parser.parse_args()

    logger = Logger()
    config = Config(f"configs/{args.config_name}.toml")

    if args.trace or config.options.trace:
        hr = __import__("heartrate")
        hr.trace(files=hr.files.all)

    main(config, args)
