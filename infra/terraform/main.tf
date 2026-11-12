resource "azurerm_resource_group" "iot" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_eventhub_namespace" "iot" {
  name                = var.namespace_name
  location            = azurerm_resource_group.iot.location
  resource_group_name = azurerm_resource_group.iot.name
  sku                 = "Basic"
  capacity            = 1

  local_authentication_enabled = false
  minimum_tls_version          = "1.2"
}

resource "azurerm_eventhub" "telemetry" {
  name              = "synthetic-telemetry"
  namespace_id      = azurerm_eventhub_namespace.iot.id
  partition_count   = 2
  message_retention = 1
}
