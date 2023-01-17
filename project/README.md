# Project - Predicting Bitcoing closing price
*Intro*

### Links

- Monitoring dashboard

- Interactive prediction service

## Architecture


<p align="center">
  <img width="600" alt="project architecture" src="https://user-images.githubusercontent.com/50402197/212725120-d906a718-caf1-4227-8379-3c33a6cf0d23.png">
</p>


### Feature pipeline 

In this pipeline, the historical data is read from (file or api) and converted to a dataframe. Afterwards, an API call is fetching the most popular tweet and its date regarding bitcoin, for each day from (date) until today is. The result is an object, and another API call to IBM sentiment analysis (idk the name) is done, calculating the sentiment score for each tweet every day. A dataframe out of all sentiment scores are constructeds with the corresponding date. Then, we use the date as a join key to merge the sentiment score dataframe with the price dataframe, and push it to Hopsworks.

### Training pipeline

( If we want scheduling retrain, we use modal, otherwise we can run it locally)
Here, we perform:
- Model specific transformation functions allowing us to reuse the feature pipeline
- Algorithm selection, evaluating with cross validation
- Random search
- Coarse search 
- Model evaluation
- Model testing 
- Push model to github

### Daily feature pipeline

This pipeline is similar to the feature pipeline. However, it is serverless, run daily and the resulting { closing price, date, sentiment scores } tuple is ingested to the feature store at the end of the day. This data is used in the prediction service for model governance, see batch pipeline below. It is also used for future model training (e.g. re-train model every day, or every 10th day)

### Daily batch pipeline

Similar to daily feature pipeline, we run this on a daily basis and it is serverless. 
Here we monitor our model - showing predictions, error rate and actual values


