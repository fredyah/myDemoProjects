variable "vSphere_login_dataMsg" {
  description = "vSphere login data Message ( username, passwd, Host )"
  type        = object({
    vs_username       = string
    vs_passwd         = string
    vs_vsphere_server = string
  })
  default     = {
    vs_username       = "Your Username"
    vs_passwd         = "Your Passwords"
    vs_vsphere_server = "Your vSphere Server UrL"
  }
}

variable "vSphere_dataCenter_Name" {
  description = "vSphere DataCenter Name"
  type = string
  default = "Your DataCenter Name"
}

variable "vSphere_DataStore_Name" {
  description = "vSphere DataStore Name ( SAN, Nas or Ohters... )"
  type = string
  default = "Your vSphere DataStore Name"
}

variable "vSphere_Network_Name" {
  description = "vSphere Network Name"
  type = string
  default = "Your vSphere Network Name"
}

variable "vSphere_VM_template_Name" {
  description = "vSphere VM template Name"
  type = string
  default = "Your vShpere VM template Name"
}

variable "num_Worker_Nodes" {
  description = "K8S Worker Nodes number"
  type = number
  default = 2
}


variable "vSphere_VM_Resources_Data" {
  description = "vSphere VM create resource Data ( vmName, vmFirmwareType, vmCPU_Num, vmMemorySize, vmDiskSize... )"
  type = map(object({
    vmName = string
    vmESXI_Host_IP = string
    vmDataStore_ID = string
    vmCPU_Num = number
    vmMemorySize = number
    vmFireWareType = string  ## linux → "efi"
    vmDisk = object({
  #    vmDisKLabel = string
      vmDiskSize = number
      vmDiskEagerlyScrub = bool
      vmDiskThinProvisioned = bool
    })
  }))
  default = {
    K8sMasterNode = {
      vmName = "Your New Ubuntu24 VM Name"
      vmESXI_Host_IP = "ESXI Host IP / Name"
      vmDataStore_ID = "datastore-1009"
      vmCPU_Num = 4
      vmMemorySize = 8192
      vmFireWareType = "efi"
      vmDisk = {
  #      vmDisKLabel = "${var.vmName}-disk0"
        vmDiskSize = 64
        vmDiskEagerlyScrub = false
        vmDiskThinProvisioned = true
      }
    }
    K8sWorKNode = {
      vmName = "Your New Ubuntu24 VM Name"
      vmESXI_Host_IP = "ESXI Host IP / Name"
      vmDataStore_ID = "datastore-1009"
      vmCPU_Num = 4
      vmMemorySize = 8192
      vmFireWareType = "efi"
      vmDisk = {
  #      vmDisKLabel = "${var.vmName}-disk0"
        vmDiskSize = 64
        vmDiskEagerlyScrub = false
        vmDiskThinProvisioned = true
      }
    }
  }
}