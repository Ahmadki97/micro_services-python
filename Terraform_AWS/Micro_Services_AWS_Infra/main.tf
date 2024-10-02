module "VPC" {
  source = "./VPC"
}

module "IAM" {
  source   = "./IAM"
  oidc_arn = module.EKS.oidc-arn
}

# module "RDS" {
#   source              = "./RDS"
#   vpc_private_subnets = module.VPC.VPC_Private_Subnets
#   dbs_sgs             = module.VPC.VPC_Security_Group_IDs
# }

module "EKS" {
  source              = "./EKS"
  vpc_private_subnets = module.VPC.VPC_Private_Subnets
  eks_cluster_role    = module.IAM.Micro_EKS_Role_ARN
  eks_nodegroup_role  = module.IAM.Micro_EKS_NodeGroup_Role_Var
  ec2_key_pair        = module.EC2.Worker_Nodes_Key_ID
  # eks_cluster_role_policy_attachment= module.IAM.Micro_EKS_Role_Attachment
  # node_group_policy_attachment = module.IAM.WorkerNodes_Policy_Attachment
  # cni_policy_attachment_var = module.IAM.EKS_CNI_Policy_Attachment
  # ec2_eks_container_registry_var = module.IAM.EKS_EC2_Container_Registery_Attachment
}

module "EC2" {
  source     = "./EC2"
  subnet_id  = module.VPC.VPC_Public_Subnets
  bastion_sg = module.VPC.Bastion_Security_Group
  jenkins_sg = module.VPC.Jenkins_Security_Group
}

# module "Elastic_Cache" {
#   source              = "./Elastic_Cache"
#   vpc_private_subnets = module.VPC.VPC_Private_Subnets
# }

module "Helm" {
  source            = "./HELM"
  vpc_id            = module.VPC.Micro_VPC_Id
  lb_srvaccount     = module.IAM.aws_lb_controller_sva
  extdns_srvaccount = module.IAM.aws_extdns_sva
}

# module "Route53" {
#   source = "./Route53"
#   vpc_id = module.VPC.Micro_VPC_Id
#   domain_validation_options = module.ACM.cert_validation_options
# }

# module "ACM" {
#   source = "./ACM"
#   route53_records = module.Route53.route53_records
# }

