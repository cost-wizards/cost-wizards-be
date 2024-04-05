import loguru
from cost_wiz.config.settings import EnvSettings


if __name__ == "__main__":
    logger = loguru.logger
    env: EnvSettings = EnvSettings()

