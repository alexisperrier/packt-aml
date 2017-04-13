# NEXT
# make 6 validation for each
#  - original Titanic, default recipe (same)
#  - original Titanic, NO QB recipe 
#  - extended Titanic, default recipe

# specify recipe file
# loop over 3 models, with 2 validations each
# get AUC score back

import pandas as pd
import numpy as np
import json
import csv
import os

def json_dsrc(mode, percentBegin, percentEnd):
    return {
        "DataSourceId": "dsrc.ch6.ttnc_ext.%s.%s"% (mode, experiment),
        "DataSourceName": "DS Titanic %s [%s]"% (mode, experiment),
        "DataSpec": {
            "DataLocationS3": "%s%s"% (s3_path, filenames['main']),
            "DataSchemaLocationS3": "%s%s"% (s3_path, filenames['schema']),
            "DataRearrangement": "{\"splitting\":{\"percentBegin\":%s,\"percentEnd\":%s}}"% (percentBegin, percentEnd)
        },
        "ComputeStatistics": True
    }

def create_dsrc(mode, percentBegin, percentEnd):
    with open(cli_path + "%s_datasource.json"%mode, 'w') as outfile:
        json.dump(json_dsrc(mode, percentBegin, percentEnd), outfile, indent=4)
    print("aws machinelearning create-data-source-from-s3 --cli-input-json file://%s%s_datasource.json"% (cli_path, mode))

def json_model():
    return {
        "MLModelId": "mdl.ch6.ttnc_ext.%s"% experiment,
        "MLModelName": "Model Titanic [%s]"% experiment,
        "MLModelType": "BINARY",
        "Parameters": {
            "sgd.maxPasses": "100",
            "sgd.shuffleType": "auto",
            "sgd.l2RegularizationAmount": "1.0E-06"
        },
        "TrainingDataSourceId": "dsrc.ch6.ttnc_ext.%s.%s"% ("train", experiment),
        "RecipeUri": "s3://aml.packt/data/no_qb_recipe.json"
    }

def create_model():
    with open(cli_path + "generate_model.json", 'w') as outfile:
        json.dump(json_model(), outfile, indent=4)
    os.system("aws machinelearning create-ml-model --cli-input-json file://%sgenerate_model.json"% cli_path)

def json_eval(mode):
    return {
        "EvaluationId": "eval.ch6.ttnc_ext.%s.%s"% (mode, experiment),
        "EvaluationName": "Eval Titanic %s [%s]"% (mode, experiment),
        "MLModelId": "mdl.ch6.ttnc_ext.%s"% experiment,
        "EvaluationDataSourceId": "dsrc.ch6.ttnc_ext.%s.%s"% (mode, experiment)
    }

def create_eval(mode = 'valid'):
    with open(cli_path + "generate_eval_%s.json"% mode, 'w') as outfile:
        json.dump(json_eval(mode), outfile, indent=4)
    os.system("aws machinelearning create-evaluation --cli-input-json file://%sgenerate_eval_%s.json"% (cli_path, mode))

def json_prediction(mode):
    return {
        "BatchPredictionId": "prd.ch6.ttnc_ext.%s.%s"% (mode,experiment),
        "BatchPredictionName": "Pred Titanic %s [%s]"% (mode,experiment),
        "MLModelId": "mdl.ch6.ttnc_ext.%s"% experiment,
        "BatchPredictionDataSourceId": "dsrc.ch6.ttnc_ext.%s.%s"% (mode, experiment),
        "OutputUri": "s3://aml.packt/"
    }

def create_prediction(mode = 'test'):
    with open(cli_path + "generate_prediction_%s.json"% mode, 'w') as outfile:
        json.dump(json_prediction(mode), outfile, indent=4)
    os.system("aws machinelearning create-batch-prediction --cli-input-json file://%sgenerate_prediction_%s.json"% (cli_path, mode))

def get_batch_prediction(mode):
    command_str = "aws machinelearning get-batch-prediction --batch-prediction-id prd.ch6.ttnc_ext.%s.%s"% (mode,experiment)
    (output, err) = subprocess.Popen(command_str, stdout=subprocess.PIPE, shell=True).communicate()
    print(output.decode("utf-8"))
    print("aws s3 cp %sprd.ch6.ttnc_ext.%s.%s-%s.gz %s"% (s3_result_path,mode,experiment,filenames['main'], filepath) )
    return output.decode("utf-8")

