# Project - Predicting bitcoin daily closing price
**Disclaimer: This is (definately) not financial advice**

This is a ML prediction service that estimates today's closing price of bitcoin. The features used are time series data (year, month, day), volume, max value, min value and open price. Besides predicting today's closing price, the ten past predictions  are compared with the actual price. The data ranges from 2016-01-01 until today, and is fetched using yahoo finance api. 

### Links

[Monitoring Dashboard](https://huggingface.co/spaces/Akseluhr/btc_monitoring):
- Monitor model's performance over the 10 past days.

[Interactive prediction service](https://huggingface.co/spaces/Akseluhr/btc):
- Get today's closing price prediction.

## Approach
- The initial idea was to predict the next market value with real time predictions using binance bitcoin price streaming api. See feature-pipeline-streaming.py. After a series of troubles with Hopsworks online feature store, we came up with the following idea instead:
- Predicting bitcoin daily price using the sentiment score of the n most popular tweets of the corresponding day. See twitter-data.ipynb. After a series with troubles with the twitter api (limited requests and access issues), we settled with the final following idea:
- Predicting bitcoin daily closing price using yahoo finance api with time series features, trading volume, opening price, min value, max value.

## Architecture

<p align="center">
  <img width="698" alt="Skärmavbild 2023-01-18 kl  23 49 12" src="https://user-images.githubusercontent.com/50402197/213312913-22795a3d-5e32-4340-9054-595d92978aa4.png">
</p>


### Feature pipeline 

In this pipeline, the historical data is read from the yahoo finance api, and converted to a dataframe. Time series features are then derived out of the date-time index. Ultimately this data is ingested to a Hopsworks offline feature group.

### Training pipeline

In this local pipeline, the following is performed:
- Train/test/val time series split (approx 2250/300/5)
- Baseline model evaluation: xgboost
- Feature importance evaluation
- Random search for hyperparams
- Coarse search for hyperparams
- Model evaluation: xgboost
- Model training on all data: xgboost
- Model testing
- Push and save the model to Hopsworks

### Daily feature pipeline

This pipeline is similar to the feature pipeline. However, it is serverless, runs daily using Modal, and the daily tuple is ingested to the feature store at the end of the day. This data is used in the prediction service for model governance, see batch pipeline below. It may also be used for future scheduled model training (e.g. re-train model every day, or every 10th day).

### Daily batch pipeline

Similar to the daily feature pipeline, we run this on a daily basis and it is serverless. Here we monitor our model. That is, plotting the predictions of the past 10 days with each day's corresponding actual closing price. Furthermore, the root mean squared error is presented for these ten days. 
