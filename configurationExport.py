import os
import re
from pyzabbix import ZabbixAPI
import urllib3
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Prompt
from form import get_export_choice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

def get_zabbix_api(url):
    zapi = ZabbixAPI(url)
    zapi.session.verify = False
    zapi.timeout = 5.1
    return zapi

def connect_with_token(zapi, api_token):
    try:
        zapi.login(api_token=api_token)
        if zapi.host.get(limit=1):
            return True
        else:
            return False
    except Exception:
        return False

def connect_with_password(zapi, username, password):
    try:
        zapi.login(user=username, password=password)
        if zapi.host.get(limit=1):
            return True
        else:
            return False
    except Exception:
        return False

def sanitize_filename(name):
    return re.sub(r'[^A-Za-z0-9]+', '_', name)

def get_item_ids(zapi, export_type):
    method = f"{export_type}.get"
    response = zapi.do_request(method, {"output": ["id", "name"]})
    return [(item['groupid'] if export_type == 'hostgroup' else
             item['hostid'] if export_type == 'host' else
             item['imageid'] if export_type == 'image' else
             item['sysmapid'] if export_type == 'map' else
             item['mediatypeid'] if export_type == 'mediatype' else
             item['templateid'], item['name']) for item in response['result']]

def export_data(zapi, destination_directory, export_format, export_type):
    console.print(f"[bold white]Exporting {export_type}s to {destination_directory} in {export_format.upper()} format...[/bold white]")
    
    items = get_item_ids(zapi, export_type)
    if not items:
        console.print(f"[bold red]No {export_type}s found.[/bold red]")
        return

    export_param = {
        'hostgroup': 'groups',
        'host': 'hosts',
        'image': 'images',
        'map': 'maps',
        'mediatype': 'mediaTypes',
        'template': 'templates'
    }.get(export_type)

    export_options = {export_param: [item[0] for item in items]}
    total_items = len(items)
    
    console.print(f"\n[bold yellow]Total of {export_type}s in the queue: {total_items}[/bold yellow]")
    with Progress(
        TextColumn("[bold green]Exporting...[/bold green]"),
        BarColumn(bar_width=None, style="red", complete_style="green"),
        TextColumn("[white]{task.percentage:>3.1f}%[/white]"),
        TimeElapsedColumn()
    ) as progress:
        task = progress.add_task("[green]Exporting...", total=total_items)
        
        for i, (item_id, item_name) in enumerate(items, start=1):
            config = zapi.configuration.export(
                format=export_format,
                options={export_param: [item_id]},
            )
            sanitized_name = sanitize_filename(item_name)
            write_export(f"{item_id}_{sanitized_name}", config, export_format, destination_directory)

            progress.update(task, advance=1)

    console.print("[bold green]\nExport completed.[/bold green]")

def write_export(name, config, export_format, destination_directory):
    if config is not None:
        with open(f"{destination_directory}/{name}.{export_format}", "w", encoding='utf-8') as f:
            f.write(config)

def main(details):
    https_url = f"https://{details['ip']}"
    http_url = f"http://{details['ip']}"

    zapi = get_zabbix_api(https_url)
    connected = False

    if details['auth_method'] == "token":
        console.print("[bold white]Trying HTTPS connection...[/bold white]")
        connected = connect_with_token(zapi, details['api_token'])
        if not connected:
            console.print("[bold white]Trying HTTP connection...[/bold white]")
            zapi = get_zabbix_api(http_url)
            connected = connect_with_token(zapi, details['api_token'])
    elif details['auth_method'] == "password":
        console.print("[bold white]Trying HTTPS connection...[/bold white]")
        connected = connect_with_password(zapi, details['username'], details['password'])
        if not connected:
            console.print("[bold white]Trying HTTP connection...[/bold white]")
            zapi = get_zabbix_api(http_url)
            connected = connect_with_password(zapi, details['username'], details['password'])

    if connected:
        console.print(f"[bold green]\nSuccessfully connected to the API: {zapi.api_version()}\n[/bold green]")
        
        export_type = get_export_choice()
        
        destination_directory = Prompt.ask("[bold white]Please enter the directory to save the exports[/bold white]").strip()
        os.makedirs(destination_directory, exist_ok=True)
        
        export_format = Prompt.ask("[bold white]Please enter the export format (yaml, xml, json)[/bold white]")
        if export_format not in ['yaml', 'xml', 'json']:
            console.print("[bold red]Invalid choice.[/bold red]")
            exit(1)
        export_data(zapi, destination_directory, export_format, export_type)
    else:
        console.print("[bold red]Failed to connect to the Zabbix API using both HTTPS and HTTP. Unable to export data.[/bold red]")

