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
# Review Summary Score      int64
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

np.random.seed(0)
review_scores = {
    'Overwhelmingly Positive': 4,
    'Very Positive': 3,
    'Positive': 2,
    'Mostly Positive': 1,
    'Mixed': 0,
    'Mostly Negative': -1,
    'Negative': -2,
    'Very Negative': -3,
    'Overwhelmingly Negative': -4,
}
review_scores_labels = {v: k for k, v in review_scores.items()}
positive_review_scores = {v: k for k, v in review_scores.items() if v >= -1}
df_ea_full = pd.read_json('gamesEA.json', lines=True)
df = pd.read_json('gamesEAsample2.json', lines=True)
df1 = pd.read_json('gamesBeta.json', lines=True)

df_ea_full.columns = [col.replace(' ', '_') for col in df_ea_full.columns]
df.columns = [col.replace(' ', '_') for col in df.columns]
df1.columns = [col.replace(' ', '_') for col in df1.columns]
df_ea_full['Release_Date'] = pd.to_datetime(df_ea_full['Release_Date'])
df['Release_Date'] = pd.to_datetime(df['Release_Date'])
df1['Release_Date'] = pd.to_datetime(df1['Release_Date'])
df_ea_full['Release_Date_Epoch'] = (
    pd.Timestamp.today() - df_ea_full['Release_Date']) / pd.Timedelta('1D')
df['Release_Date_Epoch'] = (
    pd.Timestamp.today() - df['Release_Date']) / pd.Timedelta('1D')
df1['Release_Date_Epoch'] = (
    pd.Timestamp.today() - df1['Release_Date']) / pd.Timedelta('1D')
# df_ea_full['Release_Date_Epoch'] = (df_ea_full['Release_Date'] -
#                                     pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
# df['Release_Date_Epoch'] = (df['Release_Date'] -
#                             pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
# df1['Release_Date_Epoch'] = (df1['Release_Date'] -
#                              pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
df_ea_full['Game_Type'] = 'EA'
df['Game_Type'] = 'EA'
df1['Game_Type'] = 'Beta'
df_ea_full['Game_Type_Numeric'] = df_ea_full['Game_Type'].map(
    {'EA': 0, 'Beta': 1})
df['Game_Type_Numeric'] = df['Game_Type'].map({'EA': 0, 'Beta': 1})
df1['Game_Type_Numeric'] = df1['Game_Type'].map({'EA': 0, 'Beta': 1})

# # # # ------------- Summarizing the data ------------- # # # #
df_eaSummary = df_ea_full.describe().drop(
    ['ID', 'Release_Date', 'Game_Type_Numeric', 'Previous_Price', 'Review_Number'], axis=1)
dfSummary = df.describe().drop(
    ['ID', 'Release_Date', 'Game_Type_Numeric', 'Previous_Price', 'Review_Number'], axis=1)
df1Summary = df1.describe().drop(
    ['ID', 'Release_Date', 'Game_Type_Numeric', 'Previous_Price', 'Review_Number'], axis=1)
print(df_eaSummary)
print(dfSummary)
print(df1Summary)
# Conclusions
# EA games are :
# -cheaper (avg $8-$10) vs (avg $20)
# -have lower score (avg 1-1.5) vs (avg 3.4)
# -have less reviews (avg 50-2000) vs (avg 84,000)
# -ratio positive/negative reviews is worse in most cases (outlier in sample 2)
# -Still we have to test with ANOVA if differences are significant
all_categories_ea_full = df_ea_full['Categories'].explode()
top_10_categoriess_ea_full = all_categories_ea_full.value_counts().head(10)
print(top_10_categoriess_ea_full)
all_categories_ea = df['Categories'].explode()
top_10_categoriess_ea = all_categories_ea.value_counts().head(10)
print(top_10_categoriess_ea)
all_categories_beta = df1['Categories'].explode()
top_10_categoriess_beta = all_categories_beta.value_counts().head(10)
print(top_10_categoriess_beta)
# -250 different categories
# -top 10 EA -> Indie, Action, Singleplayer, Adventure, Casual, Simulation, Strategy, RPG, Multiplayer, Fantasy
# -top 10 Beta -> Indie, Action, Simulation, Adventure, Strategy, RPG, Casual, Massively Multiplayer, Free to Play, Sports
# -maybe EA should focus more on Indie and Multiplayer games rather than Singleplayer

