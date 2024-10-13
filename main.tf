provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false  # 리소스 그룹에 리소스가 남아 있어도 삭제하도록 설정
    }
  }
  subscription_id = "9c9e23e3-df71-42db-9f2b-609c0c9efdac"  # Azure 구독 ID
}

# 리소스 그룹 생성
resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "Germany West Central"  # 원하는 리전으로 변경 가능
}

# 가상 네트워크 생성
resource "azurerm_virtual_network" "example" {
  name                = "example-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

# 서브넷 생성
resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.1.0/24"]
}

# Public IP 생성
resource "azurerm_public_ip" "example" {
  name                = "example-pip"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
  allocation_method   = "Static"  # Standard SKU에서는 Static으로 변경해야 함
  sku                 = "Standard"  # SKU가 Standard일 때는 Static IP만 허용됨
}

# 네트워크 보안 그룹 생성
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
    destination_port_range     = "22"  # SSH 포트
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
    destination_port_range     = "80"  # HTTP 포트
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

# 네트워크 인터페이스 생성
resource "azurerm_network_interface" "example" {
  name                = "example-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.example.id  # Public IP 연결
  }
}

# 네트워크 인터페이스에 NSG 연결
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.example.id
  network_security_group_id = azurerm_network_security_group.example.id
}

# 가상 머신 생성
resource "azurerm_virtual_machine" "example" {
  name                  = "example-vm"
  location              = azurerm_resource_group.example.location
  resource_group_name   = azurerm_resource_group.example.name
  network_interface_ids = [azurerm_network_interface.example.id]
  vm_size               = "Standard_DS1_v2"  # VM 크기

  # OS 디스크 설정
  storage_os_disk {
    name              = "example-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  # OS 이미지 설정 (Ubuntu 사용)
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  # OS 프로필 설정
  os_profile {
    computer_name  = "example-vm"
    admin_username = var.admin_username   # 변수를 사용
    admin_password = var.admin_password   # 민감한 정보로 변수 처리
  }

  # Linux VM에 대한 비밀번호 인증 설정
  os_profile_linux_config {
    disable_password_authentication = false  # 비밀번호 인증 활성화
  }

  # 가상 머신 생성 후 Docker 설치 및 Docker Hub 이미지 실행
  provisioner "remote-exec" {
    connection {
      type     = "ssh"
      user     = var.admin_username  # 위에서 설정한 사용자 이름
      password = var.admin_password  # 위에서 설정한 비밀번호
      host     = azurerm_public_ip.example.ip_address  # Public IP 주소
      port     = 22
    }

    inline = [
      "sleep 30",  # VM이 완전히 시작되기를 기다림
      "sudo apt-get update",
      "sudo apt-get install -y docker.io",  # Docker 설치
      "sudo systemctl start docker",        # Docker 시작
      "sudo docker pull ksoochoi/fastapiwithnginx:latest",  # Docker Hub에서 이미지 pull
      "sudo docker run -d -p 80:8000 ksoochoi/fastapiwithnginx:latest"  # 이미지 실행
    ]
  }
}

output "public_ip_address" {
  value = azurerm_public_ip.example.ip_address
}