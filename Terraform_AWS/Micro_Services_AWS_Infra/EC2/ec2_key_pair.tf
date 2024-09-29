# We should be able to access the key or we will never be able to restore it
# TO download it we can export the tls_private key
# After Performing Terrafrom apply we can use the command terraform output -raw private_key_pem > micro_worker_key.pem 
resource "tls_private_key" "Micro-Private-Key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "Micro_Worker_Key" {
  key_name   = "micro_worker_key"
  public_key = tls_private_key.Micro-Private-Key.public_key_openssh
}