# region PLOTS
# # # # # # # # # # # # # # # # # # # # # # PLOTS # # # # # # # # # # # # # # # # # # # # # #
# # # # ------------- Price ------------- # # # #
# # # Box plot
# df_prices = pd.concat([df['Current_Price'], df1['Current_Price']], axis=1)
# df_prices.columns = ['EA', 'Beta']
# df_prices.plot.box(figsize=(7, 4))
# plt.title('Price Comparison')
# plt.show()

# # # # # ------------- Reviews ------------- # # # #
# # # Box plot total reviews
# df_total_reviews = pd.concat(
#     [df['API_Review_Number'], df1['API_Review_Number']], axis=1)
# df_total_reviews.columns = ['EA', 'Beta']
# df_total_reviews.plot.box(figsize=(7, 4))
# plt.title('Total Reviews Comparison')
# plt.show()

# # # Box plot positive/negative reviews EA vs Beta
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
# df_review_sentiment_ea = pd.concat(
#     [df['API_Positive_Reviews'], df['API_Negative_Reviews']], axis=1)
# df_review_sentiment_ea.columns = [
#     'Positive_Reviews', 'Negative_Reviews']
# Q1_ea = df_review_sentiment_ea.quantile(0.25)
# Q3_ea = df_review_sentiment_ea.quantile(0.75)
# IQR_ea = Q3_ea - Q1_ea
# mask_ea = (df_review_sentiment_ea >= (Q1_ea - 1.5 * IQR_ea)
#            ) & (df_review_sentiment_ea <= (Q3_ea + 1.5 * IQR_ea))
# df_review_sentiment_ea = df_review_sentiment_ea[mask_ea]
# # df_review_sentiment_ea.plot.box(figsize=(7, 4))
# # plt.title('Reviews EA')
# # plt.show()

# df_review_sentiment_beta = pd.concat(
#     [df1['API_Positive_Reviews'], df1['API_Negative_Reviews']], axis=1)
# df_review_sentiment_beta.columns = [
#     'Positive_Reviews', 'Negative_Reviews']
# Q1_beta = df_review_sentiment_beta.quantile(0.25)
# Q3_beta = df_review_sentiment_beta.quantile(0.75)
# IQR_beta = Q3_beta - Q1_beta
# mask_beta = (df_review_sentiment_beta >= (Q1_beta - 1.5 * IQR_beta)
#              ) & (df_review_sentiment_beta <= (Q3_beta + 1.5 * IQR_beta))
# df_review_sentiment_beta = df_review_sentiment_beta[mask_beta]
# # df_review_sentiment_beta.plot.box(figsize=(7, 4))
# # plt.title('Reviews Beta')
# # plt.show()

# # # Multiplot for the same
# df_review_sentiment_ea.plot.box(ax=axes[0])
# axes[0].set_title('Reviews EA')
# df_review_sentiment_beta.plot.box(ax=axes[1])
# axes[1].set_title('Reviews Beta')
# plt.tight_layout()
# plt.show()


# # # # ------------- Review Score ------------- # # # #
# # # Box plot
# null_counts_ea = df['Review_Summary_Score'].isnull().sum()
# null_counts_beta = df1['Review_Summary_Score'].isnull().sum()
# df_review_score = pd.concat(
#     [df['Review_Summary_Score'], df1['Review_Summary_Score']], axis=1)
# df_review_score.columns = [
#     f'EA ({null_counts_ea} null)', f'Beta ({null_counts_beta} null)']
# df_review_score.plot.box(figsize=(7, 4))
# plt.title('Review Score')
# plt.show()


