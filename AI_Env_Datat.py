import psutil
import pynvml
import wmi
import ctypes


class SystemInfo:
    def __init__(self):
        self.personal_system_index = None
        self.interacting_processes = []
        self.non_interacting_processes = []
        self.all_top_processes_names = []
        self.wifi_percent = 0.0

    def get_cpu_info(self):
        """Returns the name of the CPU"""
        w = wmi.WMI()
        cpu = w.Win32_Processor()[0]
        return cpu.Name

    def get_gpu_info(self):
        """Returns the names of every GPU available in the system"""
        w = wmi.WMI()
        gpu_info = []
        for gpu in w.Win32_VideoController():
            gpu_info.append(gpu.Name)
        return gpu_info

    def get_ram_info(self):
        """Returns the frequency and capacity of the RAM"""
        ram_info = {}
        ram_info['frequency'] = psutil.cpu_freq().current
        ram_info['capacity'] = psutil.virtual_memory().total
        return ram_info

    def get_system_info(self):
        """Returns the system info (CPU, GPU, RAM)"""
        if self.personal_system_index is None:
            system_info = {}
            system_info['cpu'] = self.get_cpu_info()
            system_info['gpu'] = self.get_gpu_info()
            system_info['ram'] = self.get_ram_info()
            self.personal_system_index = system_info
        return self.personal_system_index

    def get_gpu_processes(self):
        """Returns the processes running on the GPU"""
        gpu_processes = []
        pynvml.nvmlInit()
        self.device_count = pynvml.nvmlDeviceGetCount()
        if self.device_count >= 0:
            for i in range(self.device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                gpu_processes_info = pynvml.nvmlDeviceGetComputeRunningProcesses(handle)
                for process in gpu_processes_info:
                    try:
                        proc = psutil.Process(process.pid)
                        name = proc.name()
                        gpu_processes.append(name)
                    except psutil.NoSuchProcess:
                        pass
            pynvml.nvmlShutdown()
            return gpu_processes
        else:
            pass

    def is_gpu_available(self):
        """Returns True if a GPU is available"""
        pynvml.nvmlInit()
        self.device_count = pynvml.nvmlDeviceGetCount()
        if self.device_count >= 0:
            return True
        else:
            return False

    def get_top_processes(self, process_list, key):
        """Returns the top 10 processes based on the key"""
        processes = []
        for process in process_list:
            try:
                name = process.info['name']
                value = process.info[key]
                processes.append({'name': name, 'value': value})   
            except (psutil.NoSuchProcess, KeyError):
                pass
        sorted_processes = sorted(processes, key=lambda x: x['value'], reverse=True)
        return [(process['name'], process['value']) for process in sorted_processes[:10] if process['value'] >= 0]

    def get_gpu_usage(self):
        """Returns the GPU usage"""
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        gpu_usage = []

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            gpu_info = pynvml.nvmlDeviceGetUtilizationRates(handle)
            gpu_usage.append({'index': i, 'percentage': gpu_info.gpu})

        pynvml.nvmlShutdown()
        return gpu_usage

    def get_system_usage(self):
        """Returns the CPU, RAM, and GPU usage"""
        cpu_percent = psutil.cpu_percent(interval=1)
        ram_percent = psutil.virtual_memory().percent
        gpu_usage = self.get_gpu_usage()

        if self.is_gpu_available():
            gpu_percentages = [gpu['percentage'] for gpu in gpu_usage]
            return cpu_percent, ram_percent, gpu_percentages
        else:
            return cpu_percent, ram_percent

    def get_top_processes_info(self):
        """Returns the top processes based on CPU, RAM, and GPU usage"""
        if self.is_gpu_available():
            cpu_percent, ram_percent, gpu_percentages = self.get_system_usage()
            
            # Fetch CPU processes
            cpu_processes1 = psutil.process_iter(['name', 'cpu_percent'])

            cpu_processes1 = list(cpu_processes1)  # Convert to list to ensure it is evaluated
            # Fetch RAM processes
            ram_processes = psutil.process_iter(['name', 'memory_percent'])
            
            # Fetch top CPU processes
            top_cpu_processes = self.get_top_processes(cpu_processes1, 'cpu_percent')
            
            # Fetch top RAM processes
            top_ram_processes = self.get_top_processes(ram_processes, 'memory_percent')
            
            # Fetch GPU processes
            gpu_processes = self.get_gpu_processes()[:4]

            self.top_cpu_processes_names = [process[0] for process in top_cpu_processes]
            self.top_ram_processes_names = [process[0] for process in top_ram_processes]
            self.gpu_processes_names = gpu_processes
            self.all_top_processes_names = self.top_cpu_processes_names + self.top_ram_processes_names + self.gpu_processes_names

            return top_cpu_processes, top_ram_processes, gpu_processes
        else:
            cpu_percent, ram_percent = self.get_system_usage()
            cpu_processes = psutil.process_iter(['name', 'cpu_percent'])
            ram_processes = psutil.process_iter(['name', 'memory_percent'])
            top_cpu_processes = self.get_top_processes(cpu_processes, 'cpu_percent')
            top_ram_processes = self.get_top_processes(ram_processes, 'memory_percent')

            self.top_cpu_processes_names = [process[0] for process in top_cpu_processes]
            self.top_ram_processes_names = [process[0] for process in top_ram_processes]
            self.all_top_processes_names = self.top_cpu_processes_names + self.top_ram_processes_names

            return top_cpu_processes, top_ram_processes

    def if_any_common_top(self):
        """Returns the common top processes running on CPU, RAM, and GPU"""
        if self.is_gpu_available():
            top_cpu_processes, top_ram_processes, gpu_processes = self.get_top_processes_info()
            top_cpu_gpu = set([process[0] for process in top_cpu_processes]) & set(gpu_processes)
            top_ram_gpu = set([process[0] for process in top_ram_processes]) & set(gpu_processes)
            top_cpu_ram = set([process[0] for process in top_cpu_processes]) & set([process[0] for process in top_ram_processes])
            return top_cpu_gpu, top_ram_gpu, top_cpu_ram
        else:
            top_cpu_processes, top_ram_processes = self.get_top_processes_info()
            top_cpu_ram = set([process[0] for process in top_cpu_processes]) & set([process[0] for process in top_ram_processes])
            return top_cpu_ram

    def check_user_interaction(self):
        """Returns the processes that are being interacted with by the user and the processes that are not being interacted with"""
        interacting_processes = []
        non_interacting_processes = []
        for process_name in self.all_top_processes_names:
            if self.is_user_interacting(process_name):
                interacting_processes.append(process_name)
            else:
                non_interacting_processes.append(process_name)
        return interacting_processes, non_interacting_processes

    def is_user_interacting(self, process_name):
        """Returns True if the user is interacting with the process"""
        user32 = ctypes.windll.user32
        active_window_handle = user32.GetForegroundWindow()
        active_process_id = ctypes.c_ulong(0)
        user32.GetWindowThreadProcessId(active_window_handle, ctypes.byref(active_process_id))
        active_process = psutil.Process(active_process_id.value)
        return active_process.name() == process_name
    
    def get_current_interaction_results(self):
        """Returns the details of the processes that are being interacted with by the user"""
        interacting_processes_details = []
        interaction_result = self.check_user_interaction()
        self.interacting_processes = interaction_result[0]

        for process_name in self.interacting_processes:
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                if proc.info['name'].lower() == process_name.lower():
                    interacting_processes_details.append(proc.info)

        wifi_info = {'name': 'Wi-Fi', 'cpu_percent': 0.0, 'memory_percent': 0.0, 'wifi_percent': self.wifi_percent}
        interacting_processes_details.append(wifi_info) if self.wifi_percent > 0 else None

        disk_usage = psutil.disk_usage('/')
        disk_info = {'name': 'Disk', 'cpu_percent': 0.0, 'memory_percent': 0.0, 'disk_percent': disk_usage.percent}
        interacting_processes_details.append(disk_info)

        return interacting_processes_details

    def get_current_non_interaction_results(self):
        """Returns the details of the processes that are not being interacted with by the user"""
        non_interacting_processes_details = []
        interaction_result = self.check_user_interaction()
        self.non_interacting_processes = interaction_result[1]

        for process_name in self.non_interacting_processes:
            for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                if proc.info['name'] == process_name:
                    non_interacting_processes_details.append(proc.info)

        wifi_info = {'name': 'Wi-Fi', 'cpu_percent': 0.0, 'memory_percent': 0.0, 'wifi_percent': self.wifi_percent}
        non_interacting_processes_details.append(wifi_info) if self.wifi_percent > 0 else None

        disk_usage = psutil.disk_usage('/')
        disk_info = {'name': 'Disk', 'cpu_percent': 0.0, 'memory_percent': 0.0, 'disk_percent': disk_usage.percent}
        non_interacting_processes_details.append(disk_info)

        return non_interacting_processes_details

    def get_wifi_uses_percent(self, processes):
        """Returns the Wi-Fi usage percentage accumulation"""
        wifi_usage = {name: 0.0 for name in processes}
        for process in processes:
            name = process['name']
            if name in wifi_usage and 'wifi_percent' in process:
                wifi_usage[name] += process['wifi_percent']
        return wifi_usage
