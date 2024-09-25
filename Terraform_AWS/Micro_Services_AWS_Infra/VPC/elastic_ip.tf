
resource "aws_eip" "Micro_EIP" {
  domain = "vpc"
  tags = {
    Name = "Elastic IP for Micro App NatGateway"
  }
}
