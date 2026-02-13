# Terraform Automation Python Script

This Python script generates **Terraform code for Azure application VMs**, referencing existing Cloud Landing Zone (CLZ) networks.

## Features

- Generates Resource Group, NSG, NIC, and Linux VM
- References existing VNET/Subnet (avoids network sprawl)
- Enforces naming conventions automatically
- Produces ready-to-deploy Terraform code

## Usage

```bash
python generate_tf_vm_clz.py \
  --app payments \
  --env dev \
  --region eastus \
  --vm_size Standard_B2s \
  --network_rg rg-clz-network \
  --vnet_name vnet-clz-eastus \
  --subnet_name snet-app-eastus
