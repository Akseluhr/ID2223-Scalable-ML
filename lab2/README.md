
# ID2223 - [Lab 2](https://github.com/ID2223KTH/id2223kth.github.io/tree/master/assignments/lab2). 

About lab

## Approach

- Given the quouta limitation on Google Colab, we tried to migrate the given colab notebook to Kaggle, since one can access 40 hours of GPU instead of 12. However, we encountered many dependency/environment problems. After many hours of unsuccesful debugging, we decided to go back to google colab.
- In colab, one can store 80GB of data (e.g. model checkpoints and preprocessed data). However, all this data is lost when exiting the session. Therefore we needed a solution to:
  1. Store the preprocessed data.
  2. Store model checkpoints.

- To address 1, we found that the data we used was large enough to exceed the 15GB google drive quouta. Hence, we tried to find a way to store the preprocessed data on Hopsworks. To save some time, we preprocessed only one recording using feature_extractor (which either increases or decreases the audio samples to 30s AND converting the audio files to log-Mel spectrograms). We converted the preprocessed sample to a dataframe as Hopsworkds does not accept the DatasetDict datastructure. However, the values after the dataframe conversion were stored as 2-d (input_features) and 1-d (label) arrays, not as values. This means that in order to store it on Hopsworks, we would have been required to do a tremendous preprocessing effort to convert the audio samples to the correct format that Hopsworks require. We discarded the idea of having Hopsworks as a feature store and instead we zipped the preprocessed data and stored it on drive.
 
