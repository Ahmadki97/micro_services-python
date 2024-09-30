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

variable "dbs_sgs" {
  type = list(string)
}