# # # # # ------------- Realease Date ------------- # # # #
# df['Release_Date'] = pd.to_datetime(df['Release_Date'])
# df1['Release_Date'] = pd.to_datetime(df1['Release_Date'])
# fig, ax = plt.subplots(figsize=(7, 4))

# # # Histogram
# df['Release_Date'].hist(ax=ax, bins=30, alpha=0.5, label='Early Access')
# df1['Release_Date'].hist(ax=ax, bins=30, alpha=0.5, label='Beta')

# ax.set_title('Histogram of Release Dates')
# ax.set_xlabel('Release Date')
# ax.set_ylabel('Frequency')
# ax.legend()
# plt.show()
# # # Line chart
# fig, ax = plt.subplots(figsize=(7, 4))
# df_yearly = df['Release_Date'].groupby(df['Release_Date'].dt.year).count()
# df1_yearly = df1['Release_Date'].groupby(df1['Release_Date'].dt.year).count()
# df_yearly.plot(ax=ax, label='Early Access')
# df1_yearly.plot(ax=ax, label='Beta')

# # # Set the title and labels
# ax.set_title('Line chart of Release Dates')
# ax.set_xlabel('Release Date')
# ax.set_ylabel('Frequency')
# ax.legend()
# plt.show()

# -trend shows that the number of Beta games decline in last years while EA games are increasing especially last 2 years


# # # # ------------- Categories ------------- # # # #
# # Setup Exploded DFs
df_exploded = df.explode('Categories')
df1_exploded = df1.explode('Categories')
selected_categories = df1_exploded['Categories'].unique().tolist()
df_exploded = df_exploded[df_exploded['Categories'].isin(selected_categories)]

# # # # Count barchart
# ea_category_counts = df_exploded['Categories'].value_counts()
# beta_category_counts = df1_exploded['Categories'].value_counts()
# category_counts = pd.DataFrame(
#     {'Early Access': ea_category_counts, 'Beta': beta_category_counts}).sort_values(by=['Beta', 'Early Access'])
# category_counts.plot(kind='barh', figsize=(7, 4))
# plt.title('Category Counts for Early Access and Beta Games')
# plt.xlabel('Number of Games')
# plt.ylabel('Category')
# plt.show()

# -shows that EA games have similar but not quite identic target genres. more focus on multiplayer and indie games should be placed


# # Total Reviews barchart -- a bit useless
# ea_category_reviews = df_exploded.groupby(
#     'Categories')['API_Review_Number'].mean()
# beta_category_reviews = df1_exploded.groupby(
#     'Categories')['API_Review_Number'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_reviews, 'Beta': beta_category_reviews}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(10, 6))
# plt.title('Total Reviews per Category')
# plt.xlabel('Total Reviews')
# plt.ylabel('Category')
# plt.show()


# # Price barchart
# ea_category_price = df_exploded.groupby(
#     'Categories')['Current_Price'].mean()
# beta_category_price = df1_exploded.groupby(
#     'Categories')['Current_Price'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_price, 'Beta': beta_category_price}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(7, 4))
# plt.title('Average Price per Category')
# plt.xlabel('Price')
# plt.ylabel('Category')
# plt.show()

# # Review Score barchart
# ea_category_review_scores = df_exploded.groupby(
#     'Categories')['Review_Summary_Score'].mean()
# beta_category_review_scores = df1_exploded.groupby(
#     'Categories')['Review_Summary_Score'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_review_scores, 'Beta': beta_category_review_scores}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(7, 4))
# plt.title('Average Review Score per Category')
# plt.xlabel('Review Score')
# plt.xticks(list(positive_review_scores.keys()),
#            list(positive_review_scores.values()), rotation=15)
# plt.ylabel('Category')
# plt.show()

# - EA games show differences in review score between the different genre with RPG and Simulation being better than the rest
# - Beta games are well perceived throught all of the top genre

# # Review Score crosstab EA
# ea_cross_counts = pd.crosstab(
#     df_exploded['Categories'], df_exploded['Review_Summary'])
# ea_cross_counts['Total'] = ea_cross_counts.sum(axis=1)
# ea_cross_counts = ea_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# ea_cross_counts.plot(kind='barh', stacked=True, figsize=(7, 4))
# plt.title(
#     'Cross tabulation for Review Scores per Category for Early Access Games')
# plt.xlabel('Total Games')
# plt.ylabel('Category')
# plt.show()

