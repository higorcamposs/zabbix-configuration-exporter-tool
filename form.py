from rich.console import Console
from rich.prompt import Prompt

console = Console()

def display_banner():
    banner = """
    =============================================
    ||         Zabbix Config Exporter Tool      ||
    =============================================
    """
    console.print(banner, style="bold red")

def get_zabbix_details():
    display_banner()
    
    zabbix_ip = Prompt.ask("[bold white]Please enter the IP[/bold white]")
    auth_method = Prompt.ask("[bold white]Do you want to use a token or a password for authentication? (token/password)[/bold white]")
    if auth_method == "token":
        api_token = Prompt.ask("[bold white]Please enter your Zabbix API token[/bold white]", password=True).strip()
        username = None
        password = None
    elif auth_method == "password":
        username = Prompt.ask("[bold white]Please enter your username[/bold white]").strip()
        password = Prompt.ask("[bold white]Please enter your password[/bold white]", password=True).strip()
        api_token = None
    else:
        console.print("[bold red]Invalid authentication method. Use 'token' or 'password'.[/bold red]")
        return None

    return {
        'ip': zabbix_ip,
        'auth_method': auth_method,
        'api_token': api_token,
        'username': username,
        'password': password
    }

def get_export_choice():
    console.print("[bold white]What do you want to export?[/bold white]")
    console.print("[bold green]1. Host groups[/bold green]")
    console.print("[bold green]2. Hosts[/bold green]")
    console.print("[bold green]3. Images[/bold green]")
    console.print("[bold green]4. Maps[/bold green]")
    console.print("[bold green]5. Media types[/bold green]")
    console.print("[bold green]6. Templates[/bold green]")
    
    choice = Prompt.ask("[bold white]Enter the number of your choice[/bold white]").strip()
    choices = {
        '1': 'hostgroup',
        '2': 'host',
        '3': 'image',
        '4': 'map',
        '5': 'mediatype',
        '6': 'template'
    }

    if choice not in choices:
        console.print("[bold red]Invalid choice. Please enter a number between 1 and 6.[/bold red]")
        exit(1)

    return choices.get(choice)


