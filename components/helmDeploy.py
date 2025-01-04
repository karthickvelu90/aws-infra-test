import pulumi
import pulumi_kubernetes as k8s


# Class to deploy services using helm chart. 
class helmDeploy:
    
    def __init__(self, service_list, k8s_provider):
        self.service_list = service_list
        self.k8s_provider = k8s_provider

 
    # This definition assumes the helm chart are available in local path to deploy the service into kubernetes. 
    def deploy_local(self):
        # Loop to run service helm chart/ 
        deployments = []
        for service in self.service_list:
            
            # Helm chart path to be used. 
            helmPath = f"./helmchart/{service}"
            
            # Invoke helm module. 
            deployment = k8s.helm.v3.Chart(service,
            k8s.helm.v3.ChartOpts(
                path=helmPath,  # Specify the path to your local Helm chart directory
            ),
            opts=pulumi.ResourceOptions(provider=self.k8s_provider)
            ) 
        deployments.append(deployment)
        return deployments
    
    
    ######### Store the helm chart in ECR and call them during deployment.  ##########
    
    # def deploy_remote( service, helmPath):  
    #     self.apply_helm_chart = k8s.helm.v3.Chart("nginx",
    #         k8s.helm.v3.ChartOpts(
    #             repo="<ECR Repository URL >",
    #             chart="<service / chart name>",
    #             version="<Chart version>",
    #             values={
    #                 # Can Use this section to overwrite the default values.yaml values during deployment. 
    #             },
    #         ),
    #         opts=pulumi.ResourceOptions(provider=k8s_provider)
    #     )
        
