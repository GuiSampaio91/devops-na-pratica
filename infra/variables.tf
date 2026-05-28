variable "project_name" {
  description = "Identificador do projeto, usado em tags e nomes de recursos."
  type        = string
  default     = "devops-na-pratica"
}

variable "environment" {
  description = "Ambiente de execucao (dev, hml, prd)."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "Regiao da AWS onde a infra sera provisionada."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo da instancia EC2. Default t2.micro (free tier)."
  type        = string
  default     = "t2.micro"
}

variable "allowed_ssh_cidr" {
  description = "Lista de CIDRs autorizados a abrir SSH na instancia."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
