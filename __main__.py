import pulumi
import pulumi_aws as aws
import pulumi_eks as eks
import pulumi_kubernetes as k8s
from components.network import network
from components.eks import eks
from components.helmDeploy import helmDeploy


# Input variables defined during planning phase. 

config = pulumi.Config("prod")
aws_region = config.require("aws_region")
vpc_name =  config.require("vpc_name")
tags = config.require_object("tags")
vpc_cidr = config.require("vpc_cidr")
subnet_cidr_mask = config.require("subnet_cidr_mask")
instanceType = config.require("instanceType")
min_size = config.require_int("min_size")
max_size = config.require_int("max_siz")
NodeGroupList = config.require_object("NodeGroupList")
cluster_name = config.require("cluster_name")
service_list = config.require_object("service_list")


# Specify the AWS provider with the region: Toronto , Canada 
provider = aws.Provider("aws-provider", region="ca-central-1")

# Create VPC with the predefined cidr and subnet requirements. 
vpc = network(provider, tags, vpc_name, vpc_cidr, subnet_cidr_mask)
create_vpc = vpc.vpc()


# Update VPC information to variable.  
vpc_id = create_vpc.id
vpc_private_subnet_id = create_vpc.private_subnet_ids
vpc_public_subnet_id = create_vpc.public_subnet_ids


# Create Kubernetes Cluster with 2 node Group named "Tools" & "Microservice"
eks_cluster = eks(provider, tags, vpc_id, vpc_private_subnet_id, vpc_public_subnet_id, instanceType, min_size, max_size , cluster_name, NodeGroupList)
create_eks_cluster = eks_cluster.eksCluster()

# Assign cluster to variable
eks_kubeconfig = create_eks_cluster.kubeconfig


# Create a K8s provider instance using the EKS cluster's kubeconfig
k8s_provider = k8s.Provider("k8s-provider", kubeconfig=eks_kubeconfig)


# Deploy Microservices to EKS cluster using helm. 
service_deploy = helmDeploy(service_list, k8s_provider)
service_deploy.deploy_local()