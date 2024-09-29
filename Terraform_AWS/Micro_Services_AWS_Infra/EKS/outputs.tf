output "eks-cluster-endpoint" {
  value = aws_eks_cluster.Micro_EKS.endpoint
}
output "eks-cluster-ca" {
  value = aws_eks_cluster.Micro_EKS.certificate_authority[0].data
}
output "eks-oidc-provider" {
  value = aws_eks_cluster.Micro_EKS.identity[0].oidc[0].issuer
}
output "eks-cluster-token" {
  value = data.aws_eks_cluster_auth.Micro_EKS_Auth.token
}
output "oidc-arn" {
  value = aws_iam_openid_connect_provider.eks.arn
}