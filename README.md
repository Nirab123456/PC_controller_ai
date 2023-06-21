**Project Name: PC Application Monitoring(mainly for collecting training_dataset)**

README

This project aims to provide a simple solution for monitoring the interaction and non-interaction states of the top 10 applications on your PC using deep learning techniques. The project utilizes the Python programming language and leverages the power of libraries such as psutil, pynvml, wmi, ctypes, and pandas to collect and analyze the data.

**Project Features:**

- **Interaction Monitoring**: The project tracks the interaction status of the top 10 applications running on your PC. It provides real-time updates on the CPU usage, memory usage, disk usage, and Wi-Fi usage of these applications.

- **Non-Interaction Monitoring**: In addition to the interacting applications, the project also captures data from the non-interacting applications. This allows for a comprehensive understanding of the resource utilization on your PC.

- **Data Analysis**: The collected data is stored in pandas DataFrames, providing a structured representation for further analysis. You can easily perform operations on the collected data, such as filtering, aggregating, and visualizing the metrics.

- **Basic Test**: The project includes a basic test suite to ensure the functionality of the monitoring system. This allows you to verify the accuracy and reliability of the collected data.

**Installation:**

To get started with the project, follow the steps below to install the required dependencies:

1. Make sure you have Python installed on your system. You can download Python from the official website (https://www.python.org) and follow the installation instructions for your operating system.

2. Clone the project repository from GitHub:
   ```
   git clone https://github.com/Nirab123456/PC_controller_ai.git
   ```

3. Navigate to the project directory:
   ```
   cd PC_controller_ai
   ```

4. Create a virtual environment (optional but recommended):
   ```
   python -m venv myenv
   ```

5. Activate the virtual environment:
   - For Windows:
     ```
     myenv\Scripts\activate
     ```
   - For Linux/Mac:
     ```
     source myenv/bin/activate
     ```

6. Install the required dependencies from the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

**Usage:**

Once you have installed the dependencies, you can run the project using the provided scripts. Modify the code as per your requirements and execute the main script to start monitoring the PC applications.

1. Open the project in your preferred development environment.

2. Modify the code to customize the monitoring settings if needed.

4. Run the script:
   ```
   python test.py
   ```

5. The application monitoring will start, and you will receive real-time updates on the interaction and non-interaction states of the top 10 applications.

**Contributing:**

Contributions to the project are welcome. If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue on the project repository.


Happy monitoring!

Author: [RIFATUL ISLAM MAJUMDER ]
Email: [rifatulislam212@gmail.com]
