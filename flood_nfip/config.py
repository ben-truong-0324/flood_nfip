import socket

# Determine the hostname
hostname = socket.gethostname()
if hostname == "Khais-MacBook-Pro.local" or hostname == "Khais-MBP.attlocal.net":  
    from flood_nfip.config_mac import *  
else:
    from flood_nfip.config_cuda import * 

import os


ORIGINAL_PATH = os.path.join(os.getcwd(), 'data', 'FimaNfipClaims.csv')
TRAIN_PATH = os.path.join(os.getcwd(), 'data', 'train.csv')
TEST_PATH = os.path.join(os.getcwd(), 'data', 'test.csv')

ETL_VERSION = 'v1'

# Define paths for processed datasets based on ETL_version
PROCESSED_TRAIN_PATH = os.path.join(os.getcwd(), 'data', f'train_processed_{ETL_VERSION}.csv')
PROCESSED_TEST_PATH = os.path.join(os.getcwd(), 'data', f'test_processed_{ETL_VERSION}.csv')



DATASET_SELECTION = "kaggle_flood_nfip" #kaggle_housing #kaggle_housing_test

EVAL_FUNC_METRIC = 'rmlse' #'mae'  #rmse #'f1' # 'accuracy' 
N_ESTIMATOR = 5

EVAL_MODELS = [
                # 'default',
                'MPL',
                'CNN', 
                'LSTM', 
                'bi-LSTM',
                'conv-LSTM', 
                #'seg-gru',
                ]

PARAM_GRID = {
    'lr': [0.01, 0.005, 0.0005],
    'batch_size': [16, 32],
    
    # 'hidden_layers': [[75,19]],
    'dropout_rate': [0, 0.005, 0.01, ],
    'hidden_layers': [[64, 32], [128, 64, 32], [64],[75]],
    # 'activation_function': just use relu
}


from pathlib import Path
def set_output_dir(path):
    # Ensure the directory exists
    os.makedirs(path, exist_ok=True)
    return path
# Get the root project directory (the parent directory of kaggle_housing)
project_root = Path(__file__).resolve().parent.parent
# Define the output directory path relative to the project root
OUTPUT_DIR_A3 = project_root / 'outputs' / DATASET_SELECTION
DRAFT_VER_A3 = 1
# Set the directories using set_output_dir
AGGREGATED_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/aggregated_graphs')
Y_PRED_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/y_pred_graphs')
CV_LOSSES_PKL_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/pkl_cv')
PERFM_PKL_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/perf_pkl')
MODELS_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/saved_models')
LABEL_ENCODERS_PKL_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/label_encoders')
SOLUTIONS_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/solutions')
TXT_OUTDIR = set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/txt_stats')
OUTPUT_DIR_RAW_DATA_A3 =set_output_dir(OUTPUT_DIR_A3 / f'ver{DRAFT_VER_A3}_{EVAL_FUNC_METRIC}_etl{ETL_VERSION}/raw_data_assessments')

MODEL_ALL_LOG_FILE = os.path.join(os.getcwd(), TXT_OUTDIR, 'all_models_logs.txt')


#ML PARAMS
K_FOLD_CV = 5


from dotenv import load_dotenv
load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB_NAME = os.getenv('MYSQL_DB_NAME')
MYSQL_TABLE_NAME = os.getenv('MYSQL_TABLE_NAME')

MYSQL_CONFIG = {
    'user': MYSQL_USER,    
    'password': MYSQL_PASSWORD, 
    'host':MYSQL_HOST,    
    'port': MYSQL_PORT,
    'database': MYSQL_DB_NAME, 
    'raise_on_warnings': True,
}

