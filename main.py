from form import get_zabbix_details
from configurationExport import main as export_main

def main():
    details = get_zabbix_details()
    if details:
        export_main(details)

if __name__ == "__main__":
    main()

