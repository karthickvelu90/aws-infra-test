import pulumi
import pulumi_eks as eks


# Create EKS cluster with two Node group. one for Tools and other for microservices. 

class eks:
    
    def __init__(self, provider, tags, vpc_id, instanceType, min_size, max_size, vpc_private_subnet_id,  vpc_public_subnet_id, cluster_name, NodeGroupList ):
        
        self.provider = provider
        self.tags = tags
        self.vpc_id = vpc_id
        self.instanceType = instanceType
        self.min_size = min_size
        self.max_size = max_size
        self.vpc_private_subnet_id = vpc_private_subnet_id
        self.vpc_public_subnet_id = vpc_public_subnet_id
        self.cluster_name = cluster_name
        self.NodeGroupList = NodeGroupList
        
# Method for Node group creation based on input list provided. 
    def nodeGroup(self , NodeGroupName):
        return eks.ManagedNodeGroup(f"{NodeGroupName}-node-group",
            cluster=cluster.core,
            node_group_name=NodeGroupName,
            node_role=cluster.instance_role,
            subnet_ids= self.vpc_private_subnet_id,
            instance_types=[self.instanceType],
            scaling_config=eks.NodeGroupScalingConfigArgs(
                desired_size=self.min_size,
                min_size=self.min_size,
                max_size=self.max_size,
            ),
            tags=self.tags,
            labels={"service": f"{NodeGroupName}"}
            taints={
                "key": "service",
                "value": f"{NodeGroupName}",
                "effect": "NoSchedule",  # Possible values: NoSchedule, PreferNoSchedule, NoExecute
            },
            opts=pulumi.ResourceOptions(provider=self.provider)
            )

# Method for EKS cluster creation. 
    def eksCluster(self):
        
        cluster = eks.Cluster(self.cluster_name,
            create_oidc_provider=True,
            vpc_id=self.vpc_id,
            public_subnet_ids=self.vpc_public_subnet_id,
            private_subnet_ids=self.vpc_private_subnet_id,
            instance_role_policy_arns=[
                "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy",
                "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
                "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
            ],
            tags=self.tags,
            skip_default_node_group=True,
            opts=pulumi.ResourceOptions(provider=self.provider)
        )
    
        ## Loop Node Group creation using NodeGroupList variable. 
        NodeGroup_list = []
        for NodeGroupName in self.NodeGroupList:
            nodeGroup = nodeGroup(self, NodeGroupName)

            NodeGroup_list.append(nodeGroup)
    
        return cluster
    
    