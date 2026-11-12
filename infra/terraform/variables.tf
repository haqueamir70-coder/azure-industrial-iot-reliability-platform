variable "resource_group_name" {
  type        = string
  description = "Resource group for the isolated demo namespace."
  default     = "rg-industrial-iot-demo"
}

variable "location" {
  type        = string
  description = "Azure region."
  default     = "eastus"
}

variable "namespace_name" {
  type        = string
  description = "Globally unique Event Hubs namespace name."
}
