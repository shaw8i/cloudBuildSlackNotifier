# Cloud Build Slack Notifier

a cloud build function on gcp to send slack alerts 


## Usage

#### Create the cloud-builds Pub/Sub topic:
```
gcloud pubsub topics create cloud-builds
``` 

#### Create the cloud function:
  
```
gcloud functions deploy Cloud-Build-Slack-Notifier --runtime python37 --trigger-topic cloud-builds --project <my-project> --set-env-vars slackToken=<slack-token>,slackChannel=<slack-channel-name>
```
