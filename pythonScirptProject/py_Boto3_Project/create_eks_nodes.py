import re
import boto3
import time
from botocore.client import BaseClient
from dotenv import load_dotenv
from my_variables import eks_nodes_variables




# 使用已存在的 VPC 設置
vpc_id = eks_nodes_variables["vpc_id"]  # 你的 VPC ID
subnet_ids = eks_nodes_variables['subnet_ids']  # 你的子網 ID
cluster_security_group_ids = eks_nodes_variables['cluster_security_group_ids']  # 你的安全組 ID
node_security_group_id = eks_nodes_variables['node_security_group_id']  # 你的節點組安全組 ID

# 使用已存在的 IAM 角色 ARN
role_arn = eks_nodes_variables['role_arn']  # 你的 EKS 集群 IAM 角色 ARN
node_role_arn = eks_nodes_variables['node_role_arn']  # 你的節點 IAM 角色 ARN
key_pair_name = eks_nodes_variables['key_pair_name']  # 你的密鑰對名稱






# 創建節點組
def create_node_group(cluster_name, nodegroup_name, node_role_arn, subnets, node_security_group_id, key_pair_name, group_node_dict):
    eks_client = boto3.client('eks')

    response = eks_client.create_nodegroup(
        clusterName=cluster_name,
        nodegroupName=nodegroup_name,
        scalingConfig={
            'minSize': group_node_dict['instance_num'],
            'maxSize': group_node_dict['instance_num'],
            'desiredSize': group_node_dict['instance_num']
        },
        diskSize=group_node_dict['disksize'],
        subnets=subnets,
        instanceTypes=[group_node_dict['instance_type'],],
        amiType='AL2_x86_64',  # Amazon Linux 2
        remoteAccess={
            'ec2SshKey': key_pair_name,
            'sourceSecurityGroups': [node_security_group_id]
        },
        nodeRole=node_role_arn
    )

    return response





if __name__ == "__main__":

    # 創建 EKS 集群
    cluster_name = eks_nodes_variables['cluster_name']
    eks_client = boto3.client('eks')

    # 創建 Node Group
    nodegroup_list_dict = eks_nodes_variables['nodegroup_list_dict']

    for nld in nodegroup_list_dict.keys():
        nodegroup_name = nld



        response = create_node_group(cluster_name, nodegroup_name, node_role_arn, subnet_ids, node_security_group_id, key_pair_name, nodegroup_list_dict[nodegroup_name])
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

