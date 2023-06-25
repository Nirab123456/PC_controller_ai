from AI_Env_Datat import SystemInfo

class Env_data_process(SystemInfo):
    def __init__(self):
        """Initializes the data for the current state"""
        super().__init__()
        self.system_info = None
        self.gpu_processes = None
        self.all_interacting_processes = None
        self.interacting_processes = None
        self.non_interacting_processes = None
        self.update_data()

    def update_data(self):
        """Updates the data for the current state"""
        self.system_info = self.get_system_info()
        self.gpu_processes = self.get_gpu_processes()
        self.all_interacting_processes = self.get_top_processes_info()
        self.interacting_processes = self.get_current_interaction_results() or []  # Assign an empty list if None
        self.non_interacting_processes = self.get_current_non_interaction_results()

    def get_unique_process_names(self, processes):
        """Returns the unique process names"""
        if processes is None:
            return set()
        unique_names = set()
        if isinstance(processes, dict):
            processes = processes.values()  # Convert dictionary values to a list of processes
        for process in processes:
            unique_names.add(process['name'])
        return unique_names



    def get_cpu_uses_percent(self, processes):
        """Returns the CPU usage percentage accumulation of each process"""
        process_names = self.get_unique_process_names(processes)
        cpu_usage = {name: 0.0 for name in process_names}
        for process in processes:
            name = process['name']
            if name in process_names:
                cpu_usage[name] += process['cpu_percent']
        return cpu_usage
    
    def get_disc_uses_percent(self, processes):
        """Returns the disk usage percentage accumulation of each process"""
        process_names = self.get_unique_process_names(processes)
        disc_usage = {name: 0.0 for name in process_names}
        for process in processes:
            name = process['name']
            if name in process_names and 'disc_percent' in process:
                disc_usage[name] += process['disc_percent']
        return disc_usage


    def get_memory_uses_percent(self, processes):
        """Returns the memory usage percentage accumulation of each process"""
        process_names = self.get_unique_process_names(processes)
        memory_usage = {name: 0.0 for name in process_names}
        for process in processes:
            name = process['name']
            if name in process_names:
                memory_usage[name] += process['memory_percent']
        return memory_usage
    
    def get_Wi_fi_uses_percent(self, processes):
        """Returns the Wi-Fi usage percentage accumulation of each process"""
        process_names = self.get_unique_process_names(processes)
        Wi_fi_usage = {name: 0.0 for name in process_names}
        for process in processes:
            name = process['name']
            if name in process_names:
                Wi_fi_usage[name] += process.get('Wi_fi_percent', 0.0)
        return Wi_fi_usage

