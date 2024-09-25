resource "aws_vpc" "Micro_Cluster_VPC" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = "true"
  tags = {
    Name = "VPC for microservices app"
  }
}








