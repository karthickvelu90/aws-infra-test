import pulumi
import pulumi_aws as aws
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
    
    # Create an Internet Gateway
        internet_gateway = aws.ec2.InternetGateway("internetGateway",
            vpc_id=vpc.vpc_id,
            tags=self.tags
        )

    # Create an Elastic IP for the NAT Gateway
        nat_eip = aws.ec2.Eip("natEip", 
            vpc=True
        )

    # Create a NAT Gateway in one of the public subnets
        nat_gateway = aws.ec2.NatGateway("natGateway",
            allocation_id=nat_eip.id,
            subnet_id=vpc.public_subnet_ids[0],
            tags=self.tags
        )

    # Create route table for the public subnets
        public_route_table = aws.ec2.RouteTable("publicRouteTable",
            vpc_id=vpc.vpc_id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    gateway_id=internet_gateway.id
                )
            ],
            tags=self.tags
        )

    # Create route table for the private subnets
        private_route_table = aws.ec2.RouteTable("privateRouteTable",
            vpc_id=vpc.vpc_id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    nat_gateway_id=nat_gateway.id
                )
            ],
            tags=self.tags
        )

    # Associate public subnets to the public route table
        for subnet_id in vpc.public_subnet_ids:
            aws.ec2.RouteTableAssociation(f"publicRouteTableAssociation-{subnet_id}",
                route_table_id=public_route_table.id,
                subnet_id=subnet_id
            )

    # Associate private subnets to the private route table
        for subnet_id in vpc.private_subnet_ids:
            aws.ec2.RouteTableAssociation(f"privateRouteTableAssociation-{subnet_id}",
                route_table_id=private_route_table.id,
                subnet_id=subnet_id
            )
        
        return create_vpc    