# # Review Score crosstab Beta
# beta_cross_counts = pd.crosstab(
#     df1_exploded['Categories'], df1_exploded['Review_Summary'])
# beta_cross_counts['Total'] = beta_cross_counts.sum(axis=1)
# beta_cross_counts = beta_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# beta_cross_counts.plot(kind='barh', stacked=True, figsize=(7, 4))
# plt.title(
#     'Cross tabulation for Review Scores per Category for Beta Games')
# plt.xlabel('Total Games')
# plt.ylabel('Category')
# plt.show()

# - majority of EA have not enough reviews to be even ranked and the rest are quite dispersed
# - Beta games are primarily well perceived and are also well above the minimum treshold

# endregion

# region ANALISYS
# # # # # # # # # # # # # # # # # # # # # # ANALISYS # # # # # # # # # # # # # # # # # # # # # #

# # MANOVA
new_df = pd.concat([df, df1])
new_df['Game_Type'] = new_df['Game_Type'].astype('category')
manova = MANOVA.from_formula(
    'Current_Price + Discount + API_Review_Number + Review_Summary_Score + Release_Date_Epoch ~ Game_Type', data=new_df).mv_test()
print(manova)

# all p-values < 0.005 therefore there is significant difference between the groups
# Wilks' lambda: Tests the null hypothesis that the group means are equal. A smaller value indicates more evidence against the null hypothesis.
# Pillai's trace: A more robust test that is less sensitive to deviations from multivariate normality.
# Hotelling-Lawley trace: Another test for the multivariate effect.
# Roy's greatest root: Focuses on the largest eigenvalue of the test matrix and is particularly sensitive to the largest effect.

