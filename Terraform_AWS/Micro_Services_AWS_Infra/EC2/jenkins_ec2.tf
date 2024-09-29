# resource "aws_instance" "Jenkins" {
#   count                       = 2
#   ami                         = "ami-0e86e20dae9224db8"
#   instance_type               = "t2.micro"
#   associate_public_ip_address = true
#   key_name                    = aws_key_pair.Micro_Worker_Key.key_name
#   subnet_id                   = var.subnet_id
#   security_groups             = [var.jenkins_sg]
#   ebs_block_device {
#     device_name           = "/dev/sdh"
#     volume_size           = "20"
#     volume_type           = "gp2"
#     delete_on_termination = true
#   }
#   user_data = <<-EOF
#             #!/bin/bash
#             sudo apt update
#             sudo apt install -y openjdk-17-jre
#             sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
#             sudo echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
#             sudo apt-get update
#             sudo apt-get install -y jenkins
#             sudo systemctl enable jenkins
#             EOF
#   tags = {
#     Name = var.Jenkins_Names[count.index]
#   }
# }