terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

variable "services" {
  description = "Endpoints monitored by the Python health checker"

  type = list(object({
    name = string
    url  = string
  }))

  default = [
    {
      name = "nginx"
      url  = "http://localhost"
    },
    {
      name = "local-test-app"
      url  = "http://localhost:8080"
    }
  ]
}

resource "local_file" "health_configuration" {
  filename = "${path.module}/../python-health-check/services.json"

  content = jsonencode({
    services = var.services
  })
}

output "configuration_file" {
  description = "Path to the generated health-check configuration"
  value       = local_file.health_configuration.filename
}
