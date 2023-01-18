import os

import hopsworks
import pandas as pd
import math

import seaborn as sns
from hsml.schema import Schema
from hsml.model_schema import ModelSchema

# Creating time series features
def create_features(df, label=None):
    df = df.copy()
    df['Dayofyear'] = df.index.dayofyear
    df['Month'] = df.index.month
    df['Year'] = df.index.year
    
    return df

project = hopsworks.login()
fs = project.get_feature_store()

try:
    feature_view = fs.get_feature_view(name="btc_modal_2", version=1)
    feature_df, labels = feature_view.get_training_data(training_dataset_version=1)
except:
    btc_fg = fs.get_feature_group(name="btc_modal_2", version=1)
    query = btc_fg.select_all()
    feature_view = fs.create_feature_view(name="btc_modal_2",
                                          version=1,
                                          description="Read from brc dataset",
                                          labels=["close"],
                                          query=query)
    version, job = feature_view.create_training_data(
        description = 'btc new training',
        data_format = 'csv',
        write_options = {"wait_for_job": False}
    )
    feature_df, label = feature_view.get_training_data(training_dataset_version=1)

print(feature_df)
print(labels)
feature_df = feature_df.sort_values(by=["date"], ascending=[True]).reset_index(drop=True)

print(feature_df)


train_size = math.floor(len(feature_df)*0.85) # 85% training data
test_size = math.floor(len(feature_df)*0.15) 

print(train_size)
print(test_size)
#train = feature_df.iloc[0:ceil(len(feature_df)*0.9)]
#test = feature_df.iloc[2250:len(data)]

start_time_train = '2016-01-01 00:00:00'
end_time_train = '2021-12-31 00:00:00'

start_time_test = '2022-01-01 00:00:00'
end_time_test = '2023-01-18 00:00:00'
# you can also pass dates as datetime objects

# get training data
td_version, td_job = feature_view.create_train_test_split(
    train_start=start_time_train,
    train_end=end_time_train,
    test_start=start_time_test,
    test_end=end_time_test,
    data_format= 'csv',
    write_options = {"wait_for_job": True}
)
 
X_train, X_test, y_train, y_test = feature_view.get_train_test_split(td_version)

X_train.head(5)
X_test.head()
y_train.head()
y_test.head()

#model = RandomForestClassifier(bootstrap=True, max_depth=None, max_features='auto', min_samples_leaf=1, min_samples_split=10, n_estimators=20)
#model.fit(X_train, y_train.values.ravel())

# Evaluate model performance using the features from the test set (X_test)
#y_pred = model.predict(X_test)


'''
# Compare predictions (y_pred) with the labels in the test set (y_test)
metrics = classification_report(y_test, y_pred, output_dict=True)
results = confusion_matrix(y_test, y_pred)

# Create the confusion matrix as a figure, we will later store it as a PNG image file
df_cm = pd.DataFrame(results, ['True Survived', 'True Died'],
                     ['Pred Survived', 'Pred Died'])
cm = sns.heatmap(df_cm, annot=True)
fig = cm.get_figure()

# We will now upload our model to the Hopsworks Model Registry. First get an object for the model registry.
mr = project.get_model_registry()

# The contents of the 'iris_model' directory will be saved to the model registry. Create the dir, first.
model_dir = "titanic_model"
if not os.path.isdir(model_dir):
    os.mkdir(model_dir)

# Save both our model and the confusion matrix to 'model_dir', whose contents will be uploaded to the model registry
joblib.dump(model, model_dir + "/titanic_model.pkl")
fig.savefig(model_dir + "/confusion_matrix.png")

# Specify the schema of the model's input/output using the features (X_train) and labels (y_train)
input_schema = Schema(X_train)
output_schema = Schema(y_train)
model_schema = ModelSchema(input_schema, output_schema)

# Create an entry in the model registry that includes the model's name, desc, metrics
titanic_model = mr.python.create_model(
    name="titanic_modal",
    metrics={"accuracy": metrics['accuracy']},
    model_schema=model_schema,
    description="Titanic Survival Predictor"
)

# Upload the model to the model registry, including all files in 'model_dir'
titanic_model.save(model_dir)


if __name__ == "__main__":
    if LOCAL == True:
        g()
    else:
        with stub.run():
            f()
            
'''