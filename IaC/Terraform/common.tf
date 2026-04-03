# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Resource group that cotains all the resources for the project
resource "azurerm_resource_group" "cloud_rg" {
  name     = "cloud_rg"
  location = "West Europe"
}

# Generate a random string
resource "random_string" "random" {
  length  = 6
  upper   = false
  special = false
}

# Storage account for all the files an dbs
resource "azurerm_storage_account" "cloud_sa" {
  name                     = "stor${random_string.random.id}"
  resource_group_name      = azurerm_resource_group.cloud_rg.name
  location                 = azurerm_resource_group.cloud_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "files_container" {
  name                  = "files-container"
  storage_account_name  = azurerm_storage_account.cloud_sa.name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "blob_asier" {
  name                   = "blob_asier"
  storage_account_name   = azurerm_storage_account.cloud_sa.name
  storage_container_name = azurerm_storage_container.files_container.name
  type                   = "Block"
}
