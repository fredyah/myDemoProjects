from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

class ESXiConnection:
    def __init__(self, host, user, passwd, ssl_context=None):
        """
        初始化連接到 ESXi
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.ssl_context = ssl_context or ssl._create_unverified_context()
        self.si = None

    def connect(self):
        """
        連接到 ESXi
        """
        self.si = SmartConnect(
            host=self.host,
            user=self.user,
            pwd=self.passwd,
            sslContext=self.ssl_context
        )
        if self.si:
            print(f"Successfully connected to ESXi at {self.host}.")
        else:
            raise ConnectionError("Failed to connect to ESXi.")

    def disconnect(self):
        """
        斷開與 ESXi 的連接
        """
        if self.si:
            Disconnect(self.si)
            print("Disconnected from ESXi.")
        self.si = None

    def get_content(self):
        """
        獲取 ESXi 的內容對象
        """
        if self.si:
            return self.si.RetrieveContent()
        else:
            raise ConnectionError("Not connected to ESXi.")

class ESXiOperations(ESXiConnection):
    def __init__(self, host, user, passwd, ssl_context=None):
        super().__init__(host, user, passwd, ssl_context)

    def find_vm_by_name(self, vm_name):
        """
        根據名稱查找虛擬機
        """
        content = self.get_content()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        for vm in container.view:
            if vm.name == vm_name:
                container.Destroy()
                return vm
        container.Destroy()
        return None

    def list_powered_on_vms(self):
        """
        列出所有已開機的虛擬機
        """
        content = self.get_content()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        
        powered_on_vms = []
        for vm in container.view:
            if vm.runtime.powerState == "poweredOn":
                powered_on_vms.append(vm.name)
        
        container.Destroy()
        return powered_on_vms



    def power_on_vm(self, vm_name):
        """
        開啟指定虛擬機的電源
        """
        vm = self.find_vm_by_name(vm_name)
        if not vm:
            print(f"VM {vm_name} not found.")
            return

        if vm.runtime.powerState == "poweredOn":
            print(f"{vm.name} is already powered on.")
        else:
            print(f"Powering on {vm.name}...")
            task = vm.PowerOn()
            self.wait_for_task(task)
            print(f"{vm.name} is now powered on.")

    def power_off_vm(self, vm_name):
        """
        關閉指定虛擬機的電源
        """
        vm = self.find_vm_by_name(vm_name)
        if not vm:
            print(f"VM {vm_name} not found.")
            return

        if vm.runtime.powerState == "poweredOff":
            print(f"{vm.name} is already powered off.")
        else:
            print(f"Powering off {vm.name}...")
            task = vm.PowerOff()
            self.wait_for_task(task)
            print(f"{vm.name} is now powered off.")


    def enter_maintenance_mode(self, host_ip):
        """
        將指定主機進入維護模式
        """
        host = self.find_host_by_ip(host_ip)
        if host:
            if host.runtime.inMaintenanceMode:
                print(f"Host with IP {host_ip} is already in maintenance mode.")
            else:
                print(f"Entering maintenance mode for host with IP {host_ip}...")
                task = host.EnterMaintenanceMode_Task(timeout=0)
                self.wait_for_task(task)
                print(f"Host with IP {host_ip} is now in maintenance mode.")
        else:
            print(f"Host with IP {host_ip} not found.")




    def exit_maintenance_mode(self, host_ip):
        """
        將指定主機解除維護模式
        """
        host = self.find_host_by_ip(host_ip)
        if host:
            if not host.runtime.inMaintenanceMode:
                print(f"Host with IP {host_ip} is not in maintenance mode.")
            else:
                print(f"Exiting maintenance mode for host with IP {host_ip}...")
                task = host.ExitMaintenanceMode_Task(timeout=0)
                self.wait_for_task(task)
                print(f"Host with IP {host_ip} has exited maintenance mode.")
        else:
            print(f"Host with IP {host_ip} not found.")




    def shutdown_host(self, host_ip):
        """
        關閉指定主機
        """
        host = self.find_host_by_ip(host_ip)
        if host:
            if host.runtime.inMaintenanceMode:
                print(f"Shutting down host with IP {host_ip}...")
                task = host.ShutdownHost_Task(force=True)
                self.wait_for_task(task)
                print(f"Host with IP {host_ip} is now shut down.")
            else:
                print(f"Host with IP {host_ip} must be in maintenance mode before shutting down.")
        else:
            print(f"Host with IP {host_ip} not found.")


    def find_host_by_ip(self, host_ip):
        """
        根據 IP 地址查找主機，解決單機環境下找不到自己的問題
        """
        if host_ip == self.host:
            # 當連接的是單個主機時，返回其自身
            return self.get_content().rootFolder.childEntity[0].hostFolder.childEntity[0].host[0]
        
        content = self.get_content()
        for datacenter in content.rootFolder.childEntity:
            if hasattr(datacenter, 'hostFolder'):
                for host_folder in datacenter.hostFolder.childEntity:
                    if hasattr(host_folder, 'host'):
                        for host in host_folder.host:
                            if host.summary.managementServerIp == host_ip:
                                return host
        return None



    @staticmethod
    def wait_for_task(task):
        """
        等待任務完成
        """
        while task.info.state == "running":
            pass
        if task.info.state == "success":
            print("Task completed successfully.")
        else:
            print(f"Task failed: {task.info.error}")


