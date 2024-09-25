resource "aws_internet_gateway" "Micro_IGW" {
  vpc_id = aws_vpc.Micro_Cluster_VPC.id
  tags = {
    Name = "main IGW for micro-cluster VPC"
  }
}
