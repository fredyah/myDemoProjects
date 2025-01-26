provider "vsphere" {
  user           = var.vSphere_login_dataMsg["vs_username"]
  password       = var.vSphere_login_dataMsg["vs_passwd"]
  vsphere_server = var.vSphere_login_dataMsg["vs_vsphere_server"]
  allow_unverified_ssl = true
}

data "vsphere_datacenter" "dc" {
  name = var.vSphere_dataCenter_Name
}

data "vsphere_host" "host" {
  for_each = { for vm_key, vm_data in var.vSphere_VM_Resources_Data : 
    vm_data.vmESXI_Host_IP => vm_data }
  name = each.key
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_datastore" "datastore" {
  name = var.vSphere_DataStore_Name
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_network" "network" {
  name = var.vSphere_Network_Name
  datacenter_id = data.vsphere_datacenter.dc.id
}

data "vsphere_virtual_machine" "template" {
  name = var.vSphere_VM_template_Name
  datacenter_id = data.vsphere_datacenter.dc.id
}


resource "vsphere_virtual_machine" "kubernetes_master_node" {
  name = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmName
  resource_pool_id = data.vsphere_host.host[var.vSphere_VM_Resources_Data["K8sMasterNode"].vmESXI_Host_IP].resource_pool_id
  datastore_id = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmDataStore_ID

  num_cpus = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmCPU_Num
  memory = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmMemorySize
  firmware = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmFireWareType
  guest_id = data.vsphere_virtual_machine.template.guest_id
  scsi_type = data.vsphere_virtual_machine.template.scsi_type

  network_interface {
    network_id      = data.vsphere_network.network.id
    adapter_type    = data.vsphere_virtual_machine.template.network_interface_types[0]
    # connected       = true
    # start_connected = true
  }

  disk {
    label            = "${var.vSphere_VM_Resources_Data["K8sMasterNode"].vmName}-disk0"
    size             = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmDisk.vmDiskSize
    eagerly_scrub    = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmDisk.vmDiskEagerlyScrub
    thin_provisioned = var.vSphere_VM_Resources_Data["K8sMasterNode"].vmDisk.vmDiskThinProvisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template.id
  }
}


resource "vsphere_virtual_machine" "kubernetes_worker_node" {
  for_each = { for i in range(var.num_Worker_Nodes) :
    "K8sWorkNode-${i+1}" => var.vSphere_VM_Resources_Data["K8sWorKNode"] }
  name = "${each.value.vmName}-${each.key}"
  resource_pool_id = data.vsphere_host.host[each.value.vmESXI_Host_IP].resource_pool_id
  datastore_id = each.value.vmDataStore_ID

  num_cpus = each.value.vmCPU_Num
  memory = each.value.vmMemorySize
  firmware = each.value.vmFireWareType
  guest_id = data.vsphere_virtual_machine.template.guest_id
  scsi_type = data.vsphere_virtual_machine.template.scsi_type

  network_interface {
    network_id      = data.vsphere_network.network.id
    adapter_type    = data.vsphere_virtual_machine.template.network_interface_types[0]
    # connected       = true
    # start_connected = true
  }

  disk {
    label            = "${each.value.vmName}-disk0"
    size             = each.value.vmDisk.vmDiskSize
    eagerly_scrub    = each.value.vmDisk.vmDiskEagerlyScrub
    thin_provisioned = each.value.vmDisk.vmDiskThinProvisioned
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template.id

    # customize {
    #   linux_options {
    #     host_name = "fred-ubuntu-2401"
    #     domain    = ""
    #   }

    #   network_interface {
    #     ipv4_address = "192.168.1.81"
    #     ipv4_netmask = 24
    #   }

    #   ipv4_gateway = "192.168.1.254"
    # }
  }
}



output "Kubernetes_Master_node_VM_Info" {
  value = {
    name = vsphere_virtual_machine.kubernetes_master_node.name
    ip = vsphere_virtual_machine.kubernetes_master_node.network_interface[0]
    cpu_number = "${vsphere_virtual_machine.kubernetes_master_node.num_cpus} cores"
    memory_size = "${vsphere_virtual_machine.kubernetes_master_node.memory / 1000} GB"
  }
}





# Get-Datastore | Select Name, ID

# Name            Id
# ----            --
# datastore1 (6)  Datastore-datastore-1010
# SAN_Datastore_2 Datastore-datastore-1011
# datastore1 (8)  Datastore-datastore-1028
# datastore1 (7)  Datastore-datastore-1038
# datastore1 (5)  Datastore-datastore-3521
# datastore1      Datastore-datastore-1052
# SAN_Datastore   Datastore-datastore-1009
# datastore1 (4)  Datastore-datastore-3517
# NAS             Datastore-datastore-1012