import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.multivariate.manova import MANOVA


# Games
# ID                        int64
# Title                    object
# Description              object
# Discount                float64
# Previous Price          float64
# Current Price           float64
# Categories               object
# Release Date             object
# Review Summary           object
# Review Number             int64
# API Review Summary       object
# API Review Number         int64
# API Positive Reviews      int64
# API Negative Reviews      int64
# Link                     object

# Reviews
# ID                                      int64
# Review                                 object
# Language                               object
# Playtime at Review                      int64
# Voted Up                                 bool
# Steam Purchase                           bool
# Received for Free                        bool
# Written During Early Access              bool
# Timestamp Created              datetime64[ns]
# Timestamp Updated              datetime64[ns]

def format_time(minutes):
    # Convert minutes to hours and minutes
    hours, minutes = divmod(minutes, 60)
    # Convert hours to days and hours
    days, hours = divmod(hours, 24)
    # Return the time in the format '00:00:00'
    return f'{int(days):02d}:{int(hours):02d}:{int(minutes):02d} (dd:hh:mm)'
# All with text
# df = pd.read_json(f'filesToIgnore/allreviews.json', lines=True)
# All no text
# df = pd.read_json(f'filesToIgnore/allreviews_no_text.json', lines=True)
# df = df.sample(n=10000)


# change later
df_ea_full = pd.read_json(f'reviewsEA.json', lines=True)
df = pd.read_json(f'reviewsEAsample3.json', lines=True)
df1 = pd.read_json(f'reviewsBeta.json', lines=True)
df_ea_full.columns = [col.replace(' ', '_') for col in df_ea_full.columns]
df.columns = [col.replace(' ', '_') for col in df.columns]
df1.columns = [col.replace(' ', '_') for col in df1.columns]
df['Game_Type'] = 'EA'
df1['Game_Type'] = 'Beta'
df['Game_Type_Numeric'] = df['Game_Type'].map({'EA': 0, 'Beta': 1})
df1['Game_Type_Numeric'] = df1['Game_Type'].map({'EA': 0, 'Beta': 1})
df_ea_full['Voted_Up_Numeric'] = df_ea_full['Voted_Up'].map(
    {False: 0, True: 1})
df['Voted_Up_Numeric'] = df['Voted_Up'].map({False: 0, True: 1})
df1['Voted_Up_Numeric'] = df1['Voted_Up'].map({False: 0, True: 1})
df_ea_full['Received_for_Free_Numeric'] = df_ea_full['Received_for_Free'].map(
    {False: 0, True: 1})
df['Received_for_Free_Numeric'] = df['Received_for_Free'].map(
    {False: 0, True: 1})
df1['Received_for_Free_Numeric'] = df1['Received_for_Free'].map({
                                                                False: 0, True: 1})
df_ea_full['Written_During_Early_Access_Numeric'] = df_ea_full['Written_During_Early_Access'].map({
    False: 0, True: 1})
df['Written_During_Early_Access_Numeric'] = df['Written_During_Early_Access'].map({
                                                                                  False: 0, True: 1})
df1['Written_During_Early_Access_Numeric'] = df1['Written_During_Early_Access'].map({
                                                                                    False: 0, True: 1})
new_df = pd.concat([df, df1])

# # # # ------------- Summarizing the data ------------- # # # #
average_playtime_ea = format_time(df['Playtime_at_Review'].mean())
positive_review_proportion_ea = df['Voted_Up'].mean()
early_access_review_proportion_ea = df['Written_During_Early_Access'].mean()
average_playtime_beta = format_time(df1['Playtime_at_Review'].mean())
positive_review_proportion_beta = df1['Voted_Up'].mean()
early_access_review_proportion_beta = df1['Written_During_Early_Access'].mean()
print(f'Average Playtime: EA {
      average_playtime_ea} vs Beta {average_playtime_beta}')
print(f'Positive Reviews: EA {
      round(positive_review_proportion_ea, 4)*100}% vs Beta {round(positive_review_proportion_beta, 4)*100}%')
