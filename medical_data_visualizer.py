import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')
print(df.info())
print(df.head(10))

# Add 'overweight' column
bmi_lambda = lambda row: 0 if (row["weight"]/(((row['height'])/100)**2)<=25) else 1
df['overweight'] = df.apply(bmi_lambda,axis=1)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
normalize_lambda = lambda x: 0 if x==1 else 1
df['cholesterol'] = df['cholesterol'].apply(normalize_lambda)
df['gluc'] = df['gluc'].apply(normalize_lambda)
df_cat = pd.melt(df,id_vars='id',value_vars =['cholesterol','gluc','smoke','alco','active','overweight'])
print(df_cat.head(10))
cardio_0 = df[df['cardio']==0]
cardio_1 = df[df['cardio']==1]
print(cardio_1.head())
print(cardio_0.head())
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,id_vars='id',value_vars =['cholesterol','gluc','smoke','alco','active','overweight'] )


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.melt(df, id_vars='cardio',var_name = 'variable', value_vars = ['active','alco','cholesterol', 'gluc','overweight','smoke'])

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, kind="count",  x="variable",hue="value", col="cardio").set_axis_labels("variable", "total")
    
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    filter1 = df['ap_lo'] <= df['ap_hi']
    filter2 = df['height'] >= df['height'].quantile(0.025)
    filter3 = df['height'] <= df['height'].quantile(0.975)
    filter4 = df['weight'] >= df['weight'].quantile(0.025)
    filter5 = df['weight'] <= df['weight'].quantile(0.975)
    df_heat = df[(filter1) & (filter2) & (filter3) & (filter4) & (filter5)]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=np.bool))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,vmin=0,vmax=.3,annot=True,mask=mask,linewidth=0.1, annot_kws={"fontsize":10},fmt='0.1f',cmap='magma')


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
