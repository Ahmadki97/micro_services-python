variable "lb_srvaccount" {
  type        = string
  description = "Name of the aws lb controller service account"
}
variable "vpc_id" {
  type        = string
  description = "The ID of the VPC where the aws lb controller will be created"
}

variable "extdns_srvaccount" {
  type        = string
  description = "Name of the external-dns service account"
}