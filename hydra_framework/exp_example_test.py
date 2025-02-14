import hydra
import os
import sys
import logging
from datetime import datetime
from hydra.core.hydra_config import HydraConfig
from omegaconf import DictConfig, OmegaConf
from pytorch_lightning.loggers import TensorBoardLogger

# 获取 logger
logger = logging.getLogger(__name__)


def _log_initial_info(cfg: DictConfig):
    """
    记录脚本的初始信息
    """
    script = os.path.basename(sys.argv[0])
    script_name = os.path.splitext(script)[0]
    args = sys.argv[1:]
    conda_env = os.getenv('CONDA_DEFAULT_ENV', 'N/A')
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    logger.info(f"Script Name: {script_name}")
    logger.info(f"Arguments: {args}")
    logger.info(f"Conda Environment: {conda_env}")
    logger.info(f"Start Time: {start_time}")
    logger.info("\n" + OmegaConf.to_yaml(cfg))


@hydra.main(
    version_base="1.2",
    config_path=os.getenv('CONFIGS_LOCATION', './config'),
    config_name="exp_example",
)
def main(cfg: DictConfig):
    if HydraConfig.get().mode == hydra.types.RunMode.RUN:
        work_dir = HydraConfig.get().run.dir
    else:
        work_dir = os.path.join(HydraConfig.get().sweep.dir,
                                HydraConfig.get().sweep.subdir)
    cfg = OmegaConf.to_container(cfg, resolve=True)
    tb_logger = TensorBoardLogger(save_dir=work_dir)
    _log_initial_info(cfg)  # 打印当前内容

    return 42


if __name__ == "__main__":
    main()
