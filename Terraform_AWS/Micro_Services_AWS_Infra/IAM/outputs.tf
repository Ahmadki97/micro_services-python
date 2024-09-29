output "Micro_EKS_Role_ARN" {
  value = aws_iam_role.Micro_EKS_Role.arn
}
output "Micro_EKS_Role_Attachment" {
  value = aws_iam_role_policy_attachment.Micro_EKS_Role_Attachment
}
# output "WorkerNodes_Policy_Attachment" {
#   value = aws_iam_role_policy_attachment.Micro_NodeGroup_Policy_Attachment
# }
# output "EKS_CNI_Policy_Attachment" {
#   value = aws_iam_role_policy_attachment.EKS_CNI_Policy
# }
# output "EKS_EC2_Container_Registery_Attachment" {
#   value = aws_iam_role_policy_attachment.EC2ContainerRegistryReadOnly
# }

output "Micro_EKS_NodeGroup_Role_Var" {
  value = aws_iam_role.Micro_EKS_NodeGroup_Role.arn
}

output "aws_lb_controller_sva" {
  value = kubernetes_service_account.awslb.metadata[0].name
}

output "aws_extdns_sva" {
  value = kubernetes_service_account.external-dns.metadata[0].name
}