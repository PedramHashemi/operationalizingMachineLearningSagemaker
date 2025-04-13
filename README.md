# operationalizingMachineLearningSagemaker

## Step 1:

### Initial Setup
I create a sagemaker instance with in the `Applications and IDEs > studio`
![Screenshot 2025-04-13 at 11 28 43](https://github.com/user-attachments/assets/7983a0ca-4b63-440a-a526-9a270c6076cd)

I then create a jupyterlab with `ml.t5.medium`. This should be enough to run the jupyterlab itself. The instance has 5GB of storage which is enough for this project.
![Screenshot 2025-04-08 at 20 40 28](https://github.com/user-attachments/assets/61c2c14e-0aa6-4d04-af9a-f926418103a7)

### Download Data to an S3 Bucket
The first bucket on the following image is automatically created on creation of sagemaker.

I created the second bucket for everything that I perform in this project. `sagemaker-us-east-1-574117696758`.

![Screenshot 2025-04-13 at 11 39 43](https://github.com/user-attachments/assets/a072b396-127b-4cfc-b2ea-62c6d5f7f0bf)

Running the first few cells of the `train_and_deply_solution.ipynb` with the changes in the S3 bucket look like the image below.

![Screenshot 2025-04-13 at 11 44 15](https://github.com/user-attachments/assets/eec2795b-03c9-4ece-8a26-af2af3d246e9)

also for fitting the model:

![Screenshot 2025-04-13 at 11 45 00](https://github.com/user-attachments/assets/39791439-8038-4003-94d9-2e78e04a2810)

Later the model location will look like the folowing.

![Screenshot 2025-04-13 at 11 45 30](https://github.com/user-attachments/assets/dcf4b591-1d4f-43ba-a5f3-873d88f39931)


### Training and Deployment

The endpoint deployed is : `pytorch-inference-2025-04-13-07-44-25-598`

### Multi-Instance Training

I trained the model with 3 instances.
![Screenshot 2025-04-13 at 12 10 45](https://github.com/user-attachments/assets/3d20bf68-233c-4771-831b-44e78e7a6ef3)

One single instance and one multi-instance.
![Screenshot 2025-04-13 at 12 27 26](https://github.com/user-attachments/assets/672131ec-1721-48e5-a849-b3ba912be87e)

The Training with 3 instance.
![Screenshot 2025-04-13 at 12 27 41](https://github.com/user-attachments/assets/aad96632-97d2-45a8-a062-188a3ef5b283)


## Step 2

The following instances are created as shown in the image bellow.
![Screenshot 2025-04-08 at 22 59 47](https://github.com/user-attachments/assets/5371bcd3-1be7-4148-a0ad-528faf62a7b1)

The instance `c3.xlarge` is powerful and big enough to run the model.

![Screenshot 2025-04-08 at 22 04 32](https://github.com/user-attachments/assets/d6fca34f-0e80-4ade-bcd3-76d3964d73b4)

The following image shows the saved model and all the code saved in the ec2 instance.
![Screenshot 2025-04-08 at 22 51 09](https://github.com/user-attachments/assets/3e3a4df4-e5a3-4192-b5ed-9d70ed2557b3)


The code for the ec2 instance is much simpler since it doesn't have to work with the managed instances of sagemaker and the pytorch containers that it runs.

## Step 3

I have setup a lambda function with the provided code.

![Screenshot 2025-04-13 at 12 31 57](https://github.com/user-attachments/assets/cc9e32f5-2bcd-4600-8a49-3e51c2409f84)

![Screenshot 2025-04-13 at 09 48 25](https://github.com/user-attachments/assets/35399542-8beb-4522-a9d6-1302ad5bd2f6)

I added the endpoint mentioned in step 1.

- The endpoint gets a url for the location of the image in s3 bucket.
- Then it reads the json and returns the result of the json with success code 200.

## Step 4

I setup a test in the image bellow:

![Screenshot 2025-04-13 at 10 25 15](https://github.com/user-attachments/assets/3153ee5c-876b-4ac7-8900-d64f5230199c)

running the test will fail with the error that lambda does not have access to sagemaker.

![Screenshot 2025-04-13 at 09 49 58](https://github.com/user-attachments/assets/d1ab428c-0803-478f-bd19-9b8bbff0d299)

to solve this problem we add sagemaker full access to the permissions.

![Screenshot 2025-04-13 at 09 52 00](https://github.com/user-attachments/assets/91c9beb4-18cb-45c5-9765-8da5e3c26718)
![Screenshot 2025-04-13 at 09 54 48](https://github.com/user-attachments/assets/89f31cd9-ce86-4407-819f-5933da1a2ccf)

Now I run the test again and the result is success with code 200.

![Screenshot 2025-04-13 at 10 14 41](https://github.com/user-attachments/assets/37d4c63a-eb63-446a-9aa0-e6918c95edf9)

The workspace is secure since only this lambda function has access to it and the endpoint cannot be called from  elsewhere.
The vulnerabilities naturally occure with attaching fullaccess roles. This access can be minimized.

The old and inactive roles that contain this full access are vulnerable and can be exploited.

The projects and IAM roles must be ripped off of the roles that are irrelevant to them or the roles that they don't use anymore.

## Step 5

Setting up Concurrency

![Screenshot 2025-04-13 at 11 04 47](https://github.com/user-attachments/assets/55086d85-dfcf-40bc-94fb-3c18aaa11bc8

I have reserved 2 and 2 provisioned concurrency instance that are going to parallelize requests and keep the load on the instances lower.
Setting up Autoscaling
This can be costly as we have 2 reserved concurrency but it can well handle a high traffic situation and able to do concurrency for up to 2 instances more.

![Screenshot 2025-04-13 at 10 34 15](https://github.com/user-attachments/assets/4551e4cf-183d-4984-b292-2f6e93917ad9)

The Autoscaling will scale up the to up to 3 instances. We are only using CPU instances. It waits 600 mlseconds until it scale out and takes 600 mlsecond until it scale back down.
It takes a bit long 600mlseconds to scale up which can be a bit long and can yield failed api calls but reduce the costs. on the other hand it waits 600mlsecond before scaling down which can also increase the cost but it remains responsive for longer.



