output "Worker_Nodes_Key_ID" {
  value = aws_key_pair.Micro_Worker_Key.id
}

output "private_key_pem" {
  value     = tls_private_key.Micro-Private-Key.private_key_pem
  sensitive = true
}

