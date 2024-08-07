# Zabbix Configuration Exporter Tool
---
> **📢 If you have any considerations, suggestions, or questions, feel free to contact me! I am available to help.**
---
The `Zabbix Configuration Exporter Tool` is a command-line utility designed to export various configurations from a Zabbix server.

### How it works

1. **Prompt for details**: The tool prompts the user to enter the Zabbix IP, authentication method, and credentials.
2. **Export choice**: Users select what type of configuration they want to export.
3. **Specify directory and format**: Users specify the directory where the exports will be saved and choose the export format.
4. **Export process**: The tool connects to the Zabbix API, retrieves the selected configurations, and exports them to the specified directory. A progress bar shows the export progress.

### Requirements
- Python 3.6 or higher
- `pyzabbix` library
- `rich` library

### Installation
To install the necessary libraries, run:
```bash
pip3 install pyzabbix rich
```

### Usage
To run the tool, execute:
```bash
python3 main.py
```
