import boto3
import time
import json

# define the service you want to interact with
client = boto3.client('machinelearning')

trial = 6

# location of schemas and files
data_s3     = 's3://aml.packt/data/ch8/ames_housing_shuffled.csv'
schema_s3   = 's3://aml.packt/data/ch8/ames_housing.csv.schema'
recipe_s3   = 's3://aml.packt/data/ch8/recipe_ames_housing_default.json'

# algorithm parameters
sgd_params = {
    "sgd.shuffleType": "auto",
    "sgd.l1RegularizationAmount": "1.0E-04",
    "sgd.maxPasses": "100"
}
# set the object names and Ids
def name_id_generation(prefix, mode, trial):
    Id = '_'.join([prefix, mode, "%02d"%int(trial)])
    name   = "[%s] %s %02d"% (prefix, mode, int(trial)  )
    return {'Name':name, 'Id':Id}

# Create datasource for training
resource = name_id_generation('DS', 'training', trial)
print("Creating datasources for training (%s)"% resource['Name'] )
response = client.create_data_source_from_s3(
    DataSourceId    = resource['Id'] ,
    DataSourceName  = resource['Name'],
    DataSpec = {
        'DataLocationS3'        : data_s3,
        'DataSchemaLocationS3'  : schema_s3,
        'DataRearrangement':'{\"splitting\":{\"percentBegin\":0,\"percentEnd\":70}}'
    },
    ComputeStatistics = True
)

# Create datasource for validation
resource = name_id_generation('DS', 'validation', trial)
print("Creating datasources for validation (%s)"% resource['Name'] )
response = client.create_data_source_from_s3(
    DataSourceId    = resource['Id'] ,
    DataSourceName  = resource['Name'],
    DataSpec = {
        'DataLocationS3': data_s3,
        'DataSchemaLocationS3': schema_s3,
        'DataRearrangement':'{\"splitting\":{\"percentBegin\":70,\"percentEnd\":100}}'
    },
    ComputeStatistics = True
)

# Train model with existing recipe
resource = name_id_generation('MDL', '', trial) 
print("Training model (%s) with params:\n%s"% (resource['Name'], json.dumps(sgd_params, indent=4)) )
response = client.create_ml_model(
    MLModelId   = resource['Id'],
    MLModelName = resource['Name'],
    MLModelType = 'REGRESSION',
    Parameters  = sgd_params,
    TrainingDataSourceId= name_id_generation('DS', 'training', trial)['Id'],
    RecipeUri   = recipe_s3
)

# Create evaluation
resource = name_id_generation('EVAL', '', trial) 
print("Launching evaluation (%s) "% resource['Name'] )
response = client.create_evaluation(
    EvaluationId    = resource['Id'],
    EvaluationName  = resource['Name'],
    MLModelId       = name_id_generation('MDL', '', trial)['Id'],
    EvaluationDataSourceId = name_id_generation('DS', 'validation', trial)['Id']
)

# wait on evaluation

# start timing 
t0 = time.time()
waiter = client.get_waiter('evaluation_available')
print("Waiting on evaluation to finish ")
waiter.wait(FilterVariable='Name', EQ=name_id_generation('EVAL', '', trial)['Name'])
t = time.time() - t0

print("Evaluation has finished after %sm %ss"% (int(t/60), t%60)  )

response = client.get_evaluation(
    EvaluationId=name_id_generation('EVAL', '', trial)['Id']
)
print("="*40)
print("[trial %s] RMSE %0.2f"% (trial, float(response['PerformanceMetrics']['Properties']['RegressionRMSE'])) )


# Now delete the resources
print("Deleting datasources and model")
response = client.delete_data_source(
    DataSourceId=name_id_generation('DS', 'training', trial)['Id']
)

response = client.delete_data_source(
    DataSourceId=name_id_generation('DS', 'validation', trial)['Id']
)

response = client.delete_ml_model(
    MLModelId=name_id_generation('MDL', '', trial)['Id']
)

