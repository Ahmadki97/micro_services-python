resource "aws_db_subnet_group" "Micro_Subnet_Group" {
  name       = "micro_rds"
  subnet_ids = var.vpc_private_subnets
  tags = {
    Name = "Micro_DB subnet group"
  }
}
