vSphere_login_dataMsg = {
  vs_username       = "administrator@vsphere.test"
  vs_passwd         = "*********"
  vs_vsphere_server = "192.168.1.7"
}

vSphere_dataCenter_Name = "Datacenter"

vSphere_DataStore_Name = "SAN_Datastore"

vSphere_Network_Name = "VM Network"

vSphere_VM_template_Name = "u24-server-template"

num_Worker_Nodes = 2

vSphere_VM_Resources_Data = {
  K8sMasterNode = {
    vmName = "fred-K8S-MasterNode"
    vmESXI_Host_IP = "192.168.1.14"
    vmDataStore_ID = "datastore-1009"
    vmCPU_Num = 4
    vmMemorySize = 8192
    vmFireWareType = "efi"
    vmDisk = {
  #    vmDisKLabel = "${var.vmName}-disk0"
      vmDiskSize = 64
      vmDiskEagerlyScrub = false
      vmDiskThinProvisioned = true
    }
  }
  K8sWorKNode = {
    vmName = "fred-K8S-WorkNode"
    vmESXI_Host_IP = "192.168.1.19"
    vmDataStore_ID = "datastore-1011"
    vmCPU_Num = 4
    vmMemorySize = 8192
    vmFireWareType = "efi"
    vmDisk = {
 #     vmDisKLabel = "${var.vmName}-disk0"
      vmDiskSize = 90
      vmDiskEagerlyScrub = false
      vmDiskThinProvisioned = true
    }
  }
}



##  terraform plan -var-file="vars.tfvars"