def get_evaluation(evaluation_id):
    command_str = "aws machinelearning get-evaluation --evaluation-id %s"% evaluation_id
    (output, err) = subprocess.Popen(command_str, stdout=subprocess.PIPE, shell=True).communicate()
    res = json.loads( output.decode("utf-8"))
    auc = float(res['PerformanceMetrics']['Properties']['BinaryAUC'])
    print("%0.3f"%auc)
    return auc


filepath = '/Users/alexisperrier/apps/packt/assets/ch6/data/'
cli_path = '/Users/alexisperrier/apps/packt/assets/ch6/cli/'
s3_path = 's3://aml.packt/data/'
s3_result_path = 's3://aml.packt/batch-prediction/result/'

def run_experiment(experiment_type):
    filenames = generate_filenames(experiment_type)

    # load, shuffle and save
    df = pd.read_csv(filepath + filenames['main'])
    df = df.reindex(np.random.permutation(df.index))
    df.to_csv(filepath + filenames['main'], quoting= csv.QUOTE_NONNUMERIC, index=False)
    os.system("aws s3 cp %s%s %s "% (filepath, filenames['main'], s3_path) )

    # write cli JSON
    create_dsrc("train", 0, 60)
    create_dsrc("valid", 60, 80)
    create_dsrc("test", 80, 100)

    create_model()
    create_eval("valid")
    create_eval("test")


# Files


results = {
    'default': [0.861, 0.815], 
    'extended': [0.872, 0.857], 
    'no_qb': [0.845, 0.796]
}

def generate_filenames(experiment_type):
    if experiment_type == 'default':
        return {
            'main': "ch6_original_titanic.csv",
            'train': "ch6_titanic.train.%s.csv"% experiment,
            'valid': "ch6_titanic.valid.%s.csv"% experiment,
            'test': "ch6_titanic.test.%s.csv"% experiment,
            'schema': "ch6_original_titanic.csv.schema",
            'recipe': "default_recipe.json",
        }
    elif experiment_type == 'no_qb':
        return {
            'main': "ch6_original_titanic.csv",
            'train': "ch6_titanic.train.%s.csv"% experiment,
            'valid': "ch6_titanic.valid.%s.csv"% experiment,
            'test': "ch6_titanic.test.%s.csv"% experiment,
            'schema': "ch6_original_titanic.csv.schema",
            'recipe': "no_qb_recipe.json",
        }
    elif experiment_type == 'extended':
        return {
            'main': "ch6_extended_titanic.csv",
            'train': "ch6_titanic.train.%s.csv"% experiment,
            'valid': "ch6_titanic.valid.%s.csv"% experiment,
            'test': "ch6_titanic.test.%s.csv"% experiment,
            'schema': "ch6_extended_titanic.csv.schema",
            'recipe': "extended_recipe.json",
        }

experiment = 'C01_default'
run_experiment('default')
experiment = 'C02_default'
run_experiment('default')

auc = get_evaluation("eval.ch6.ttnc_orig.valid.C01_default")
results['default'].append(auc)
auc = get_evaluation("eval.ch6.ttnc_orig.test.C01_default")
results['default'].append(auc)
auc = get_evaluation("eval.ch6.ttnc_orig.valid.C02_default")
results['default'].append(auc)
auc = get_evaluation("eval.ch6.ttnc_orig.test.C02_default")
results['default'].append(auc)

experiment = 'D01_NOQB'
run_experiment('no_qb')
experiment = 'D03_NOQB'
run_experiment('no_qb')


results['no_qb'].append(get_evaluation("eval.ch6.ttnc_orig.valid.D01_NOQB"))
results['no_qb'].append(get_evaluation("eval.ch6.ttnc_orig.test.D01_NOQB"))

experiment = 'E01_EXT'
run_experiment('extended')

experiment = 'E05_EXT'
run_experiment('extended')

results['extended'].append(get_evaluation("eval.ch6.ttnc_ext.valid.E04_EXT"))
results['extended'].append(get_evaluation("eval.ch6.ttnc_ext.test.E04_EXT"))
results['extended'].append(get_evaluation("eval.ch6.ttnc_ext.valid.E05_EXT"))
results['extended'].append(get_evaluation("eval.ch6.ttnc_ext.test.E05_EXT"))