# # One-Way ANOVAs
f_val, p_val = stats.f_oneway(df.dropna(subset=['Review_Summary_Score'])[
                              'Review_Summary_Score'], df1.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score'])
print(f"Review Score:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

f_val, p_val = stats.f_oneway(df['Current_Price'], df1['Current_Price'])
print(f"Price:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

f_val, p_val = stats.f_oneway(
    df['API_Review_Number'], df1['API_Review_Number'])
print(f"Total Reviews:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

f_val, p_val = stats.f_oneway(
    df['Release_Date_Epoch'], df1['Release_Date_Epoch'])
print(f"Release Date:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

f_val, p_val = stats.f_oneway(df['Discount'], df1['Discount'])
print(f"Discount:")
print(f"F-value: {f_val}  |||  P-value: {p_val}")

# F-value = ratio of variance btw groups to variance within groups (higher = more difference)
# p-value < 0.05 => there is significant difference in Review Score, Price, and Total Reviews between EA and Beta games
# no significant difference was found for the Discount


# # T-tests
t_stat, p_value = stats.ttest_ind(
    df.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score'], df1.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score'])
print(f"Review Score:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

t_stat, p_value = stats.ttest_ind(
    df['Current_Price'], df1['Current_Price'])
print(f"Price:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

t_stat, p_value = stats.ttest_ind(
    df['API_Review_Number'], df1['API_Review_Number'])
print(f"Total Reviews:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

t_stat, p_value = stats.ttest_ind(
    df['Release_Date_Epoch'], df1['Release_Date_Epoch'])
print(f"Release Date:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

t_stat, p_value = stats.ttest_ind(
    df['Discount'], df1['Discount'])
print(f"Discount:")
print(f"T-statistic: {t_stat}  |||  P-value: {p_value}")

# t-stat = size of difference relative to variation in data (higher = more difference)
# p-value < 0.05 => there is significant difference in Review Score, Price, and Total Reviews between EA and Beta games
# no significant difference was found for the Discount

# # Correlation Matrix EA/Beta
variables = ['Game_Type_Numeric', 'Current_Price', 'API_Review_Number',
             'Review_Summary_Score', 'Release_Date_Epoch', 'Discount']
df_subset = new_df[variables]
correlation_matrix = df_subset.corr()
print(correlation_matrix)
fig, ax = plt.subplots(figsize=(7, 4))
cax = ax.matshow(correlation_matrix, cmap='binary')
fig.colorbar(cax)

ax.set_xticks(np.arange(len(correlation_matrix.columns)))
ax.set_yticks(np.arange(len(correlation_matrix.index)))

# Labeling the ticks with the variable names
ax.set_xticklabels(correlation_matrix.columns, rotation=25, ha="left")
ax.set_yticklabels(correlation_matrix.index)

plt.title('Correlation Matrix Heatmap')
plt.show()
# we observe stronger positive colleration in Game Type and Review Score also (Price and Review Number) and negative cor. with Release Date
# in between the other DVs we see positive correlation between Price and Review Number/Score lets continue with Regression

# # Regression
X = sm.add_constant(new_df['Game_Type_Numeric'])

dependent_vars = ['Current_Price', 'API_Review_Number',
                  'Review_Summary_Score', 'Release_Date_Epoch', 'Discount']

Y = new_df.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score']
model = sm.OLS(Y, sm.add_constant(
    new_df.dropna(subset=['Review_Summary_Score'])['Game_Type_Numeric'])).fit()
print(f"Review Score:")
print(model.summary())

Y = new_df['Current_Price']
model = sm.OLS(Y, X).fit()
print(f"Price:")
print(model.summary())

Y = new_df['API_Review_Number']
model = sm.OLS(Y, X).fit()
print(f"Total Reviews:")
print(model.summary())

Y = new_df['Release_Date_Epoch']
model = sm.OLS(Y, X).fit()
print(f"Release Date:")
print(model.summary())

Y = new_df['Discount']
model = sm.OLS(Y, X).fit()
print(f"Discount:")
print(model.summary())

# Interaction events:
# Review Score - 2.2        p<0.05
# Price - 12.9              p<0.05
# Total Reviews - 84,130    p<0.05
# Release Date - -788       p<0.05
# Discount - 0.05           p>0.05

# # Multiple Linear Regression
independent_vars = ['Current_Price', 'API_Review_Number',
                    'Release_Date_Epoch', 'Discount']
dependent_var = 'Review_Summary_Score'

X = sm.add_constant(new_df.dropna(subset=['Review_Summary_Score'])[
                    ['API_Review_Number', 'Current_Price', 'Release_Date_Epoch', 'Discount']])
Y = new_df.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score']
model = sm.OLS(Y, X).fit()
print(f"EA + Beta:")
print(model.summary())

X = sm.add_constant(df_ea_full.dropna(subset=['Review_Summary_Score'])[
                    ['API_Review_Number', 'Release_Date_Epoch']])
Y = df_ea_full.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score']
model = sm.OLS(Y, X).fit()
print(f"EA full:")
print(model.summary())

X = sm.add_constant(df.dropna(subset=['Review_Summary_Score'])[
                    ['API_Review_Number', 'Release_Date_Epoch']])
Y = df.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score']
model = sm.OLS(Y, X).fit()
print(f"EA sample:")
print(model.summary())

X = sm.add_constant(df1.dropna(subset=['Review_Summary_Score'])[
                    ['API_Review_Number', 'Current_Price', 'Release_Date_Epoch', 'Discount']])
Y = df1.dropna(subset=['Review_Summary_Score'])['Review_Summary_Score']
model = sm.OLS(Y, X).fit()
print(f"Beta:")
print(model.summary())

# Interaction events:
# Both Sets
# Total Reviews - 0.000004  p<0.05
# Price - 0.04              p<0.05
# Release Date - -0.00003   p>0.05
# Discount - 0.75           p>0.05
# Full EA Set
# Total Reviews - 0.00002  p<0.05
# Release Date - 0.0004   p<0.05
# EA Set
# Total Reviews - 0.0028  p<0.05
# Release Date - 0.0006   p<0.05
# Beta Set - no significant effects


# endregion
