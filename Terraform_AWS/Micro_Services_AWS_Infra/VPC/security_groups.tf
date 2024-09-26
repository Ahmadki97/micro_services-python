resource "aws_security_group" "Micro_Mysql_SG" {
  name        = "Micro_Mysql_SG"
  description = "Allow MySQL traffic"
  vpc_id      = aws_vpc.Micro_Cluster_VPC.id
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "MySQL Security Group"
  }
}

resource "aws_security_group" "Micro_Postgres_SG" {
  name        = "Micro_Postgres_SG"
  description = "Allow PostgreSQL traffic"
  vpc_id      = aws_vpc.Micro_Cluster_VPC.id
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "PostgreSQL Security Group"
  }
}

resource "aws_security_group" "Micro_Elastic_Cache_SG" {
  name        = "Micro_Elastic_Cache_SG"
  description = "Allow redis Traffic"
  vpc_id      = aws_vpc.Micro_Cluster_VPC.id
  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "Elastic Cache SG"
  }
}

resource "aws_security_group" "Bastion-SG" {
  name_prefix = "bastion-sg"
  description = "Security group for Bastion Host allowing ping, SSH, HTTP, and HTTPS"
  vpc_id      = aws_vpc.Micro_Cluster_VPC.id

  # Ingress rule for allowing SSH
  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH from anywhere
  }

  # Ingress rule for allowing HTTP
  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTP from anywhere
  }

  # Ingress rule for allowing HTTPS
  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow HTTPS from anywhere
  }

  # Ingress rule for allowing ICMP (ping)
  ingress {
    description = "Allow ICMP ping"
    from_port   = -1
    to_port     = -1
    protocol    = "icmp"
    cidr_blocks = ["0.0.0.0/0"] # Allow ping from anywhere
  }

  # Egress rule to allow all outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outbound traffic
  }

  # Tag the security group
  tags = {
    Name = "Bastion-SG"
  }
}


resource "aws_security_group" "Jenkins-SG" {
  name        = "Jenkins-SG"
  description = "Allow access to jenkins"
  vpc_id      = aws_vpc.Micro_Cluster_VPC.id
  # Allow HTP Access
  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow HTTPS Access
  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  # Allow SSH Access
  ingress {
    description = "Allow SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow Jenkins Access
  ingress {
    description = "Allow Jenkins"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outbound traffic
  }

  tags = {
    Name = "Jenkins-SG"
  }
}



