import hopsworks
import pandas as pd
import numpy as np

project = hopsworks.login()
fs = project.get_feature_store()

titanic_df = pd.read_csv("https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1"
                         "/titanic.csv")

# Drop less important columns
titanic_df.drop(['Name', 'Ticket', 'SibSp', 'Parch', 'Cabin', 'Embarked'], axis=1, inplace=True)

# Handle missing values (age)
titanic_df['Age'].fillna((titanic_df['Age'].mean()), inplace=True)
bins = [-np.infty, 20, 25, 29, 30, 40, np.infty]
titanic_df['Age'] = pd.cut(x=titanic_df['Age'], bins=bins, labels=False)

# Map to numeric values (gender)
categories = {"female": 1, "male": 0}
titanic_df['Sex'] = titanic_df['Sex'].replace(categories)

titanic_df['Fare'] = titanic_df['Fare'].fillna(-1)

titanic_fg = fs.get_or_create_feature_group(
    name="titanic_modal",
    version=1,
    primary_key=["PassengerId"],
    description="Titanic dataset")
titanic_fg.insert(titanic_df, write_options={"wait_for_job": False})
