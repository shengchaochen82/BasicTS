import os
from easydict import EasyDict
# architecture 
from basicts.archs.StemGNN_arch import StemGNN
# runner
from basicts.runners.StemGNN_runner import StemGNNRunner
from basicts.data.base_dataset import BaseDataset
from basicts.metrics.mae import masked_mae
from basicts.metrics.mape import masked_mape
from basicts.metrics.rmse import masked_rmse
from basicts.losses.losses import masked_l1_loss

"""Different from the official code, we use Adam as the optimizer and MAE as the loss function since they bring better performance."""

CFG = EasyDict()

# ================= general ================= #
CFG.DESCRIPTION = 'StemGNN model configuration'
CFG.RUNNER  = StemGNNRunner
CFG.DATASET_CLS   = BaseDataset
CFG.DATASET_NAME  = "PEMS03"
CFG.DATASET_TYPE  = 'Traffic flow'
CFG.GPU_NUM = 1
CFG.METRICS = {
    "MAE": masked_mae,
    "RMSE": masked_rmse,
    "MAPE": masked_mape
}

# ================= environment ================= #
CFG.ENV = EasyDict()
CFG.ENV.SEED    = 1
CFG.ENV.CUDNN = EasyDict()
CFG.ENV.CUDNN.ENABLED = True

# ================= model ================= #
CFG.MODEL = EasyDict()
CFG.MODEL.NAME  = 'StemGNN'
CFG.MODEL.ARCH  = StemGNN
CFG.MODEL.PARAM = {
    "units":    358,
    "stack_cnt": 2,
    "time_step": 12,
    "multi_layer": 5,
    "horizon": 12,
    "dropout_rate": 0.5,
    "leaky_rate": 0.2
}
CFG.MODEL.FROWARD_FEATURES = [0]            
CFG.MODEL.TARGET_FEATURES  = [0]                

# ================= optim ================= #
CFG.TRAIN = EasyDict()
CFG.TRAIN.LOSS = masked_l1_loss
CFG.TRAIN.OPTIM = EasyDict()
CFG.TRAIN.OPTIM.TYPE = "Adam"
CFG.TRAIN.OPTIM.PARAM= {
    "lr":0.002
}
CFG.TRAIN.LR_SCHEDULER = EasyDict()
CFG.TRAIN.LR_SCHEDULER.TYPE = "MultiStepLR"
CFG.TRAIN.LR_SCHEDULER.PARAM= {
    "milestones":[1, 50, 100],
    "gamma":0.5
}

# ================= train ================= #
# CFG.TRAIN.CLIP_GRAD_PARAM = {
#     'max_norm': 5.0
# }
CFG.TRAIN.NUM_EPOCHS = 200
CFG.TRAIN.CKPT_SAVE_DIR = os.path.join(
    'checkpoints',
    '_'.join([CFG.MODEL.NAME, str(CFG.TRAIN.NUM_EPOCHS)])
)
# train data
CFG.TRAIN.DATA          = EasyDict()
CFG.TRAIN.NULL_VAL      = 0.0
## read data
CFG.TRAIN.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TRAIN.DATA.BATCH_SIZE   = 64
CFG.TRAIN.DATA.PREFETCH     = False
CFG.TRAIN.DATA.SHUFFLE      = True
CFG.TRAIN.DATA.NUM_WORKERS  = 2
CFG.TRAIN.DATA.PIN_MEMORY   = False

# ================= validate ================= #
CFG.VAL = EasyDict()
CFG.VAL.INTERVAL = 1
# validating data
CFG.VAL.DATA = EasyDict()
## read data
CFG.VAL.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.VAL.DATA.BATCH_SIZE     = 64
CFG.VAL.DATA.PREFETCH       = False
CFG.VAL.DATA.SHUFFLE        = False
CFG.VAL.DATA.NUM_WORKERS    = 2
CFG.VAL.DATA.PIN_MEMORY     = False

# ================= test ================= #
CFG.TEST = EasyDict()
CFG.TEST.INTERVAL = 1
# validating data
CFG.TEST.DATA = EasyDict()
## read data
CFG.TEST.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TEST.DATA.BATCH_SIZE    = 64
CFG.TEST.DATA.PREFETCH      = False
CFG.TEST.DATA.SHUFFLE       = False
CFG.TEST.DATA.NUM_WORKERS   = 2
CFG.TEST.DATA.PIN_MEMORY    = False
