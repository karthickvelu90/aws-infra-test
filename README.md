# aws-infra-test

## Deployment Details : 

## Step
1. Creates Amazon Virtual Provate Cloud(VPC) - AWS crosswalk module used to create VPC and subnet.
   
2. Creates Elastic kubernetes Service (EKS) cluster with two node group. Pulumi_eks module used to create eks cluster and Node Group. 
   a. Tools - Min Node count 2 and scaling upto 5 nodes during peek load. 
   b. Microservice - Min Node count 2 and scaling upto 5 nodes during peek load.
   
3. Deploy two services using helm chart detailed inside helmchart folder.
   
   ### a. infra-web
   
     1. Added environment variable "ApiAddress" to access the infraapi service internally.
     2. Enabled HPA to scale up during peak load. Scaling will occur either of CPU or Memory utilization reaches 60%
     3. Assuming the CI pipeline will push the Docker image to ECR, repository URL will be updated.
     4. Accessible via Network Load Balancer with port 80. Internally pod exposes the service in 5000 port. service type marked as "LoadBalancer"
     5. Resources request and limit are defined for pods. Actual value need to be determined based on performance testing.
     6. Node Selector and Tolerations are added to pods to ensure pod get deployed in respective Node Group.
        
   ### b. infraapi
      
     1. Assuming the CI pipeline will push the Docker image to ECR, repository URL will be updated.
     2. Enabled HPA to scale up during peak load. Scaling will occur either of CPU or Memory utilization reaches 60%
     3. Accessible only within the cluster. Internally pod exposes the service in 5000 port. Service Type marked as "LoadBalancer"
     4. Resources request and limit are defined for pods. Actual value need to be determined based on performance testing.
     5. Node Selector and Tolerations are added to pods to ensure pod get deployed in respective Node Group. 


## Assumption: 
1. AWS account is avaliable. 
2. User executing the code was granted IAM policy. 
3. APIs of VPC, EKS are enabled in the account region. 

## IAC Execution step:
1. This code assumes the stack as "PROD".
2. Initialize the local virtual environment with dependencies. poetry is used to download dependencies.
3. Run "Pulumi Preview" command to validate before execution.
4. Once resource creation validated successfully, Run "Pulumi up" command to create required Infra components.


![aws_infra](https://github.com/user-attachments/assets/2ace5821-2611-494a-9e1a-660e0b380f95)

   
