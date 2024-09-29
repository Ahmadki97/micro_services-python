# resource "aws_instance" "Bastion-Host" {
#   ami                         = "ami-066784287e358dad1"
#   instance_type               = "t2.micro"
#   associate_public_ip_address = true
#   key_name                    = aws_key_pair.Micro_Worker_Key.key_name
#   subnet_id                   = var.subnet_id
#   security_groups             = [var.bastion_sg]
#   ebs_block_device {
#     device_name           = "/dev/sdh"
#     volume_size           = "20"
#     volume_type           = "gp2"
#     delete_on_termination = true
#   }
#   tags = {
#     Name = "Bastion-Host"
#   }
# }