import sys
from dotenv import load_dotenv

from assistant.tracker import InternshipTracker
from assistant.utils import print_header, get_user_input, print_success, print_error, print_info, Colors
from assistant.engine import process_user_query

def run_tracker_menu() -> None:
    tracker = InternshipTracker()
    
    while True:
        print_header("📊 INTERNSHIP TRACKER", Colors.BLUE)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Track a New Application")
        print(f"{Colors.BOLD}2.{Colors.ENDC} View Tracked Applications")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Update Application Status")
        print(f"{Colors.BOLD}4.{Colors.ENDC} Back to Main Menu\n")
        
        choice = get_user_input("Select an option")
        
        if choice == '1':
            company = get_user_input("Company Name")
            role = get_user_input("Role")
            status = get_user_input("Status (e.g., applied, interview, rejected) [default: applied]")
            
            if company and role:
                status_to_save = status if status.strip() else "applied"
                tracker.add_application(company, role, status_to_save)
                print_success(f"Added {company} - {role} [{status_to_save.upper()}]")
                
        elif choice == '2':
            print_header("📋 YOUR APPLICATIONS", Colors.CYAN)
            apps = tracker.get_all_applications()
            if not apps:
                print_info("No applications tracked yet. Keep applying!")
            else:
                for i, app in enumerate(apps, 1):
                    # Color code statuses intelligently
                    status = app['status'].lower()
                    color = Colors.GREEN if status == 'offer' else (Colors.WARNING if status == 'interview' else (Colors.FAIL if status == 'rejected' else Colors.CYAN))
                    print(f"{Colors.BOLD}{i}.{Colors.ENDC} {app['company']} - {app['role']} [{color}{app['status'].upper()}{Colors.ENDC}]")
            
        elif choice == '3':
            apps = tracker.get_all_applications()
            if not apps:
                print_info("No applications to update.")
                continue
                
            for i, app in enumerate(apps, 1):
                print(f"{i}. {app['company']} ({app['status']})")
                
            try:
                index = int(get_user_input("\nEnter the application number to update")) - 1
                new_status = get_user_input("Enter new status")
                if new_status:
                    if tracker.update_application_status(index, new_status):
                        print_success("Status updated successfully.")
                    else:
                        print_error("Invalid application number.")
            except ValueError:
                print_error("Please enter a valid number.")
                
        elif choice == '4':
            break
        else:
            print_error("Invalid choice. Please select an option from 1 to 4.")

def main() -> None:
    load_dotenv()
    
    print_header("🚀 AI PRODUCTIVITY & INTERNSHIP ASSISTANT", Colors.HEADER)
    print_info("Welcome! I am your AI-powered career mentor.\n")
    
    print(f"{Colors.BOLD}Options:{Colors.ENDC}")
    print(" 🔹 Type a natural request (e.g., 'Help me draft an email to Google')")
    print(" 🔹 Type 'tracker' to manage your applications")
    print(" 🔹 Type 'exit' to quit\n")
    
    while True:
        query = get_user_input("How can I help you today?")
        
        if not query:
            continue
            
        normalized_query = query.lower()
        if normalized_query in ['exit', 'quit']:
            print_success("Goodbye! Best of luck with your career goals.")
            sys.exit(0)
            
        elif normalized_query == 'tracker':
            run_tracker_menu()
            
        else:
            process_user_query(query)

if __name__ == "__main__":
    import os
    # Enable ANSI escape codes natively on modern Windows Terminal
    if os.name == 'nt':
        os.system("")
    main()
