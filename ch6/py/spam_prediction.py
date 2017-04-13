import boto3
import json
import pandas as pd

# Define the service
client = boto3.client('machinelearning')

# Endpoint url given in the model summary
endpoint_url = "https://realtime.machinelearning.us-east-1.amazonaws.com"

# Model id to be used
model_id = "ml-kJmiRHyn1UM"

# The actual sample to be predicted. JSON formatted
record = {
        "body": "Hello world, my name is Alex"
    }

record = {
        "body": "Call now to get free contacts for free, no cash no credit card. "
    }

# use the predict() method of the machine learning service
response = client.predict(    
    MLModelId       = model_id,
    Record          = record,
    PredictEndpoint = endpoint_url
)

print(json.dumps(response, indent=4))

# ---------------------------------------------------------------------------------
#  Predict real time endpoint
# ---------------------------------------------------------------------------------

filename = "assets/ch6/data/spam_heldout.csv"

import boto3
import json
import pandas as pd

# Initialize the Service, the Model ID and the endpoint url
client = boto3.client('machinelearning')
endpoint_url = "https://realtime.machinelearning.us-east-1.amazonaws.com"
model_id = "ml-kJmiRHyn1UM"

# Recall which class is spam and which is ham
spam_label = {'0': 'ham', '1':'spam'}

# Load the held out dataset into a panda DataFrame
df = pd.read_csv(filename)
df['predicted'] = -1
df['predicted_score'] = -1

# Loop over each DataFrame rows    
for index, row in df.iterrows():
    record = { "body": row['sms'] }
    response = client.predict(    
        MLModelId       = model_id,
        Record          = record,
        PredictEndpoint = endpoint_url
    )
    predicted_label = response['Prediction']['predictedLabel']
    predicted_score = response['Prediction']['predictedScores'][predicted_label]
    print("[%s] %s (%0.2f):\t %s "% (spam_label[str(row['nature'])], 
                                spam_label[predicted_label], 
                                predicted_score, 
                                row['sms'] ) 
    )

    df.loc[index, 'predicted'] = int(response['Prediction']['predictedLabel'])

# ---------------------------------------------------------------------------------
#  ROC AUC
# ---------------------------------------------------------------------------------


import boto3
import json
import pandas as pd
from sklearn import metrics


# Initialize the Service, the Model ID and the endpoint url
client = boto3.client('machinelearning')
endpoint_url = "https://realtime.machinelearning.us-east-1.amazonaws.com"
model_id = "ml-kJmiRHyn1UM"

# Load the held out dataset into a panda DataFrame
df = pd.read_csv(filename)
df['predicted'] = -1
df['predicted_score'] = -1
# df = df[100:300]
# Loop over each DataFrame rows    
for index, row in df.iterrows():
    record = { "body": row['sms'] }
    response = client.predict(    
        MLModelId       = model_id,
        Record          = record,
        PredictEndpoint = endpoint_url
    )
    predicted_label = response['Prediction']['predictedLabel']
    predicted_score = response['Prediction']['predictedScores'][predicted_label]
    print("[%s] %s (%0.2f):\t %s "% (spam_label[str(row['nature'])], 
                                spam_label[predicted_label], 
                                predicted_score, 
                                row['sms'] ) 
    )

    df.loc[index, 'predicted'] = int(response['Prediction']['predictedLabel'])
    df.loc[index, 'predicted_score'] = predicted_score

fpr, tpr, threshold = metrics.roc_curve(df.nature, df.predicted_score)
roc_auc = metrics.auc(fpr, tpr)


import matplotlib.pyplot as plt
%matplotlib


fig, ax = plt.subplots(1,1, figsize=(8,8))

ax.set_axis_bgcolor('white')
ax.set_title('ROC - Spam dataset')
ax.grid()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('True Positive Rate')
ax.set_ylabel('False Positive Rate')

ax.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
ax.plot([0, 1], [0, 1],'r--')

ax.legend(loc='lower right')
ax.set_xlim(-0.05, 1.)
ax.set_ylim(0, 1.05)
plt.tight_layout()
plt.show()

plt.savefig('B05028_06_12.png', dpi=180, facecolor='white', transparent=False)


