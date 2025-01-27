eks_cluster_variables = {
    # 使用已存在的 VPC 設置
    "vpc_id": "vpc-0c1de954c8a6",  # 你的 VPC ID
    "subnet_ids": ['subnet-057271755c1d5', 'subnet-0862df737141', 'subnet-0d68d2b3c43', 'subnet-0453f2500c36a', 'subnet-042652dfdad4', 'subnet-04267af0c9c1'],  # 你的子網 ID
    "cluster_security_group_ids": ['sg-061992be167b', 'sg-062052fbe8d5f'],  # 你的安全組 ID
    "node_security_group_id": 'sg-0619962be167b',  # 你的節點組安全組 ID

    # 使用已存在的 IAM 角色 ARN
    "role_arn": 'arn:aws:iam::6665835:role/eks-cluster-2023-12--AWSServiceRoleForAmazonEK-elkimrdMBV',  # 你的 EKS 集群 IAM 角色 ARN
    "node_role_arn": 'arn:aws:iam::6665835:role/prod-node-instance-role-NodeInstanceRole-2GHT82FVFB',  # 你的節點 IAM 角色 ARN
    "key_pair_name": 'aws-key-pair',  # 你的密鑰對名稱
    "k8s_managemnt_tool_ip": "51.168.105.93/32",  ## K8s 管理工具 IP
    "cluster_name": 'test-cluster-1',   ## K8s cluster name
    "nodegroup_name": 'system-group',   ##  K8s System node name
}



eks_nodes_variables = {
    # 使用已存在的 VPC 設置
    "vpc_id": "vpc-0c1de954c8a6",  # 你的 VPC ID
    "subnet_ids": ['subnet-057271755c1d5', 'subnet-0862df737141', 'subnet-0d68d2b3c43', 'subnet-0453f2500c36a', 'subnet-042652dfdad4', 'subnet-04267af0c9c1'],  # 你的子網 ID
    "cluster_security_group_ids": ['sg-061992be167b', 'sg-062052fbe8d5f'],  # 你的安全組 ID
    "node_security_group_id": 'sg-0619962be167b',  # 你的節點組安全組 ID

    # 使用已存在的 IAM 角色 ARN
    "role_arn": 'arn:aws:iam::6665835:role/eks-cluster-2023-12--AWSServiceRoleForAmazonEK-elkimrdMBV',  # 你的 EKS 集群 IAM 角色 ARN
    "node_role_arn": 'arn:aws:iam::6665835:role/prod-node-instance-role-NodeInstanceRole-2GHT82FVFB',  # 你的節點 IAM 角色 ARN
    "key_pair_name": 'aws-key-pair',  # 你的密鑰對名稱
    "cluster_name": 'test-cluster-1',   ## K8s cluster name
    "nodegroup_list_dict": {
        'backend-node-group': {'instance_num': 1, 'instance_type': 'c5.xlarge', 'disksize': 40},
        'frontend-group-node': {'instance_num': 1, 'instance_type': 'c5.xlarge', 'disksize': 40},
    },
}


