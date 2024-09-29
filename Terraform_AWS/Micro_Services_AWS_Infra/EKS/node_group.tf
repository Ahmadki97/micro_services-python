resource "aws_eks_node_group" "Micro_EKS_NodeGroup" {
  cluster_name    = aws_eks_cluster.Micro_EKS.name
  node_group_name = "micro_node_group"
  node_role_arn   = var.eks_nodegroup_role
  subnet_ids      = var.vpc_private_subnets
  instance_types  = ["t3.medium"]
  remote_access {
    ec2_ssh_key = var.ec2_key_pair
  }
  disk_size = "30"
  ami_type  = "AL2_x86_64"

  scaling_config {
    desired_size = 4
    max_size     = 5
    min_size     = 2
  }

  update_config {
    max_unavailable = 1
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Node Group handling.
  # Otherwise, EKS will not be able to properly delete EC2 Instances and Elastic Network Interfaces.
  # depends_on = [
  #   var.node_group_policy_attachment_var,
  #   var.cni_policy_attachment_var,
  #   var.ec2_eks_container_registry_var,
  # ]
}
