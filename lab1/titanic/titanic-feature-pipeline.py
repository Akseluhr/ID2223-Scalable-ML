import hopsworks
import pandas as pd

project = hopsworks.login()
fs = project.get_feature_store()

titanic_df = pd.read_csv("https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1"
                         "/titanic.csv")

# Drop less important columns
titanic_df.drop(['Name', 'Ticket', 'SibSp', 'Parch', 'Cabin', 'Embarked'], axis=1, inplace=True)

# Handle missing values (age)
titanic_df['Age'].fillna((titanic_df['Age'].mean()), inplace=True)

# Map to numeric values (gender)
categories = {"female": 1, "male": 0}
titanic_df['Sex'] = titanic_df['Sex'].map(categories)

titanic_fg = fs.get_or_create_feature_group(
    name="titanic_modal",
    version=1,
    primary_key=["PassengerId", "Pclass", "Sex", "Age", "Fare"],
    description="Titanic dataset")
titanic_fg.insert(titanic_df, write_options={"wait_for_job": False})

# expectation_suite = ge.core.ExpectationSuite(expectation_suite_name="iris_dimensions")
# value_between(expectation_suite, "sepal_length", 4.5, 8.0)
# value_between(expectation_suite, "sepal_width", 2.1, 4.5)
# value_between(expectation_suite, "petal_length", 1.2, 7)
# value_between(expectation_suite, "petal_width", 0.2, 2.5)
# iris_fg.save_expectation_suite(expectation_suite=expectation_suite, validation_ingestion_policy="STRICT")
