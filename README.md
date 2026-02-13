# Python Script for Terraform VM Automation

This Python script automates the creation of **Terraform code for Azure Virtual Machines (VMs)**, including:

- Resource Groups
- Network Security Groups (NSGs)
- Network Interfaces (NICs)
- Linux Virtual Machines

It references **existing Cloud Landing Zone (CLZ) VNETs/Subnets**, ensuring that application deployments **reuse shared network infrastructure** and **avoid duplication or network sprawl**.

---

## Features

- Generates Terraform files automatically:
  - `provider.tf`
  - `variables.tf`
  - `terraform.tfvars`
  - `main.tf`
- Enforces **naming conventions** based on app, environment, and region.
- Reusable for multiple applications and environments.
- CLZ-aligned: App-level resources deployed on existing VNET/Subnet.

---

## Prerequisites

Before running the script, ensure you have:

1. **Python 3** (3.8+ recommended)
   ```bash
   python --version
2 terraform -version

3 Azure CLI logged in
  az login
  
4 SSH key for Linux VM access
  ssh-keygen -t rsa -b 2048
  
5 Single-line command (Windows CMD)
  python generate_tf_vm_clz.py --app payments --env dev --region eastus --vm_size Standard_B2s --network_rg rg-clz-network --vnet_name      vnet-clz-eastus --subnet_name snet-app-eastus
