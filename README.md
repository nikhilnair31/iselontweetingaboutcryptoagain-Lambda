# muskTweetPusher-Lambda
* Keys folder has autheticationn json stuff for Firestore service account
* `firepush.py` accepts json.dump as event then
    * Deletes all documents in collection
    * Pushes all data recieved to Firestore collection
    * returns event values with 200 status

## Run the following to Deploy
* `docker build -t <container_name> .`
* `docker run -d -p 8080:8080 <container_name>`
* `aws ecr create-repository --repository-name <repository_name>`
* `docker tag <repository_name>:<container_tag> 832214191436.dkr.ecr.ap-south-1.amazonaws.com/lambda-docker-fire:<container_tag>`
* `aws ecr get-login-password | docker login --username AWS --password-stdin 832214191436.dkr.ecr.ap-south-1.amazonaws.com`
* `docker push 832214191436.dkr.ecr.ap-south-1.amazonaws.com/lambda-docker-fire:<container_tag>`
* Deploy new ECR image in Lambda Function