import pandas as pd

# 95 - 100 | 500+ reviews | positive | overwhelmingly
# 85 - 100 |  50+ reviews | positive | very
# 80 - 100 |  10+ reviews | positive | -
# 70 -  79 |  10+ reviews | positive | mostly
# 40 -  69 |  10+ reviews | mixed    | -
# 20 -  39 |  10+ reviews | negative | mostly
#  0 -  19 |  10+ reviews | negative | -
#  0 -  19 |  50+ reviews | negative | very
#  0 -  19 | 500+ reviews | negative | overwhelmingly

df = pd.read_json('filesToIgnore/allgames_combined.json')
print(df['Review Score'].unique())
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
df['Review Score Percent'] = (
    df['Positive Reviews'] / df['Total Reviews']) * 100
print(df['Review Score Percent'])
print(df.dtypes)

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

# !!! Text analysis: Sentiment Analysis, Word Frequency, Word Cloud,Word Frequency:, Topic Modeling,Emotion Analysis,Named Entity Recognition (NER),Readability Analysis,Length of Descriptions,Language Style,Comparative Analysis!!!

# region Hypothesis short
# Games
# # Review Score
# # # Hypothesis:  Number of reviews -> review score
# # # Hypothesis:  Price -> review score
# # # Hypothesis:  Discount -> review score
# # # Hypothesis:  Descriptions -> review score
# # # Hypothesis:  Release date -> review score
# # # Hypothesis:  Categories -> review score

# # Number of Reviews
# # # Hypothesis:  Price -> number of reviews
# # # Hypothesis:  Discount -> number of reviews
# # # Hypothesis:  Descriptions -> number of reviews
# # # Hypothesis:  Release date -> number of reviews
# # # Hypothesis:  Categories -> number of reviews

# # Price
# # # Hypothesis:  Review score -> price
# # # Hypothesis:  Number of reviews -> price
# # # Hypothesis:  Descriptions -> price
# # # Hypothesis:  Release date -> price
# # # Hypothesis:  Categories -> price


# Reviews
# # # Hypothesis:  Purchase/Free -> review sentiment
# # # Hypothesis:  User experience -> review sentiment
# # # Hypothesis:  Positive reviews correlate with playtime at review
# Hypothesis:  Categories -> success on release

# Cant test
# Hypothesis:  Purchase/Free -> reviewing the game
# endregion

# region Hypothesis long
# GAME DATA
# -------------------------------- DV = Review Score -------------------------------- #
# Hypothesis 1: The more reviews a game has, the higher the review score.
# IV: Number of Reviews -> DV: Review Score

# Hypothesis 2: The higher the price, the higher the review score.
# IV: Price -> DV: Review Score

# Hypothesis 3: The higher the discount, the higher the review score.
# IV: Discount -> DV: Review Score

# Hypothesis 4: The more (detailed/positive/intriguing/emotional) the description, the higher the review score.
# IV: Description (textual content) -> DV: Review Score

# Hypothesis 5: The more recent the release date, the lower the review score.
# IV: Release Date -> DV: Review Score

# Hypothesis 6: Certain categories have a higher likelihood of success.
# IV: Game Genre -> DV: Review Score

# -------------------------------- DV = Number of Reviews -------------------------------- #
# Hypothesis 1: The higher the price, the lower the number of reviews.
# IV: Price -> DV: Number of Reviews

# Hypothesis 2: The higher the discount, the higher the number of reviews.
# IV: Discount -> DV: Number of Reviews

# Hypothesis 3: The more (detailed/positive/intriguing/emotional) the description, the higher the number of reviews.
# IV: Description (textual content) -> DV: Number of Reviews

# Hypothesis 4: The more recent the release date, the lower the number of reviews.
# IV: Release Date -> DV: Number of Reviews

# Hypothesis 5: Certain categories have a higher number of reviews.
# IV: Game Genre -> DV: Number of Reviews

# -------------------------------- DV = Price -------------------------------- #
# Hypothesis 1: The higher the review score, the higher the price.
# IV: Review Score -> DV: Price

# Hypothesis 2: The more reviews a game has, the higher the price.
# IV: Number of Reviews -> DV: Price

# Hypothesis 3: The more (detailed/positive/intriguing/emotional) the description, the higher the price.
# IV: Description (textual content) -> DV: Price

# Hypothesis 4: The more recent the release date, the higher the price.
# IV: Release Date -> DV: Price

# Hypothesis 5: Certain categories have a higher price.
# IV: Game Genre -> DV: Price

# REVIEW DATA
# -------------------------------- DV = Review Sentiment -------------------------------- #
# Hypothesis 1: People who purchased the game are more likely to leave a negative review.
# IV: Purchased -> DV: Review Sentiment

# Hypothesis 2: People who received the game for free are more likely to leave a positive review.
# IV: Received for Free -> DV: Review Sentiment

# Hypothesis 3: User experience influences review sentiment.
# IV: Playtime at Review, Purchased, Received for Free -> DV: Review Sentiment
# Moderator: Time Created, Time Updated

# Hypothesis 4: Positive reviews correlate with playtime at review.
# IV: Playtime at Review -> DV: Review Sentiment
# Moderator: Language, Time Created, Time Updated
# endregion

# region Hypothesis old
# --------------------------------
# Hypothesis 1: The more reviews a game has, the higher the review score.

# IV: Number of Reviews -> DV: Review Score

# --------------------------------
# Hypothesis 2: Longer Development Periods Tend to Have Better Overall User Ratings.

# IV: Development Period -> DV: User Ratings

# --------------------------------
# Hypothesis 3: Certain Genres Have a Higher Likelihood of Success During the Early Access Phase

# IV: Game Genre -> DV: Review Score

# --------------------------------
# Hypothesis 4:  Games with a higher discount have a higher review score/ more reviews

# IV: Discount -> DV: Review Score, Number of Reviews

# --------------------------------
# Hypothesis 5:  Peple who purchased the game are more likely to leave a negative review

# IV: Purchased -> DV: Review Sentiment


# --------------------------------
# Hypothesis 6:  People who received the game for free are more likely to leave a positive review

# IV: Received for Free -> DV: Review Sentiment


# --------------------------------
# Hypothesis 7: Game Descriptions Impact Review Scores

# IV: Description (textual content) -> DV: Review Score
# Mediator: Review Score Percent (percentage of positive reviews)
# Moderator: Previous Price, Current Price, Release Date
#

# --------------------------------
# Hypothesis 8: Release Date Affects Review Scores

# IV: Release Date -> DV: Review Score
# Mediator: Review Score Percent


# REVIEW DATA
# --------------------------------
# Hypothesis 1: Positive Reviews Correlate with Playtime at Review

# IV: Playtime at Review -> DV: Positive Reviews
# Moderator: Language, Time Created, Time Updated

# --------------------------------
# Hypothesis 2: User Experience Influences Review Sentiment

# IV: Playtime at Review, Language, Purchased, Received for Free -> DV: Review Sentiment (Positive/Negative)
# Moderator: Time Created, Time Updated
# endregion
