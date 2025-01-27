import re
import boto3
import time
from botocore.client import BaseClient
from dotenv import load_dotenv
from my_variables import eks_cluster_variables






# 使用已存在的 VPC 設置
vpc_id = eks_cluster_variables["vpc_id"]  # 你的 VPC ID
subnet_ids = eks_cluster_variables['subnet_ids']  # 你的子網 ID
cluster_security_group_ids = eks_cluster_variables['cluster_security_group_ids']  # 你的安全組 ID
node_security_group_id = eks_cluster_variables['node_security_group_id']  # 你的節點組安全組 ID

# 使用已存在的 IAM 角色 ARN
role_arn = eks_cluster_variables['role_arn']  # 你的 EKS 集群 IAM 角色 ARN
node_role_arn = eks_cluster_variables['node_role_arn']  # 你的節點 IAM 角色 ARN
key_pair_name = eks_cluster_variables['key_pair_name']  # 你的密鑰對名稱
k8s_managemnt_tool_ip = eks_cluster_variables["k8s_managemnt_tool_ip"]   ## K8s 管理工具 IP













# 創建 EKS 集群
def create_eks_cluster(cluster_name, role_arn, vpc_config):
    eks_client = boto3.client('eks')

    response = eks_client.create_cluster(
        name=cluster_name,
        version='1.28',  # 或任何你需要的 EKS 版本
        roleArn=role_arn,
        resourcesVpcConfig=vpc_config,
        logging={
            'clusterLogging': [
                {
                    'types': [
                        'api',
                        'audit',
                        'authenticator',
                        'controllerManager',
                        'scheduler'
                    ],
                    'enabled': True
                }
            ]
        }
    )

    return response

# 創建節點組
def create_node_group(cluster_name, nodegroup_name, node_role_arn, subnets, node_security_group_id, key_pair_name):
    eks_client = boto3.client('eks')

    response = eks_client.create_nodegroup(
        clusterName=cluster_name,
        nodegroupName=nodegroup_name,
        scalingConfig={
            'minSize': 1,
            'maxSize': 1,
            'desiredSize': 1
        },
        diskSize=20,
        subnets=subnets,
        instanceTypes=['t3.medium'],
        amiType='AL2_x86_64',  # Amazon Linux 2
        remoteAccess={
            'ec2SshKey': key_pair_name,
            'sourceSecurityGroups': [node_security_group_id]
        },
        nodeRole=node_role_arn
    )

    return response

# 安裝 AWS 預設建議的 add-ons
def install_addons(cluster_name):
    eks_client = boto3.client('eks')

    addons = ['vpc-cni', 'coredns', 'kube-proxy', 'eks-pod-identity-webhook']
    for addon in addons:
        try:
            eks_client.create_addon(
                clusterName=cluster_name,
                addonName=addon,
                resolveConflicts='OVERWRITE'
            )
        except eks_client.exceptions.ResourceInUseException:
            print(f"Addon {addon} is already installed.")

if __name__ == "__main__":
    # VPC 配置
    vpc_config = {
        'subnetIds': subnet_ids,
        'securityGroupIds': cluster_security_group_ids,
        'endpointPublicAccess': True,
        'endpointPrivateAccess': True,
        'publicAccessCidrs': [
            k8s_managemnt_tool_ip
        ]
    }

    # 創建 EKS 集群
    cluster_name = eks_cluster_variables['cluster_name']
    response = create_eks_cluster(cluster_name, role_arn, vpc_config)
    print(f"Creating EKS Cluster: {response}")

    # 等待 EKS 集群創建完成
    eks_client = boto3.client('eks')
    while True:
        response = eks_client.describe_cluster(name=cluster_name)
        status = response['cluster']['status']
        print(f"Cluster status: {status}")
        if status == 'ACTIVE':
            print("EKS Cluster is active.")
            break
        time.sleep(60)

    # 創建 Node Group
    nodegroup_name = eks_cluster_variables['nodegroup_name']
    response = create_node_group(cluster_name, nodegroup_name, node_role_arn, subnet_ids, node_security_group_id, key_pair_name)
    print(f"Creating Node Group: {response}")

    # 等待 Node Group 創建完成
    while True:
        response = eks_client.describe_nodegroup(clusterName=cluster_name, nodegroupName=nodegroup_name)
        status = response['nodegroup']['status']
        print(f"Node Group status: {status}")
        if status == 'ACTIVE':
            print("Node Group is active.")
            break
        time.sleep(60)

    # 安裝 add-ons
    #install_addons(cluster_name)
    print(f"Add-ons installed for cluster {cluster_name}")