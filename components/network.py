import pulumi
import pulumi_awsx as awsx


# Create a VPC in AWS account with two subnets. One with private and another with Public. 
class network:
    
    def __init__(self, provider, tags, vpc_name, vpc_cidr, subnet_cidr_mask):
        self.provider = provider
        self.tags = tags
        self.vpc_name = vpc_name
        self.vpc_cidr = vpc_cidr
        self.subnet_cidr_mask = subnet_cidr_mask
    
# Method for VPC creation. 
    def vpc(self):
        
        create_vpc = awsx.ec2.Vpc(self.vpc_name,
            cidr_block= self.vpc_cidr,
            tags=self.tags,
            nat_gateways=awsx.ec2.NatGatewayConfigurationArgs(
                strategy="Single",
            ),
            subnet_specs=[
                awsx.ec2.SubnetSpecArgs(
                    type="public",
                    cidr_mask=self.subnet_cidr_mask,
                    tags=self.tags,
                ),
                awsx.ec2.SubnetSpecArgs(
                    type="private",
                    cidr_mask=self.subnet_cidr_mask,
                    tags=self.tags,
                ),
            ],
            opts=pulumi.ResourceOptions(provider=self.provider)
        )        
        return create_vpc