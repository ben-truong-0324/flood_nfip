import socket

# Determine the hostname
hostname = socket.gethostname()
if hostname == "Khais-MacBook-Pro.local" or hostname == "Khais-MBP.attlocal.net":  # Replace with macbook hostname
    from src.config_mac import *  # Import everything from config_dev, small monte carlo count, smalle
else:
    from src.config_cuda import * #BIG SIMU

import os

EVAL_REG_MODELS = [
    # 'MPLRelu', 'MPLReluTanh',
    'MPLTanhReluTanh', 'MPLTanhReluTanhRelu',
    # 'LSTM', 
    # 'CNN',
    # 'SalienceNN',
]


K_FOLD_CV = 5  # Number of CV folds
DREDUCE_NUM = 3
BIG_PICKLE_CHUNK_NUM = 5
NUM_STATISTICAL_ITER = 5


roc_period = 10
window_size = 20
std_dev = 2
short_window = 12
long_window = 26
signal_window = 9
rsi_period = 14
pred_for_5d_delta = 1