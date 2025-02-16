'''Collection of reusable helper functions refactored from EDA notebooks.'''

# PyPI imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def get_correlations(feature_pairs: list, df: pd.DataFrame, correlations: dict=None) -> dict:
    '''Takes list of feature name tuples and a dataframe, calculates Pearson 
    correlation coefficient and Spearman rank correlation coefficient using
    SciPy. Returns a dictionary with the results. Pass in results from an
    earlier call to append.'''

    # If results weren't passed in, start an empty dictionary to collect them
    if correlations is None:
        correlations={
            'Feature 1':[],
            'Feature 2':[],
            'Absolute Spearman':[],
            'Spearman':[],
            'Spearman p-value':[],
            'Absolute Pearson':[],
            'Pearson':[],
            'Pearson p-value':[],
            'Pearson r-squared':[]
        }

    # Loop on the feature pairs to calculate the corelation coefficients between each
    for feature_pair in feature_pairs:

        # Exclude self pairs
        if feature_pair[0] != feature_pair[1]:

            # Get data for this feature pair
            feature_pair_data=df[[*feature_pair]].dropna()

            # Replace any infinte values with nan and drop
            feature_pair_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            feature_pair_data.dropna(inplace=True)

            # Get Pearson and Spearman correlation coefficients and their p-values
            pcc=stats.pearsonr(feature_pair_data.iloc[:,0], feature_pair_data.iloc[:,1])
            src=stats.spearmanr(feature_pair_data.iloc[:,0], feature_pair_data.iloc[:,1])

            # Collect the results
            correlations['Feature 1'].append(feature_pair[0])
            correlations['Feature 2'].append(feature_pair[1])
            correlations['Absolute Spearman'].append(abs(src.statistic))
            correlations['Spearman'].append(src.statistic)
            correlations['Spearman p-value'].append(src.pvalue)
            correlations['Absolute Pearson'].append(pcc.statistic)
            correlations['Pearson'].append(pcc.statistic)
            correlations['Pearson p-value'].append(pcc.pvalue)
            correlations['Pearson r-squared'].append(pcc.statistic**2)

    return correlations


def plot_correlations(data_df: pd.DataFrame, correlations_df: pd.DataFrame) -> None:
    '''Takes a Pandas dataframe of features and a correlation dataframe for some or
    all of those features generated by get_correlations(). Plots each feature pair
    as scatter with best fit line. Uses kurtosis cutoff to decide which axes to log.'''

    fig, axs=plt.subplots(3,5, figsize=(11,7))
    fig.suptitle('Feature cross-correlations')

    for ax, (_, row) in zip(axs.flat, correlations_df.iterrows()):

        # Linear regression to show on plot
        feature_pair_data=data_df[[row['Feature 1'], row['Feature 2']]].dropna()
        regression=stats.linregress(feature_pair_data.iloc[:,0], feature_pair_data.iloc[:,1])
        regression_x=np.linspace(min(feature_pair_data.iloc[:,0]),max(feature_pair_data.iloc[:,0]))
        regression_y=regression.slope*regression_x + regression.intercept

        # Draw scatter plot with regression line
        ax.scatter(data_df[row['Feature 1']], data_df[row['Feature 2']], s=0.2, color='black')
        ax.plot(regression_x, regression_y, color='red')
        ax.set_xlabel(row['Feature 1'])
        ax.set_ylabel(row['Feature 2'])

        if stats.kurtosis(data_df[row['Feature 1']].dropna()) > 40:
            ax.set_xscale('log')

        if stats.kurtosis(data_df[row['Feature 2']].dropna()) > 40:
            ax.set_yscale('log')

    fig.tight_layout()

    return fig
