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

variable "vpc_private_subnets" {
  type = list(string)
}

variable "eks_cluster_role" {
  type = string
}

variable "eks_nodegroup_role" {
  type = string
}

variable "ec2_key_pair" {
  type = string
}

# variable "eks_cluster_role_policy_attachment" {
#   type = string
# }

# variable "node_group_policy_attachment" {
#   type = string
# }

# variable "cni_policy_attachment_var" {
#   type = string
# }

# variable "ec2_eks_container_registry_var" {
#   type = string
# }

