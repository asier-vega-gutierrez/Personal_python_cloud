# Generate a random string
resource "random_string" "random" {
  length  = 6
  upper   = false
  special = false
}

# Storage account for all the files an dbs
resource "azurerm_storage_account" "cloud_sa" {
  name                     = "stor${random_string.random.id}"
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}