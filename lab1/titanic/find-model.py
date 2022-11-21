import os
#import modal
#import great_expectations as ge
#import hopsworks
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

#project = hopsworks.login()
#fs = project.get_feature_store()

titanic_df = pd.read_csv("https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1/titanic.csv")
#X_train, X_test, y_train, y_test = train_test_split(titanic_df, test_size=0.2)

# Print shapes of train and test data
#print(X_train.shape, X_test.shape)
#print(y_train.shape, y_test.shape)
# Exploratory analysis

# First instances
print("-"*30)
print("Glimpse of the DF:")
print(titanic_df.head(5))

# Descriptive stats for titanic df
print("-"*30)
print("Statistical summary of titanic DF:")
print(titanic_df.describe())

# Find NaNs
# Age - 177 and Cabin - 687 and embarked - 2
# ML algos doesn't like missing values so we need to handle them
print("-"*30)
print("Finding NaN values:")
print(titanic_df.isnull().sum())

# I didn't do any proper feature engineering, instead I found an article mentioning 
# that these are the most important features for this dataset:
# Sex, Age, Fare, Pclass
# I drop the less important features and Cabin (since it has so many missing values)

# Drop less important columns
titanic_df.drop(['PassengerId', 'Name', 'Ticket', 'SibSp', 'Parch', 'Cabin', 'Embarked'], axis=1, inplace=True)
print(titanic_df.head(5))
print(titanic_df.columns) # THIS is what we will put in our feature store! Not sure if passanger ID needs to be included.

# Handle missing values (age)
titanic_df['Age'].fillna((titanic_df['Age'].mean()), inplace=True)
print(titanic_df.isnull().sum()) # it worked

# Map to numeric values (gender)
categories = {"female": 1, "male": 0}
titanic_df['Sex']= titanic_df['Sex'].map(categories)

# Check that all columns are numerical
print(titanic_df.dtypes)

# Normalize the data so that the model converges faster 
# convergence = a state when the loss is around the final value

# Dropping label. We save it later for seeing how well the model predicted
y = titanic_df['Survived']
titanic_df = titanic_df.drop('Survived', axis=1)  # Dropping label to normalize

scaler = MinMaxScaler()
scaled_train = scaler.fit_transform(titanic_df)
scaled_test = scaler.transform(titanic_df)

scaled_train = pd.DataFrame(scaled_train, columns=titanic_df.columns, index=titanic_df.index)
print(titanic_df.head(5))

# TODO: Train model, split data, make predictions, evaluate, hyperparam tuning (approx 1 h of work), write comments!