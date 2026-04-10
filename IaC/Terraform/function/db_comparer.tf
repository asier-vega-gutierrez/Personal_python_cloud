resource "azurerm_storage_account" "db_comparer_sa" {
  name                     = "dbcomparersa"
  resource_group_name      = var.resource_group_name
  location                 = var.resource_group_location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "db_comparer_sp" {
  name                = "db_comparer_sp"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  os_type             = "Linux"
  sku_name            = "Y1"    #Plan de consumo (pay as you go)
}

resource "azurerm_linux_function_app" "db_comparer_function" {
  name                = "dbcomparer-function"

  resource_group_name = var.resource_group_name
  location            = var.resource_group_location

  storage_account_name       = azurerm_storage_account.db_comparer_sa.name
  storage_account_access_key = azurerm_storage_account.db_comparer_sa.primary_access_key
  service_plan_id            = azurerm_service_plan.db_comparer_sp.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
  }
}