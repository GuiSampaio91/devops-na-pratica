output "instance_id" {
  description = "ID da instancia EC2 criada."
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "IP publico da instancia EC2."
  value       = aws_instance.app.public_ip
}

output "app_url" {
  description = "URL onde a aplicacao Flask estara disponivel."
  value       = "http://${aws_instance.app.public_ip}:5000"
}

output "security_group_id" {
  description = "ID do Security Group associado a instancia."
  value       = aws_security_group.app.id
}
