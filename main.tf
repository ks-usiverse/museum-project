provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false  # Set to delete even if resources remain in the resource group
    }
  }
  subscription_id = "9c9e23e3-df71-42db-9f2b-609c0c9efdac"  # Azure subscription ID
}

# Create a resource group
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "Germany West Central"  # Can be changed to any region
}

# Create a virtual network
resource "azurerm_virtual_network" "example" {
  name                = "example-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

# Create a subnet
resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Create a Public IP
resource "azurerm_public_ip" "example" {
  name                = "example-pip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"  # Standard SKUs require a change to Static
  sku                 = "Standard"  # Only Static IPs are allowed when the SKU is Standard
}

# Create a network security group
resource "azurerm_network_security_group" "example" {
  name                = "example-nsg"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"  # SSH Port
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"  # HTTP Port
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# Create a network interface
resource "azurerm_network_interface" "example" {
  name                = "example-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example.id  # Public IP Connections
  }
}

# Connect NSG to a network interface
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.example.id
  network_security_group_id = azurerm_network_security_group.example.id
}

# Create a virtual machine
resource "azurerm_virtual_machine" "example" {
  name                  = "example-vm"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = "Standard_DS1_v2"  # VM size

  # OS Disk Settings
  storage_os_disk {
    name              = "example-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  # Set up an OS image (using Ubuntu)
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  # Set up an OS profile
  os_profile {
    computer_name  = "example-vm"
    admin_username = var.admin_username   # Using variables
    admin_password = var.admin_password   # Handling variables with sensitive information
  }

  # Set up password authentication for Linux VMs
  os_profile_linux_config {
    disable_password_authentication = false  # Enable password authentication
  }

  # Install Docker and run a Docker Hub image after creating a virtual machine
  provisioner "remote-exec" {
    connection {
      type     = "ssh"
      user     = var.admin_username  # The username set up above
      password = var.admin_password  # The password set above
      host     = azurerm_public_ip.example.ip_address  # Public IP address
      port     = 22
    }

    inline = [
      "sleep 30",  # Wait for the VM to fully start
      "sudo apt-get update",
      "sudo apt-get install -y docker.io",  # Installing Docker
      "sudo systemctl start docker",        # Start Docker
      "sudo docker pull ksoochoi/fastapi:latest",  # Pull images from Docker Hub
      "sudo docker run -d -p 80:8000 ksoochoi/fastapi:latest"  # Run the image
    ]
  }
}

output "public_ip_address" {
  value = azurerm_public_ip.example.ip_address
}