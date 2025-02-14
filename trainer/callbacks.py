from pytorch_lightning import Trainer
from pytorch_lightning.callbacks import *
from dataModule.random_dataset import RandomDataModule
from model.simple_model import SimpleModel

CALLBACK_DT = {
    'ModelCheckpoint': ModelCheckpoint,
    'EarlyStopping': EarlyStopping,
    'TQDMProgressBar': TQDMProgressBar,
}

__all__ = ['get_callbacks']


def get_callbacks(callback_cfg: dict, extra_callbacks: list = None):
    """
    transform callback config to callback instance, config are expected from yaml files.

    :param extra_callbacks: list of extra callback instance.
    :param callback_cfg: dict of callback config, key must be in CALLBACK_DT.keys()
    :return: list of callback instance
    """
    assert set(callback_cfg.keys()).issubset(set(CALLBACK_DT.keys())), \
        f"callback config key must be in {CALLBACK_DT.keys()}"
    callback_lt = []
    for key in callback_cfg.keys():
        callback = CALLBACK_DT[key](**callback_cfg[key])
        callback_lt.append(callback)

    if extra_callbacks is None:
        return callback_lt
    else:
        return callback_lt + extra_callbacks


if __name__ == "__main__":
    # 初始化数据模块和模型
    data_module = RandomDataModule(batch_size=32)
    model = SimpleModel()

    # 配置 ModelCheckpoint 回调
    callback_dt = {
        'ModelCheckpoint': dict(filename='model_{epoch:02d}_{val_loss:.2f}', monitor='val_loss',
                                save_top_k=3, mode='min', save_last=True),
        'EarlyStopping': dict(monitor='val_loss', patience=5, mode='min'),
        'TQDMProgressBar': dict(refresh_rate=1),
    }
    callbacks = get_callbacks(callback_dt)

    # 初始化 trainer
    trainer = Trainer(
        max_epochs=100,
        callbacks=callbacks,
        accelerator="auto",
        enable_progress_bar=True
    )

    # 训练模型
    trainer.fit(model, datamodule=data_module)
