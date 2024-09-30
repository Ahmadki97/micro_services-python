resource "aws_db_instance" "Micro_RDS" {
  count                       = 2
  allocated_storage           = 20
  storage_type                = "gp2"
  allow_major_version_upgrade = false
  db_name                     = element(var.db_names, count.index)
  engine                      = element(var.rds_type, count.index)
  instance_class              = "db.t3.micro"
  username                    = "ahmad"
  password                    = "0938460904am"
  multi_az                    = false
  storage_encrypted           = true
  db_subnet_group_name        = aws_db_subnet_group.Micro_Subnet_Group.name
  vpc_security_group_ids = [
    var.rds_type[count.index] == "mysql" ? element(var.dbs_sgs, 0) : element(var.dbs_sgs, 1),
  ]
  skip_final_snapshot = true
}