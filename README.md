# Cloud Build Slack Notifier

a cloud build function on gcp to send slack notifications 


## Usage

#### Create the cloud-builds Pub/Sub topic:
```
gcloud pubsub topics create cloud-builds
``` 

#### Create the cloud function:
  
```
gcloud functions deploy Cloud-Build-Slack-Notifier --entry-point cloudFunctionTrigger --runtime python37 --trigger-topic cloud-builds --project <my-project> --set-env-vars slackToken=<slack-token>,slackChannel=<slack-channel-name>
```
#### Message example:
![Screenshot](https://github.com/shaw8i/cloudBuildSlackNotifier/blob/main/example/message-example.png)
