import matplotlib.pyplot as plt
import pandas as pd
%matplotlib

df = pd.read_csv('data/nonlinear.csv', names = ['x','y'])

fig, ax = plt.subplots(1,1, figsize=(6,6))

ax.set_axis_bgcolor('white')
ax.plot(df.x,df.y, '.')
ax.set_title('Non linear dataset')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('x')
ax.set_ylabel('y')


plt.tight_layout()
plt.show()

plt.savefig('B05028_09_11.png', dpi=180, facecolor='white', transparent=False)

ax.get_yaxis().set_ticks([])

# rmse per power
df = pd.read_csv('data/results_noqb_aml_5_5.csv')
# df = pd.read_csv('data/results_QB_aml_5_5.csv')

fig, ax = plt.subplots(1,1, figsize=(6,6))
ax.set_axis_bgcolor('white')

for p in range(1,6):
    cond = df.p == p
    ax.plot(df[cond].rmse, label = 'p={0}'.format(p))

ax.set_title('RMSE polynomial regression')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('trials')
ax.set_ylabel('RMSE')
plt.legend(loc='best')
plt.show()


ax.annotate("p=1", xy = (0.8,1.04), color = 'black', size=14 )
ax.annotate("p=2", xy = (6,1.06), color = 'black', size=14 )
ax.annotate("p=3", xy = (11,0.91), color = 'black', size=14 )
ax.annotate("p=4", xy = (15.4,0.90), color = 'black', size=14 )
ax.annotate("p=5", xy = (21,0.91), color = 'black', size=14 )

plt.savefig('B05028_09_15.png', dpi=180, facecolor='white', transparent=False)