provider "azurerm" {
  features {}
}

# Test fetching your Azure subscription
data "azurerm_subscription" "primary" {}

output "subscription_id" {
  value = data.azurerm_subscription.primary.subscription_id
}
