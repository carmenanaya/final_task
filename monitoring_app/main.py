import threading       # For threading operations
import time     # For sleep and timing
import msvcrt  # For detecting key press on Windows
from monitor.monitor import Monitor  # Assuming Alarm is defined in monitor module
from monitor.alarm import create_alarm  # Function to create alarms
from persistence.storage import save_alarms, load_alarms  # Functions to save/load alarms
from utils.logger import setup_logger    # Function to set up logging
from utils.validation import ask_alarm_level    # Function to validate alarm level input


print("Laddar tidigare konfigurerade larm, vänligen vänta.")
alarms = load_alarms()    # Load previously saved alarms
logger = setup_logger()    # Set up logger
logger.info("Programmet startar.")   # Log program start
monitor = Monitor(alarms, logger=logger)  # Initialize monitor with loaded alarms


def main_menu():
    while True:
        monitor.suppress_alarms.set()  # Suppress alarms while in menu
        print("\n-----Huvudmeny-----")
        print("1.Starta övervakning")
        print("2.Lista aktiv övervakning")
        print("3.Skapa larm")
        print("4.Visa larm")
        print("5.Visa övervakningsläge")
        print("6.Avsluta programmet")

        choice = input("Välj ett alternativ (1-6): ").strip()
        '''monitor.suppress_alarms.clear()  # Stop suppressing after input''' # Deleted to avoid alarms during input

        if choice == "1":
            monitor.suppress_alarms.clear()   # Stop suppressing alarms
            start_monitoring()
        elif choice == "2":
            show_status()
            monitor.suppress_alarms.set()  # Added 1 - to avoid alarms during input
        elif choice == "3":
            create_alarm_menu()
            monitor.suppress_alarms.set()  # Added 2 - to avoid alarms during input
        elif choice == "4":
            monitor.suppress_alarms.set()  # Added 3 - to avoid alarms during input
            show_alarms()            
        elif choice == "5":
            monitor.suppress_alarms.set()  # Added 4 - to avoid alarms during input
            start_monitoring_mode()
        elif choice == "6":
            monitor.suppress_alarms.clear()  # Allow final alarms
            print("Avslutar programmet, vänligen vänta...")
            if monitor.running:
                monitor.stop()
                time.sleep(1)
            logger.info("Programmet avslutas av användaren.")
            break
        else:
            print("Ogiltigt val, försök igen.")


def start_monitoring():
    if not monitor.running:
        monitor.start()
        logger.info("Övervakning startad av användaren.")
        print("Övervakning startad.")
    else:
        print("Övervakning är redan igång.")

def show_status():
    if not monitor.running:
        print("Övervakningen är inte igång.")
    else:
        cpu, mem, disk = monitor.get_current_status()
        print(f"CPU-användning: {cpu:.1f}%")
        print(f"Minnesanvändning: {mem[0]:.1f}% ({mem[1]/(1024**3):.1f} GB av {mem[2]/(1024**3):.1f} GB)")
        print(f"Diskanvändning: {disk[0]:.1f}% ({disk[1]/(1024**3):.1f} GB av {disk[2]/(1024**3):.1f} GB)")
    input("Tryck på Enter för att återgå till huvudmenyn.")

def create_alarm_menu():
    print("\n-----Skapa Larm-----")
    print("1.CPU-användning")
    print("2.Minnesanvändning")
    print("3.Diskanvändning")
    print("4.Tillbaka till huvudmenyn")
    choice = input("Välj ett alternativ (1-4): ").strip()

    if choice not in ["1","2","3"]:
        return

    alarm_type = {"1":"cpu","2":"minne","3":"disk"}[choice]
    level = ask_alarm_level()
    if level is None:
        return

    new_alarm = create_alarm(alarm_type, level)
    monitor.add_alarm(new_alarm)
    save_alarms(monitor.alarms)
    logger.info(f"Larm skapat: {alarm_type.upper()} vid {level}%")
    print(f"Larm skapat för {alarm_type.upper()} vid {level}%.")

def show_alarms():
    print("\n-----Konfigurerade Larm-----")   # Display configured alarms
    if not monitor.alarms:
        print("Inga larm är konfigurerade.")
    else:
        sorted_alarms = sorted(monitor.alarms, key=lambda a: (a.type, a.level))  # Sort by type then level
        for a in sorted_alarms:     # Display alarms
            print(f"{a.type.upper()} larm {a.level}% (id: {a.id[:6]})")     # Show first 6 chars of id
    input("Tryck på Enter för att återgå till huvudmenyn.")



def start_monitoring_mode():
    if not monitor.running:
        print("Starta övervakningen först (alternativ 1 i huvudmenyn).")
        return

    print("Övervakningsläge startat. Tryck på Enter för att återgå till menyn.")
    logger.info("Övervakningsläge startat.")

    try:
        while True:
            cpu, mem, disk = monitor.get_current_status()
            print(f"Övervakning aktiv: CPU {cpu:.1f}%, Minne {mem[0]:.1f}%, Disk {disk[0]:.1f}%", end="\r")
            
            # Stop monitoring mode if Enter is pressed
            if msvcrt.kbhit():
                key = msvcrt.getch()
                break

            time.sleep(2)
    except KeyboardInterrupt:
        pass

    print("\nÅtergår till huvudmenyn.")

# Run the main menu
if __name__ == "__main__":
    main_menu()