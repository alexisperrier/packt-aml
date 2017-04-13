'''
Next:
recreate cluster
reseed db without ID col
check schema
use create_data_source_from_redshift and subsequent model and evaluation creation to get a first eval score with QB

RMSE: 0.1540
RMSE baseline: 1.034
Difference: 0.880

then create other training / Eval DS with higher order
select x1, power(x1,2) as x2 from nonlinear limit 2;

Rewrite ch9 with switch to redshift  Info: why we use redshift instead of rds. rds requires advanced role and policies configuration.

QB vs non QB?


'''
import boto3
client = boto3.client('machinelearning')


k = 1
response = client.create_data_source_from_redshift(
    DataSourceId="CH9NL_training_b{}".format(k),
    DataSourceName="Ch9 NL training b{}".format(k),
    DataSpec={
        'DatabaseInformation': {
            'DatabaseName': 'amlpackt2',
            'ClusterIdentifier': 'amlpackt'
        },
        'SelectSqlQuery': 'select * from nonlinear order by random()',
        'DatabaseCredentials': {
            'Username': 'alexperrier',
            'Password': 'pwd:Packt17'
        },
        'S3StagingLocation': 's3://aml.packt/data/ch9/',
        'DataRearrangement': '{\"splitting\":{\"percentBegin\":0,\"percentEnd\":70 } }',
        'DataSchemaUri': 's3://aml.packt/data/ch9/nonlinear.csv.schema'
    },
    RoleARN='arn:aws:iam::178277513911:role/service-role/AmazonMLRedshift_us-east-1_amlpackt',
    ComputeStatistics=True
)


def cds(k):
    response = client.create_data_source_from_rds(
        DataSourceId="CH9_NL_training_z0{}".format(k),
        DataSourceName="Ch9 NL training z0{}".format(k),
        RDSData={
            'DatabaseInformation': {
                'InstanceIdentifier': 'amlpackt',
                'DatabaseName': 'amlpacktdb'
            },
            'SelectSqlQuery': 'select * from nonlinear order by random()',
            'DatabaseCredentials': {
                'Username': 'alexperrier',
                'Password': 'pwd:packt'
            },
            'ResourceRole': 'DataPipelineDefaultResourceRole',
            'ServiceRole': 'DataPipelineDefaultRole',
            'SubnetId': 'subnet-678f4e5a',
            'SecurityGroupIds': [
                'sg-e652bf99',
            ],
            'S3StagingLocation': 's3://aml.packt/data/ch9/',
            'DataRearrangement': '{\"splitting\":{\"percentBegin\":0,\"percentEnd\":70 } }',
            'DataSchemaUri': 's3://aml.packt/data/ch9/nonlinear.csv.schema'
        },
        RoleARN='arn:aws:iam::178277513911:role/MLtoRDS',
        ComputeStatistics=True
    )
    return response

def gds(ds_id):
    return client.get_data_source(
        DataSourceId=ds_id,
        Verbose=True
    )

response = cds(1)

gds(response['DataSourceId'])
gds('CH9_NL_training_z01')

ds_id = 'CH9_NL_training_z01'


pwd:Packt17


export RDS_CONNECT="-h amlpackt.c0rxegw7nac3.us-east-1.rds.amazonaws.com -p 5432 -U alexperrier --password -d amlpacktdb"
export PGPASSWORD="pwd:packt"


psql -h amlpackt.cenllwot8v9r.us-east-1.redshift.amazonaws.com -p 5439 -U alexperrier --password -d amlpacktdb


export RDS_CONNECT="-h amlpackt.cenllwot8v9r.us-east-1.redshift.amazonaws.com -p 5439 -U alexperrier --password -d amlpackt2"
export PGPASSWORD=pwd:Packt17


import pandas as pd

df = pd.read_csv('data/nonlinear.csv')


with open('data/nonlinear.csv', 'a') as file:
    for i,d in df.iterrows():
        file.write("insert into nonlinear (id,x1,y) values({0},{1},{2});\n".format(i,d.X,d.y)   )



cds(11)

PWD:packt67

RDSData={
        'DatabaseInformation': {
            'InstanceIdentifier': 'string',
            'DatabaseName': 'string'
        },
        'SelectSqlQuery': 'string',
        'DatabaseCredentials': {
            'Username': 'string',
            'Password': 'string'
        },
        'S3StagingLocation': 'string',
        'DataRearrangement': 'string',
        'DataSchema': 'string',
        'DataSchemaUri': 'string',
        'ResourceRole': 'string',
        'ServiceRole': 'string',
        'SubnetId': 'string',
        'SecurityGroupIds': [
            'string',
        ]
    },
    RoleARN='string',

    DataSpec={
        'DatabaseInformation': {
            'DatabaseName': 'string',
            'ClusterIdentifier': 'string'
        },
        'SelectSqlQuery': 'string',
        'DatabaseCredentials': {
            'Username': 'string',
            'Password': 'string'
        },
        'S3StagingLocation': 'string',
        'DataRearrangement': 'string',
        'DataSchema': 'string',
        'DataSchemaUri': 'string'
    },
    RoleARN='string',

