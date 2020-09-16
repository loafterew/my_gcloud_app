# My Google Cloud App

Hello, this is my Google Cloud App!

I made this app using the [Hosting Projects tutorial](https://colab.research.google.com/drive/1UsbTlPc5oB8sIwHRfmajOGf9z7E0CobT?usp=sharing) from Div's Data Science Course!

## Instructions: Initialization

Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) if you don't already have it:

`brew cask install google-cloud-sdk`

Clone the repository locally:

`git clone https://github.com/loafterew/my_gcloud_app.git`

Go into repository:

`cd my_gcloud_app`

Define these variables:

```
PROJECT_NAME='ds-web-app'
BUCKET_NAME='ds-app-bucket'
CLOUDFUNCTION_NAME='image_classifier'
ENTRY_POINT='classify_image'
```

### Create Project

Log into Google Cloud Platform:

`gcloud auth login`

Initialize the project if it doesn't exist:

`gcloud projects create $PROJECT_NAME`

Set the project name:

`gcloud config set project $PROJECT_NAME`

Create the project if it doesn't exist:

`gcloud app create`

If you haven't already, you will have to [enable billing](https://console.cloud.google.com/billing) and enter payment information.

Enable the Cloud Build API:

`gcloud services enable cloudbuild.googleapis.com`

### Create Storage Bucket

Create the bucket if it doesn't exist:

`gsutil mb gs://$BUCKET_NAME`

Make the bucket's contents public:

`gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME`

### Create Cloud Function

Go into the my_cloudfunction directory:

`cd my_cloudfunction/`

Deploy Cloud Function if it doesn't exist:

```
gcloud functions deploy $CLOUDFUNCTION_NAME \
--region us-west2 \
--entry-point $ENTRY_POINT \
--memory 2048 \
--trigger-http \
--runtime python38
```
Go back to parent directory:

`cd ..`

## Instructions: Test Web App Locally

Create and activate a python virtual environment:

```
python3 -m venv env
source env/bin/activate
```

go into my_app_v3 directory:

`cd my_app_v3`

Create a new IAM account if it doesn't exist:

```
gcloud iam service-accounts create dev-account
gcloud projects add-iam-policy-binding $PROJECT_NAME --member "serviceAccount:dev-account@$PROJECT_NAME.iam.gserviceaccount.com" --role "roles/owner"
```

Create key for local web app to access Google Storage:

`gcloud iam service-accounts keys create key.json --iam-account dev-account@$PROJECT_NAME.iam.gserviceaccount.com`

Export `GOOGLE_APPLICATION_CREDENTIALS` variable:

`export GOOGLE_APPLICATION_CREDENTIALS=key.json`

Install dependencies and run app:

```
pip install -r requirements.txt
python main.py
```

## Instructions: Deploy Web App Google Cloud

go into my_app_v3 directory:

`cd my_app_v3`

Deploy the app:

`gcloud app deploy`