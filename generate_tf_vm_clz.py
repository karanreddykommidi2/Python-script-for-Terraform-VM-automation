import argparse
import os

def write_file(filename, content):
    """Write content to a file."""
    with open(filename, "w") as f:
        f.write(content)
    print(f"Created {filename}")

# -------------------------
# Parse command-line args
# -------------------------
parser = argparse.ArgumentParser(description="Generate Terraform for VM using CLZ Network")
parser.add_argument("--app", required=True, help="Application name")
parser.add_argument("--env", required=True, help="Environment (dev/test/prod)")
parser.add_argument("--region", required=True, help="Azure region")
parser.add_argument("--vm_size", required=True, help="VM size")
parser.add_argument("--network_rg", required=True, help="Existing network resource group")
parser.add_argument("--vnet_name", required=True, help="Existing VNET name")
parser.add_argument("--subnet_name", required=True, help="Existing Subnet name")

args = parser.parse_args()

# -------------------------
# Create folder for app
# -------------------------
prefix = f"{args.app}-{args.env}-{args.region}"
os.makedirs(prefix, exist_ok=True)
os.chdir(prefix)

# -------------------------
# provider.tf
# -------------------------
provider_tf = """
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}
"""
write_file("provider.tf", provider_tf)

# -------------------------
# variables.tf
# -------------------------
variables_tf = """
variable "app" {}
variable "env" {}
variable "region" {}
variable "vm_size" {}
variable "network_rg" {}
variable "vnet_name" {}
variable "subnet_name" {}
"""
write_file("variables.tf", variables_tf)

# -------------------------
# terraform.tfvars
# -------------------------
tfvars = f"""
app          = "{args.app}"
env          = "{args.env}"
region       = "{args.region}"
vm_size      = "{args.vm_size}"
network_rg   = "{args.network_rg}"
vnet_name    = "{args.vnet_name}"
subnet_name  = "{args.subnet_name}"
"""
write_file("terraform.tfvars", tfvars)

# -------------------------
# main.tf
# -------------------------
main_tf = f"""
# Use existing CLZ network
data "azurerm_virtual_network" "clz_vnet" {{
  name                = var.vnet_name
  resource_group_name = var.network_rg
}}

data "azurerm_subnet" "clz_subnet" {{
  name                 = var.subnet_name
  virtual_network_name = data.azurerm_virtual_network.clz_vnet.name
  resource_group_name  = var.network_rg
}}

# Application Resource Group
resource "azurerm_resource_group" "app_rg" {{
  name     = "rg-{prefix}"
  location = var.region
}}

# NSG for the app
resource "azurerm_network_security_group" "app_nsg" {{
  name                = "nsg-{prefix}"
  location            = var.region
  resource_group_name = azurerm_resource_group.app_rg.name
}}

# Associate NSG to existing subnet
resource "azurerm_subnet_network_security_group_association" "nsg_assoc" {{
  subnet_id                 = data.azurerm_subnet.clz_subnet.id
  network_security_group_id = azurerm_network_security_group.app_nsg.id
}}

# Network Interface
resource "azurerm_network_interface" "nic" {{
  name                = "nic-{prefix}"
  location            = var.region
  resource_group_name = azurerm_resource_group.app_rg.name

  ip_configuration {{
    name                          = "internal"
    subnet_id                     = data.azurerm_subnet.clz_subnet.id
    private_ip_address_allocation = "Dynamic"
  }}
}}

# Linux VM
resource "azurerm_linux_virtual_machine" "vm" {{
  name                = "vm-{prefix}"
  resource_group_name = azurerm_resource_group.app_rg.name
  location            = var.region
  size                = var.vm_size
  admin_username      = "azureuser"
  network_interface_ids = [
    azurerm_network_interface.nic.id
  ]

  admin_ssh_key {{
    username   = "azureuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }}

  os_disk {{
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }}

  source_image_reference {{
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }}
}}
"""
write_file("main.tf", main_tf)

print("\nCLZ-aligned Terraform code generated successfully 🚀")
