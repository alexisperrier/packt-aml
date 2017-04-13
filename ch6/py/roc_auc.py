import pandas as pd
from sklearn import metrics

# open files
filename = 'assets/ch6/data/bp-yTDNSArMqa6-ch6_titanic_heldout.csv'
filename = 'assets/ch6/data/bp-TOJ2OLAUaRq-ch6_titanic_train.csv'
df = pd.read_csv(filename)

# true and false positive rate 
filename = 'assets/ch6/data/bp-TOJ2OLAUaRq-ch6_titanic_train.csv'
# NO QB AUC NO QB: 0.83914177335229978
filename = 'assets/ch6/data/bp-Bqv33ql2100-ch6_titanic_heldout.csv'
df = pd.read_csv(filename)
fpr, tpr, threshold = metrics.roc_curve(df.trueLabel, df.score)
roc_auc = metrics.auc(fpr, tpr)

# Extended AUC : 
filename = 'assets/ch6/data/bp-2DTY8LqSiTX-ch6_extended_titanic_heldout.csv'
prediction_file = 'assets/ch6/data/prd.ch6.ttnc_extd.test.009-ch6_extended_titanic.csv'
dfpred = pd.read_csv(prediction_file)
fpr, tpr, threshold = metrics.roc_curve(dfpred.trueLabel, dfpred.score)
roc_auc = metrics.auc(fpr, tpr)


# Plot the ROC curve

import matplotlib.pyplot as plt

%matplotlib


fig, ax = plt.subplots(1,1, figsize=(8,8))

ax.set_axis_bgcolor('white')
ax.set_title('ROC - Titanic')
ax.grid()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('True Positive Rate')
ax.set_ylabel('False Positive Rate')

filename = 'assets/ch6/data/bp-yTDNSArMqa6-ch6_titanic_heldout.csv'
df = pd.read_csv(filename)
fpr, tpr, threshold = metrics.roc_curve(df.trueLabel, df.score)
roc_auc = metrics.auc(fpr, tpr)

ax.plot(fpr, tpr, 'b', label='AUC = %0.2f (held out)' % roc_auc)

filename = 'assets/ch6/data/bp-TOJ2OLAUaRq-ch6_titanic_train.csv'
df = pd.read_csv(filename)
fpr, tpr, threshold = metrics.roc_curve(df.trueLabel, df.score)
roc_auc = metrics.auc(fpr, tpr)

ax.plot(fpr, tpr, 'b:', label='AUC = %0.2f (validation)' % roc_auc)


ax.plot([0, 1], [0, 1],'r--')

ax.legend(loc='best')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
# plt.tight_layout()
plt.show()
plt.savefig('B05028_06_06.png', dpi=180, facecolor='white', transparent=False)