print(f'Reviews Written During Early Access: EA {
      round(early_access_review_proportion_ea, 4)*100}% vs Beta {round(early_access_review_proportion_beta, 4)*100}%')

received_for_free_counts_ea = df['Received_for_Free'].value_counts()
received_for_free_counts_beta = df1['Received_for_Free'].value_counts()
prop1 = received_for_free_counts_ea.iloc[1]/received_for_free_counts_ea.iloc[0]
prop2 = received_for_free_counts_beta.iloc[1] / \
    received_for_free_counts_beta.iloc[0]
print(f'Reviews that received the game for Free: EA {
      round(prop1, 4)*100}% vs Beta {round(prop2, 4)*100}%')


df_free_ea = df[df['Received_for_Free'] == True]
df_free_beta = df1[df1['Received_for_Free'] == True]
df_not_free_ea = df[df['Received_for_Free'] == False]
df_not_free_beta = df1[df1['Received_for_Free'] == False]
positive_review_proportion_free_ea = df_free_ea['Voted_Up'].mean()
positive_review_proportion_free_beta = df_free_beta['Voted_Up'].mean()
positive_review_proportion_not_free_ea = df_not_free_ea['Voted_Up'].mean()
positive_review_proportion_not_free_beta = df_not_free_beta['Voted_Up'].mean()
print(f'Positive Reviews (Received for Free): EA {round(
    positive_review_proportion_free_ea, 4)*100}% vs Beta {round(positive_review_proportion_free_beta, 4)*100}%')
print(f'Positive Reviews (Not Received for Free): EA {round(
    positive_review_proportion_not_free_ea, 4)*100}% vs Beta {round(positive_review_proportion_not_free_beta, 4)*100}%')


# region ANALISYS
# # # # # # # # # # # # # # # # # # # # # # ANALISYS # # # # # # # # # # # # # # # # # # # # # #

# # MANOVA
manova = MANOVA.from_formula(
    ' Received_for_Free_Numeric + Playtime_at_Review ~ Game_Type_Numeric', data=new_df).mv_test()
print(manova)

# all p-values < 0.005 therefore there is significant difference between the groups
# Wilks' lambda: Tests the null hypothesis that the group means are equal. A smaller value indicates more evidence against the null hypothesis.
# Pillai's trace: A more robust test that is less sensitive to deviations from multivariate normality.
# Hotelling-Lawley trace: Another test for the multivariate effect.
# Roy's greatest root: Focuses on the largest eigenvalue of the test matrix and is particularly sensitive to the largest effect.

# # One-Way ANOVAs
f_val, p_val = stats.f_oneway(
    df['Playtime_at_Review'], df1['Playtime_at_Review'])
