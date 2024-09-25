resource "aws_subnet" "Micro_Public_Subnet" {
  count             = var.subnets_count
  vpc_id            = aws_vpc.Micro_Cluster_VPC.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = element(var.availability_zones, count.index)
  tags = {
    Name = "Public Subnet ${count.index + 1}"
  }
}

resource "aws_subnet" "Micro_Private_Subnet" {
  count             = var.subnets_count
  vpc_id            = aws_vpc.Micro_Cluster_VPC.id
  cidr_block        = "10.0.${count.index + 2}.0/24"
  availability_zone = element(var.availability_zones, count.index)
  tags = {
    Name = "Private Subnet ${count.index + 1}"
  }
}