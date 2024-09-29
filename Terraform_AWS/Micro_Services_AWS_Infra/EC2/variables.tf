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

variable "subnet_id" {
  type = string
}

variable "bastion_sg" {
  type = string
}
variable "jenkins_sg" {
  type = string
}
variable "Jenkins_Names" {
  type    = list(string)
  default = ["Jenkins_Master", "Jenkins_Agent"]
}