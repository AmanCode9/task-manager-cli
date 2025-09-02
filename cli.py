from tasks import TaskManager
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

def input_date(prompt):
    s = input(prompt).strip()
    if not s:
        return None
    try:
        datetime.strptime(s, DATE_FORMAT)
        return s
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return input_date(prompt)

def print_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    print(f"{'ID':<4} {'Title':<30} {'Due':<12} {'Status':<10}")
    print("-"*60)
    for t in tasks:
        due = t.due_date or "-"
        print(f"{t.id:<4} {t.title[:28]:<30} {due:<12} {t.status:<10}")

def main():
    mgr = TaskManager()
    while True:
        print("\n1) Add  2) View  3) Complete  4) Delete  5) Search  6) Edit  7) Quit")
        choice = input("Choose: ").strip()
        if choice=="1":
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            due = input_date("Due (YYYY-MM-DD) or empty: ")
            task = mgr.add_task(title, desc, due)
            print("Added task id:", task.id)
        elif choice=="2":
            tasks = mgr.get_all()
            print_tasks(tasks)
        elif choice=="3":
            try:
                id_ = int(input("Task ID to mark complete: "))
            except ValueError:
                print("Enter a valid integer ID.")
                continue
            if mgr.mark_complete(id_):
                print("Marked complete.")
            else:
                print("Not found.")
        elif choice=="4":
            try:
                id_ = int(input("Task ID to delete: "))
            except ValueError:
                print("Enter a valid integer ID.")
                continue
            if mgr.delete(id_):
                print("Deleted.")
            else:
                print("Not found.")
        elif choice=="5":
            keyword = input("Keyword: ").strip()
            res = mgr.search(keyword)
            print_tasks(res)
        elif choice=="6":
            try:
                id_ = int(input("Task ID to edit: "))
            except ValueError:
                print("Enter a valid integer ID.")
                continue
            t = mgr.find(id_)
            if not t:
                print("Not found.")
                continue
            title = input(f"Title [{t.title}]: ").strip()
            desc = input(f"Description [{t.description}]: ").strip()
            due = input_date(f"Due [{t.due_date or ''}]: ")
            mgr.update(id_, title or None, desc or None, due)
            print("Updated.")
        elif choice=="7":
            print("Bye")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
