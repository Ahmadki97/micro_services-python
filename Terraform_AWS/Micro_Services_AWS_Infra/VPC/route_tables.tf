resource "aws_route_table" "Micro_Public_Table" {
  vpc_id = aws_vpc.Micro_Cluster_VPC.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.Micro_IGW.id
  }
  tags = {
    Name = "Public Route Table"
  }
}

resource "aws_route_table" "Micro_Private_Table" {
  vpc_id = aws_vpc.Micro_Cluster_VPC.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.Micro_Natgateway.id
  }
  tags = {
    Name = "Private Route Table"
  }
}

resource "aws_route_table_association" "Public_Subnet_Association" {
  count          = var.subnets_count
  subnet_id      = aws_subnet.Micro_Public_Subnet[count.index].id
  route_table_id = aws_route_table.Micro_Public_Table.id
}

resource "aws_route_table_association" "Private_Subnet_Association" {
  count          = var.subnets_count
  subnet_id      = aws_subnet.Micro_Private_Subnet[count.index].id
  route_table_id = aws_route_table.Micro_Private_Table.id
}
