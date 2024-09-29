resource "aws_eks_cluster" "Micro_EKS" {
  name     = "micro-eks"
  role_arn = var.eks_cluster_role

  vpc_config {
    subnet_ids = var.vpc_private_subnets
  }

  # Ensure that IAM Role permissions are created before and deleted after EKS Cluster handling.
  # Otherwise, EKS will not be able to properly delete EKS managed EC2 infrastructure such as Security Groups.
  # depends_on = [
  #   var.eks_cluster_role_policy_attachment
  # ]
}

resource "aws_iam_openid_connect_provider" "eks" {
  url             = aws_eks_cluster.Micro_EKS.identity.0.oidc.0.issuer
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = ["9451ad2b53c7f41fab22886cc07d482085336561"]
}

data "aws_eks_cluster_auth" "Micro_EKS_Auth" {
  name = aws_eks_cluster.Micro_EKS.name
}
