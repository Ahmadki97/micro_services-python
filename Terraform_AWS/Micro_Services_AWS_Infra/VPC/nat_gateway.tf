resource "aws_nat_gateway" "Micro_Natgateway" {
  allocation_id = aws_eip.Micro_EIP.id
  subnet_id     = aws_subnet.Micro_Public_Subnet[0].id
  tags = {
    Name = "Nat Gateway for our Microservices App"
  }
}