print(f"Playtime:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

f_val, p_val = stats.f_oneway(
    df['Received_for_Free_Numeric'], df1['Received_for_Free_Numeric'])
print(f"Received for Free:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

# F-value = ratio of variance btw groups to variance within groups (higher = more difference)
# p-value < 0.05 => there is significant difference in Review Score, Price, and Total Reviews between EA and Beta games
# no significant difference was found for the Discount


# # T-tests
t_stat, p_value = stats.ttest_ind(
    df['Playtime_at_Review'], df1['Playtime_at_Review'])
print(f"Playtime:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

t_stat, p_value = stats.ttest_ind(
    df['Received_for_Free_Numeric'], df1['Received_for_Free_Numeric'])
print(f"Received for Free:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")
# t-stat = size of difference relative to variation in data (higher = more difference)
# p-value < 0.05 => there is significant difference in Review Score, Price, and Total Reviews between EA and Beta games


# # Correlation Matrix EA/Beta
variables = ['Game_Type_Numeric',
             'Playtime_at_Review', 'Received_for_Free_Numeric']
df_subset = new_df[variables]
correlation_matrix = df_subset.corr()
print(correlation_matrix)


# # Regression
X = sm.add_constant(new_df['Game_Type_Numeric'])

dependent_vars = ['Playtime_at_Review', 'Received_for_Free_Numeric']

Y = new_df['Playtime_at_Review']
model = sm.OLS(Y, X).fit()
print(f"Playtime:")
print(model.summary())

Y = new_df['Received_for_Free_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Received for Free:")
print(model.summary())

# Interaction events:
# Playtime - 6651                 p<0.05
# Received for Free - 0.01        p<0.05


# # Multiple Linear Regression
independent_vars = ['Playtime_at_Review',
                    'Received_for_Free_Numeric', 'Written_During_Early_Access_Numeric']
dependent_var = ['Voted_Up_Numeric']

X = sm.add_constant(new_df.dropna(subset=['Voted_Up_Numeric'])[
                    ['Playtime_at_Review', 'Received_for_Free_Numeric', 'Written_During_Early_Access_Numeric']])
Y = new_df.dropna(subset=['Voted_Up_Numeric'])['Voted_Up_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Review Score:")
print(model.summary())

X = sm.add_constant(df_ea_full.dropna(subset=['Voted_Up_Numeric'])[
                    ['Playtime_at_Review', 'Received_for_Free_Numeric']])
Y = df_ea_full.dropna(subset=['Voted_Up_Numeric'])['Voted_Up_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Review Score:")
print(model.summary())

X = sm.add_constant(df.dropna(subset=['Voted_Up_Numeric'])[
                    ['Playtime_at_Review', 'Received_for_Free_Numeric']])
Y = df.dropna(subset=['Voted_Up_Numeric'])['Voted_Up_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Review Score:")
print(model.summary())

X = sm.add_constant(df1.dropna(subset=['Voted_Up_Numeric'])[
                    ['Playtime_at_Review', 'Received_for_Free_Numeric', 'Written_During_Early_Access_Numeric']])
Y = df1.dropna(subset=['Voted_Up_Numeric'])['Voted_Up_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Review Score:")
print(model.summary())

# Interaction events:
# Both Sets
# Playtime - 0.00000007          p<0.05
# Received for Free - 0.04       p<0.05
# Written during EA - -0.06      p<0.05
# Full EA Set
# Playtime - 0.00000008          p<0.05
# Received for Free - 0.04       p<0.05
# EA Set
# Playtime - 0.000004            p<0.05
# Beta Set
# Playtime - 0.00000009           p<0.05
# Received for Free - 0.034       p<0.05
# Written during EA - not significant


# # ------------------------- Time Series -> # of Reviews, Avg Playtime, Voted Up
df['Timestamp_Created'] = pd.to_datetime(df['Timestamp_Created'])
df.set_index('Timestamp_Created', inplace=True)

# Time series plot for the number of reviews
df.resample('ME').size().plot()
plt.title('Number of Reviews Over Time')
plt.show()

# # Time series plot for the average playtime at review
df.resample('ME')['Playtime_at_Review'].mean().plot()
plt.title('Average Playtime at Review Over Time')
plt.show()

# # Time series plot for the proportion of reviews voted up
df.resample('ME')['Voted_Up'].mean().plot()
plt.title('Proportion of Reviews Voted Up Over Time')
plt.show()

# # ------------------------- Play Time -> # of Reviews, Voted Up
# # Define the bin edges
bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000,
        8000, 9000, 10000, df['Playtime_at_Review'].max()]

# # Create the bins
df['Playtime_Bins'] = pd.cut(
    df['Playtime_at_Review'], bins, include_lowest=True)

# # Scatter plot for the number of reviews vs binned playtime at review
reviews_df = df.groupby('Playtime_Bins').size().reset_index(name='count')
reviews_df.plot(kind='barh', x='Playtime_Bins', y='count')
plt.title('Number of Reviews vs Binned Playtime at Review')
plt.show()

# # Scatter plot for the proportion of reviews voted up vs binned playtime at review
votes_df = df.groupby('Playtime_Bins')[
    'Voted_Up'].mean().reset_index(name='mean')
votes_df.plot(kind='barh', x='Playtime_Bins', y='mean')
plt.title('Proportion of Reviews Voted Up vs Binned Playtime at Review')
plt.show()
