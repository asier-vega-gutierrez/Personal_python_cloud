# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.67.0"
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

# Modules
module "storage" {
  source = "./storage"
  resource_group_name   = azurerm_resource_group.cloud_rg.name
  resource_group_location = azurerm_resource_group.cloud_rg.location
}

module "function" {
  source = "./function"
  resource_group_name   = azurerm_resource_group.cloud_rg.name
  resource_group_location = azurerm_resource_group.cloud_rg.location
}



