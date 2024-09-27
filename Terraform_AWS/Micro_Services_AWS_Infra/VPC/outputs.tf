output "Micro_VPC_Id" {
  value = aws_vpc.Micro_Cluster_VPC.id
}
output "VPC_Private_Subnets" {
  value = aws_subnet.Micro_Private_Subnet[*].id
}
output "VPC_Public_Subnets" {
  value = aws_subnet.Micro_Public_Subnet[0].id
}
output "VPC_Security_Group_IDs" {
  value = [aws_security_group.Micro_Mysql_SG.id, aws_security_group.Micro_Postgres_SG.id]
}
output "Bastion_Security_Group" {
  value = aws_security_group.Bastion-SG.id
}
output "Jenkins_Security_Group" {
  value = aws_security_group.Jenkins-SG.id
}

