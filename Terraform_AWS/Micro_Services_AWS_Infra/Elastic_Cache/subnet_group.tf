resource "aws_elasticache_subnet_group" "Cache_Subnet_Group" {
  name       = "cach-subnet-group"
  subnet_ids = var.vpc_private_subnets
}