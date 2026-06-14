import json
import os
from datetime import datetime

DATA_FILE = "schedule.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"events": [], "volunteers": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_event():
    data = load_data()
    name = input("Event name (e.g. Food Distribution Drive): ").strip()
    if not name:
        print("Event name can't be empty.")
        return

    date_str = input("Event date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    location = input("Location (e.g. Kidwai Nagar, Kanpur): ").strip()
    time_slot = input("Time slot (e.g. 9 AM - 1 PM): ").strip()

    event = {
        "name": name,
        "date": date_str,
        "location": location,
        "time": time_slot,
        "volunteers": []
    }

    data["events"].append(event)
    save_data(data)
    print(f"\n✅ Event '{name}' added for {date_str}")


def add_volunteer():
    data = load_data()
    name = input("Volunteer name: ").strip()
    if not name:
        print("Name can't be empty.")
        return

    if any(v["name"].lower() == name.lower() for v in data["volunteers"]):
        print(f"'{name}' is already registered.")
        return

    phone = input("Phone number: ").strip()
    data["volunteers"].append({"name": name, "phone": phone})
    save_data(data)
    print(f"\n✅ Volunteer '{name}' registered.")


def list_events():
    data = load_data()
    if not data["events"]:
        print("No events scheduled yet.")
        return

    print(f"\n===== ALL EVENTS ({len(data['events'])} total) =====")
    for i, e in enumerate(data["events"], 1):
        vols = ", ".join(e["volunteers"]) if e["volunteers"] else "None assigned"
        print(f"\n  {i}. {e['name']}")
        print(f"     Date     : {e['date']}")
        print(f"     Time     : {e['time']}")
        print(f"     Location : {e['location']}")
        print(f"     Volunteers: {vols}")


def assign_volunteer():
    data = load_data()
    if not data["events"]:
        print("No events to assign to. Add an event first.")
        return
    if not data["volunteers"]:
        print("No volunteers registered. Add a volunteer first.")
        return

    print("\nEvents:")
    for i, e in enumerate(data["events"], 1):
        print(f"  {i}. {e['name']} — {e['date']} ({e['time']})")

    try:
        event_choice = int(input("\nSelect event number: ").strip())
        event = data["events"][event_choice - 1]
    except (ValueError, IndexError):
        print("Invalid event selection.")
        return

    print("\nVolunteers:")
    for i, v in enumerate(data["volunteers"], 1):
        print(f"  {i}. {v['name']}")

    try:
        vol_choice = int(input("\nSelect volunteer number: ").strip())
        volunteer = data["volunteers"][vol_choice - 1]
    except (ValueError, IndexError):
        print("Invalid volunteer selection.")
        return

    # ── CONFLICT CHECK ──
    conflicts = []
    for e in data["events"]:
        if e["date"] == event["date"] and volunteer["name"] in e["volunteers"] and e["name"] != event["name"]:
            conflicts.append(e)

    if conflicts:
        print(f"\n⚠️  CONFLICT: {volunteer['name']} is already assigned to:")
        for c in conflicts:
            print(f"     - {c['name']} on {c['date']} ({c['time']})")
        confirm = input("\nAssign anyway? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Assignment cancelled.")
            return

    if volunteer["name"] in event["volunteers"]:
        print(f"{volunteer['name']} is already assigned to this event.")
        return

    event["volunteers"].append(volunteer["name"])
    save_data(data)
    print(f"\n✅ {volunteer['name']} assigned to '{event['name']}'")


def check_volunteer_schedule():
    data = load_data()
    if not data["volunteers"]:
        print("No volunteers registered.")
        return

    name = input("Enter volunteer name: ").strip()
    assigned = []

    for e in data["events"]:
        if name in e["volunteers"]:
            assigned.append(e)

    if not assigned:
        print(f"\n{name} has no event assignments.")
        return

    print(f"\n===== SCHEDULE FOR {name} =====")
    for e in sorted(assigned, key=lambda x: x["date"]):
        print(f"  {e['date']} | {e['name']} | {e['time']} | {e['location']}")

    dates = [e["date"] for e in assigned]
    duplicates = set([d for d in dates if dates.count(d) > 1])
    if duplicates:
        print(f"\n⚠️  Warning: {name} has multiple events on: {', '.join(duplicates)}")


def main():
    menu = {
        "1": ("Add new event", add_event),
        "2": ("Register new volunteer", add_volunteer),
        "3": ("Assign volunteer to event (with conflict check)", assign_volunteer),
        "4": ("List all events", list_events),
        "5": ("Check a volunteer's schedule", check_volunteer_schedule),
        "6": ("Exit", None),
    }

    print("=========================================")
    print("   NAYEPANKH FOUNDATION")
    print("   Volunteer-Event Scheduler")
    print("=========================================")

    while True:
        print("\nWhat would you like to do?")
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        choice = input("\nEnter option: ").strip()

        if choice == "6":
            print("Goodbye.")
            break
        elif choice in menu:
            menu[choice][1]()
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
