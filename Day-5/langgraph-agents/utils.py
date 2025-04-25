def print_welcome_banner():
    """Print a flashy welcome banner for Agent 01"""
    import os
    import time
    
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # ANSI color codes
    class Colors:
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    
    # Banner
    banner = f"""
    {Colors.BOLD}{Colors.BLUE}  █████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██████╗  ██╗{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝   ██╔═████╗███║{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║      ██║██╔██║╚██║{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║      ████╔╝██║ ██║{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║      ╚██████╔╝ ██║{Colors.END}
    {Colors.BOLD}{Colors.BLUE} ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═════╝  ╚═╝{Colors.END}
    """
    
    # Print banner with a typing effect
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.1)  # Adjust for faster/slower typing effect
    
    # Print the divider
    divider = f"{Colors.YELLOW}{'═' * 70}{Colors.END}"
    print(divider)
    
    # Print welcome message
    welcome_message = [
        f"{Colors.BOLD}{Colors.GREEN}  Welcome to the ProtonX Agent 01 Class{Colors.END}",
        f"{Colors.CYAN}  Course: {Colors.UNDERLINE}https://protonx.coursemind.io/courses/67d0ef8beaa2b5001290ff7b/info{Colors.END}",
        f"{Colors.PURPLE}  © ProtonX{Colors.END}",
        "",
        f"{Colors.YELLOW}  [+] {Colors.END}{Colors.BOLD}Product Information{Colors.END} - Ask about our products",
        f"{Colors.YELLOW}  [+] {Colors.END}{Colors.BOLD}Shop Information{Colors.END} - Hours, locations, and policies",
        f"{Colors.YELLOW}  [+] {Colors.END}Type {Colors.RED}'exit'{Colors.END} to quit the conversation"
    ]
    
    # Print the welcome message with a typing effect
    for line in welcome_message:
        print(line)
        time.sleep(0.1)
    
    print(divider)
    print()
    print(f"{Colors.GREEN}Starting session...{Colors.END}")
    time.sleep(1)
    print(f"{Colors.GREEN}Agent 01 is ready to assist you!{Colors.END}")
    print()