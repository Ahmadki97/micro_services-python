variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "subnets_count" {
  type    = number
  default = 2
}

variable "rds_type" {
  type    = list(string)
  default = ["mysql", "postgres"]
}

variable "db_names" {
  type    = list(string)
  default = ["micro_auth", "review_db"]
}

variable "nodegroup_policies" {
  type = list(string)
  default = [
    "arn:aws:iam::014498645803:policy/MicroWorkerNodesPolicy",
    "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy",
    "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly",
    "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
  ]
}

variable "oidc_arn" {
  type = string
}
