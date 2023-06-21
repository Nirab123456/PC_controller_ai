from AI_Env_Data_2 import Env_data_process
import numpy as np
import pandas as pd


class pandas_data_collection(Env_data_process):
    """convert cpu,memory,wifi,disk used data to pndas dataframe."""
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame()
        self.intarected_unique_name= self.get_unique_process_names(self.interacting_processes)
        self.un_intarected_unique_name= self.get_unique_process_names(self.non_interacting_processes)
        self.inerected_cpu_uses_percent= self.get_cpu_uses_percent(self.interacting_processes)
        self.un_inerected_cpu_uses_percent= self.get_cpu_uses_percent(self.non_interacting_processes)
        self.inerected_memory_uses_percent= self.get_memory_uses_percent(self.interacting_processes)
        self.un_inerected_memory_uses_percent= self.get_memory_uses_percent(self.non_interacting_processes)
        self.inerected_Wi_fi_uses_percent= self.get_Wi_fi_uses_percent(self.interacting_processes)
        self.un_inerected_Wi_fi_uses_percent= self.get_Wi_fi_uses_percent(self.non_interacting_processes)
        self.inerected_disc_uses_percent= self.get_disc_uses_percent(self.interacting_processes)
        self.un_inerected_disc_uses_percent= self.get_disc_uses_percent(self.non_interacting_processes)
