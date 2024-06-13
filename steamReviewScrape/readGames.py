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
df = pd.read_json('gamesEAsample2.json', lines=True)
df1 = pd.read_json('gamesBeta.json', lines=True)

df['Release Date'] = pd.to_datetime(df['Release Date'])
df1['Release Date'] = pd.to_datetime(df1['Release Date'])
df['Release Date Epoch'] = (df['Release Date'] -
                            pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')
df1['Release Date Epoch'] = (df1['Release Date'] -
                             pd.Timestamp('1970-01-01')) / pd.Timedelta('1D')

# # # # ------------- Summarizing the data ------------- # # # #
# dfSummary = df.describe().drop('ID', axis=1)
# df1Summary = df1.describe().drop('ID', axis=1)
# print(df.columns)
# print(df1Summary)
# # Conclusions
# # EA games are :
# # -cheaper (avg $8-$10) vs (avg $20)
# # -have lower score (avg 1-1.5) vs (avg 3.4)
# # -have less reviews (avg 50-2000) vs (avg 84,000)
# # -ratio positive/negative reviews is worse in most cases (outlier in sample 2)
# # -Still we have to test with ANOVA if differences are significant
# all_categories_ea = df['Categories'].explode()
# top_10_categoriess_ea = all_categories_ea.value_counts().head(10)
# print(top_10_categoriess_ea)
# all_categories_beta = df1['Categories'].explode()
# top_10_categoriess_beta = all_categories_beta.value_counts().head(10)
# print(top_10_categoriess_beta)
# # -250 different categories
# # -top 10 EA -> Early Access, Singleplayer, Action, Indie, 2D, Adventure, Simulation, Casual, Strategy, 3D
# # -top 10 Beta -> Indie, Action, Simulation, Adventure, Strategy, RPG, Casual, Massively Multiplayer, Free to Play, Sports
# # -maybe EA should focus more on Indie and Multiplayer games rather than Singleplayer


# region PLOTS
# # # # # # # # # # # # # # # # # # # # # # PLOTS # # # # # # # # # # # # # # # # # # # # # #
# # # # ------------- Price ------------- # # # #
# # Box plot
# df_prices = pd.concat([df['Current Price'], df1['Current Price']], axis=1)
# df_prices.columns = ['EA', 'Beta']
# df_prices.plot.box(figsize=(7, 5))
# plt.title('Price Comparison')
# plt.show()


# # # # ------------- Reviews ------------- # # # #
# # Box plot total reviews
# df_total_reviews = pd.concat(
#     [df['API Review Number'], df1['API Review Number']], axis=1)
# df_total_reviews.columns = ['EA', 'Beta']
# df_total_reviews.plot.box(figsize=(7, 5))
# plt.title('Total Reviews Comparison')
# plt.show()

# # Box plot positive/negative reviews EA vs Beta
# fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
# df_review_sentiment_ea = pd.concat(
#     [df['API Positive Reviews'], df['API Negative Reviews']], axis=1)
# df_review_sentiment_ea.columns = [
#     'Positive Reviews', 'Negative Reviews']
# Q1_ea = df_review_sentiment_ea.quantile(0.25)
# Q3_ea = df_review_sentiment_ea.quantile(0.75)
# IQR_ea = Q3_ea - Q1_ea
# mask_ea = (df_review_sentiment_ea >= (Q1_ea - 1.5 * IQR_ea)
#            ) & (df_review_sentiment_ea <= (Q3_ea + 1.5 * IQR_ea))
# df_review_sentiment_ea = df_review_sentiment_ea[mask_ea]
# # df_review_sentiment_ea.plot.box(figsize=(7, 5))
# # plt.title('Reviews EA')
# # plt.show()

# df_review_sentiment_beta = pd.concat(
#     [df1['API Positive Reviews'], df1['API Negative Reviews']], axis=1)
# df_review_sentiment_beta.columns = [
#     'Positive Reviews', 'Negative Reviews']
# Q1_beta = df_review_sentiment_beta.quantile(0.25)
# Q3_beta = df_review_sentiment_beta.quantile(0.75)
# IQR_beta = Q3_beta - Q1_beta
# mask_beta = (df_review_sentiment_beta >= (Q1_beta - 1.5 * IQR_beta)
#              ) & (df_review_sentiment_beta <= (Q3_beta + 1.5 * IQR_beta))
# df_review_sentiment_beta = df_review_sentiment_beta[mask_beta]
# # df_review_sentiment_beta.plot.box(figsize=(7, 5))
# # plt.title('Reviews Beta')
# # plt.show()

# # Multiplot
# df_review_sentiment_ea.plot.box(ax=axes[0])
# axes[0].set_title('Reviews EA')
# df_review_sentiment_beta.plot.box(ax=axes[1])
# axes[1].set_title('Reviews Beta')
# plt.tight_layout()
# plt.show()


# # # # ------------- Review Score ------------- # # # #
# # Box plot
# null_counts_ea = df['Review Summary Score'].isnull().sum()
# null_counts_beta = df1['Review Summary Score'].isnull().sum()
# df_review_score = pd.concat(
#     [df['Review Summary Score'], df1['Review Summary Score']], axis=1)
# df_review_score.columns = [
#     f'EA ({null_counts_ea} null)', f'Beta ({null_counts_beta} null)']
# df_review_score.plot.box(figsize=(7, 5))
# plt.title('Review Score')
# plt.show()


# # # # ------------- Realease Date ------------- # # # #
# df['Release Date'] = pd.to_datetime(df['Release Date'])
# df1['Release Date'] = pd.to_datetime(df1['Release Date'])
# fig, ax = plt.subplots(figsize=(10, 6))

# # Histogram
# # df['Release Date'].hist(ax=ax, bins=30, alpha=0.5, label='Early Access')
# # df1['Release Date'].hist(ax=ax, bins=30, alpha=0.5, label='Beta')

# # Line chart
# df_yearly = df['Release Date'].groupby(df['Release Date'].dt.year).count()
# df1_yearly = df1['Release Date'].groupby(df1['Release Date'].dt.year).count()
# df_yearly.plot(ax=ax, label='Early Access')
# df1_yearly.plot(ax=ax, label='Beta')

# # Set the title and labels
# ax.set_title('Histogram of Release Dates')
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

# # # Count barchart
# ea_category_counts = df_exploded['Categories'].value_counts()
# beta_category_counts = df1_exploded['Categories'].value_counts()
# category_counts = pd.DataFrame(
#     {'Early Access': ea_category_counts, 'Beta': beta_category_counts}).sort_values(by=['Beta', 'Early Access'])
# category_counts.plot(kind='barh', figsize=(10, 6))
# plt.title('Category Counts for Early Access and Beta Games')
# plt.xlabel('Number of Games')
# plt.ylabel('Category')
# plt.show()

# -shows that EA games have similar but not quite identic target genres. more focus on multiplayer and indie games should be placed


# # Total Reviews barchart -- a bit useless
# ea_category_reviews = df_exploded.groupby(
#     'Categories')['API Review Number'].mean()
# beta_category_reviews = df1_exploded.groupby(
#     'Categories')['API Review Number'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_reviews, 'Beta': beta_category_reviews}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(10, 6))
# plt.title('Total Reviews per Category')
# plt.xlabel('Total Reviews')
# plt.ylabel('Category')
# plt.show()


# # Price barchart
# ea_category_price = df_exploded.groupby(
#     'Categories')['Current Price'].mean()
# beta_category_price = df1_exploded.groupby(
#     'Categories')['Current Price'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_price, 'Beta': beta_category_price}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(10, 6))
# plt.title('Average Price per Category')
# plt.xlabel('Price')
# plt.ylabel('Category')
# plt.show()

# # Review Score barchart
# ea_category_review_scores = df_exploded.groupby(
#     'Categories')['Review Summary Score'].mean()
# beta_category_review_scores = df1_exploded.groupby(
#     'Categories')['Review Summary Score'].mean()
# category_data = pd.DataFrame(
#     {'Early Access': ea_category_review_scores, 'Beta': beta_category_review_scores}).sort_values(by=['Beta', 'Early Access'])
# category_data.plot(kind='barh', figsize=(10, 6))
# plt.title('Average Review Score per Category')
# plt.xlabel('Review Score')
# plt.xticks(list(positive_review_scores.keys()),
#            list(positive_review_scores.values()))
# plt.ylabel('Category')
# plt.show()

# - EA games show differences in review score between the different genre with RPG and Simulation being better than the rest
# - Beta games are well perceived throught all of the top genre

# # Review Score crosstab EA
# ea_cross_counts = pd.crosstab(
#     df_exploded['Categories'], df_exploded['Review Summary'])
# ea_cross_counts['Total'] = ea_cross_counts.sum(axis=1)
# ea_cross_counts = ea_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# ea_cross_counts.plot(kind='barh', stacked=True)
# plt.title(
#     'Cross tabulation for Review Scores per Category for Early Access Games')
# plt.xlabel('Total Games')
# plt.ylabel('Category')
# plt.show()

# # Review Score crosstab Beta
# beta_cross_counts = pd.crosstab(
#     df1_exploded['Categories'], df1_exploded['Review Summary'])
# beta_cross_counts['Total'] = beta_cross_counts.sum(axis=1)
# beta_cross_counts = beta_cross_counts.sort_values(
#     by='Total', ascending=False).drop(columns='Total')
# beta_cross_counts.plot(kind='barh', stacked=True)
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
df['Game Type'] = 'EA'
df1['Game Type'] = 'Beta'
df.columns = [col.replace(' ', '_') for col in df.columns]
df1.columns = [col.replace(' ', '_') for col in df1.columns]
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

# # Regression
new_df['Game_Type_Numeric'] = new_df['Game_Type'].map({'EA': 0, 'Beta': 1})
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
# endregion
