
# ID2223 - [Lab 2](https://github.com/ID2223KTH/id2223kth.github.io/tree/master/assignments/lab2). 

About lab

## Approach

- Given the quouta limitation on Google Colab, we tried to migrate the given colab notebook to Kaggle, since one can access 40 hours of GPU instead of 12. However, we encountered many dependency/environment problems. After many hours of unsuccesful debugging, we decided to go back to google colab.
- In colab, one can store 80GB of data (e.g. model checkpoints and preprocessed data). However, all this data is lost when exiting the session. Therefore we needed a solution to:
  1. Store the preprocessed data.
  2. Store model checkpoints.

- To address 1, we found that the data we used was large enough to exceed the 15GB google drive quouta. Hence, we tried to find a way to store the preprocessed data on Hopsworks. To save some time, we preprocessed only one recording using feature_extractor (which either increases or decreases the audio samples to 30s AND converting the audio files to log-Mel spectrograms). We converted the preprocessed sample to a dataframe as Hopsworkds does not accept the DatasetDict datastructure. However, the values after the dataframe conversion were stored as 2-d (input_features) and 1-d (label) arrays, not as values. This means that in order to store it on Hopsworks, we would have been required to do a tremendous preprocessing effort to convert the audio samples to the correct format that Hopsworks require. We discarded the idea of having Hopsworks as a feature store and instead we zipped the preprocessed data and stored it on drive.
- To address 2, we followed the example notebook and thought that each checkpoint was going to be pushed to the model repository that was created on Huggingface. For Training-Pipeline-1, this worked, but for the second pipeline we encountered problems. Thereby, we used Google Drive to store the checkpoints, and uploaded the model manually to Hugging Face.

## Files

- Feature-pipeline-1 and Feature-pipeline-2
  - Data preprocessing & save to drive using CPU.
- Training-pipeline-1 and Training-pipeline-2
  - Model training with whisper small, but with different training parameters.
  - We recognize that two pairs of pipelines are not necessary, but we ran it from different google accounts concurrently.

## Data

- For the first two runs, we use two different datasets. One downsampled version (first 2500 audio recordings) to  and one utilizing the entire train+validation+other datasets (roughly 18k audio recordings) as it would be interesting to see the performance difference with more data. The test dataset sizes were resized accordingly. 
- For the third run and as a POC for hyper parameter tuning, we downsampled the training and test size (this much). 

## Training parameters

- For the first run with 2500 samples, the parameters are essentially the same as given in the example notebook, but we evaluate and create checkpoints after each 500th step instead of every 1000th step. During this run and after 500 steps, we found that the checkpoints indeed were not pushed to Hugging face, only stored in Google Colab's session storage.
- For the second run with 18k samples, we decreased the amount of steps to 2000 from 4000 in an attempt to speed up the training process. We also evaluate and create checkpoints every 100th step instead of 500th step to calm our nerves in case of runtime crashes in Google Colab.
- For the third run ...

## Results

![2500-instances](https://user-images.githubusercontent.com/50402197/206474496-21791370-5119-4f9e-94f7-f63853c60ba1.PNG)

## Discussion

### Data-centric

- We proved that adding more data decreases the WER score (32 vs 21), already after 300 steps of training. However, there was a high increase of training time. 

### Model-centric

- We added a minor hyperparameter tuning as a POC to demonstrate our understanding of how hyperparameter tuning and that tuning the parameters increases the performance. We note that the hyperparameter setting for a model trained on a larger dataset most probably will look different since it most likely has found different patterns (hence using different hyperparameters after tuning) compared to our POC. Besides finetuning whisper-small, no other whisper model was finetuned in this project. The finetuning process can be described as the larger model to finetune, the longer training time but the better results. 

## Gardio UI

## Links
* [Gardio UI of model 1 (2500 training instances, ~27 WER)](https://huggingface.co/spaces/Akseluhr/whisper-se-auhr)
