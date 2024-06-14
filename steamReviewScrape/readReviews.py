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


df = pd.read_json(f'reviewsEAsample3.json', lines=True)
df1 = pd.read_json(f'reviewsBeta.json', lines=True)
df.columns = [col.replace(' ', '_') for col in df.columns]
df1.columns = [col.replace(' ', '_') for col in df1.columns]
df['Game_Type'] = 'EA'
df1['Game_Type'] = 'Beta'
df['Game_Type_Numeric'] = df['Game_Type'].map({'EA': 0, 'Beta': 1})
df1['Game_Type_Numeric'] = df1['Game_Type'].map({'EA': 0, 'Beta': 1})
df['Voted_Up_Numeric'] = df['Voted_Up'].map({False: 0, True: 1})
df1['Voted_Up_Numeric'] = df1['Voted_Up'].map({False: 0, True: 1})
df['Received_for_Free_Numeric'] = df['Received_for_Free'].map(
    {False: 0, True: 1})
df1['Received_for_Free_Numeric'] = df1['Received_for_Free'].map({
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
    ' Received_for_Free + Playtime_at_Review ~ Game_Type', data=new_df).mv_test()
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
    df['Received_for_Free'], df1['Received_for_Free'])
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
    df['Received_for_Free'], df1['Received_for_Free'])
print(f"Received for Free:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")
# t-stat = size of difference relative to variation in data (higher = more difference)
# p-value < 0.05 => there is significant difference in Review Score, Price, and Total Reviews between EA and Beta games


# # Correlation Matrix EA/Beta
variables = ['Game_Type_Numeric', 'Playtime_at_Review', 'Received_for_Free']
df_subset = new_df[variables]
correlation_matrix = df_subset.corr()
print(correlation_matrix)


# # Regression
X = sm.add_constant(new_df['Game_Type_Numeric'])

dependent_vars = ['Playtime_at_Review', 'Received_for_Free']

Y = new_df['Playtime_at_Review']
model = sm.OLS(Y, X).fit()
print(f"Playtime:")
print(model.summary())

Y = new_df['Received_for_Free']
model = sm.OLS(Y, X).fit()
print(f"Received for Free:")
print(model.summary())

# Interaction events:
# Playtime - 6651                 p<0.05
# Received for Free - 0.01        p<0.05


# # Multiple Linear Regression
X = sm.add_constant(new_df.dropna(subset=['Voted_Up_Numeric'])[
                    ['Playtime_at_Review', 'Received_for_Free_Numeric', 'Written_During_Early_Access_Numeric']])
dependent_vars = ['Voted_Up_Numeric', 'Playtime_at_Review',
                  'Received_for_Free_Numeric', 'Written_During_Early_Access_Numeric']

Y = new_df.dropna(subset=['Voted_Up_Numeric'])['Voted_Up_Numeric']
model = sm.OLS(Y, X).fit()
print(f"Review Score:")
print(model.summary())

# Interaction events:
# Playtime - 0.00000007          p<0.05
# Received for Free - 0.04       p<0.05
# Written during EA - -0.06      p<0.05

sys.exit()

# ------------------------- Received free -> Voted up
# ------------------------- Logistic regression and correlation
# Convert boolean columns to integers
df['Voted Up'] = df['Voted Up'].astype(int)
df['Received for Free'] = df['Received for Free'].astype(int)

# Calculate the percentage of people who voted up for games received for free
free_games_voted_up = df[df['Received for Free']
                         == 1]['Voted Up'].mean() * 100
print(f"Percentage of Voted-Up when received for free: {
    free_games_voted_up}%")

# Calculate the percentage of people who voted up for games not received for free
paid_games_voted_up = df[df['Received for Free']
                         == 0]['Voted Up'].mean() * 100
print(f"Percentage of Voted-Up when NOT received for free: {
    paid_games_voted_up}%")

# Stacked bar plot
cross_tab = pd.crosstab(df['Received for Free'], df['Voted Up'])
cross_tab.plot(kind='bar', stacked=True)
plt.title('Received for Free vs Voted Up')
plt.show()

# Correlation
correlation = df[['Received for Free', 'Voted Up']].corr()
print(correlation)

# Logistic Regression
X = df[['received_for_free']]
y = df['Voted Up']

# X = sm.add_constant(X)  # adding a constant

# model = sm.Logit(y, X)
# result = model.fit()

# print(result.summary())

# # ------------------------- Time Series -> # of Reviews, Avg Playtime, Voted Up
# df['timestamp_created'] = pd.to_datetime(df['timestamp_created'])
# df.set_index('timestamp_created', inplace=True)

# # Time series plot for the number of reviews
# df.resample('ME').size().plot()
# plt.title('Number of Reviews Over Time')
# plt.show()

# # Time series plot for the average playtime at review
# df.resample('ME')['playtime_at_review'].mean().plot()
# plt.title('Average Playtime at Review Over Time')
# plt.show()

# # Time series plot for the proportion of reviews voted up
# df.resample('ME')['voted_up'].mean().plot()
# plt.title('Proportion of Reviews Voted Up Over Time')
# plt.show()

# # ------------------------- Play Time -> # of Reviews, Voted Up
# # Define the bin edges
# bins = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000,
#         8000, 9000, 10000, df['playtime_at_review'].max()]

# # Create the bins
# df['playtime_bins'] = pd.cut(
#     df['playtime_at_review'], bins, include_lowest=True)

# # Scatter plot for the number of reviews vs binned playtime at review
# reviews_df = df.groupby('playtime_bins').size().reset_index(name='count')
# reviews_df.plot(kind='bar', x='playtime_bins', y='count')
# plt.title('Number of Reviews vs Binned Playtime at Review')
# plt.show()

# # Scatter plot for the proportion of reviews voted up vs binned playtime at review
# votes_df = df.groupby('playtime_bins')[
#     'voted_up'].mean().reset_index(name='mean')
# votes_df.plot(kind='bar', x='playtime_bins', y='mean')
# plt.title('Proportion of Reviews Voted Up vs Binned Playtime at Review')
# plt.show()
