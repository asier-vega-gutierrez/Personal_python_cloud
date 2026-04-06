
#terraform apply -auto-approve -target=module.container_generator -var config_container_name=asier-container

resource "azurerm_storage_container" "config_container" {
  name                  = var.config_container_name
  storage_account_id    = var.storage_account_id
  container_access_type = "private"
}

