from datetime import date

from app.analytics.productivity_analyzer import ProductivityAnalyzer
from app.services.report_service import ReportService
from app.services.task_service import TaskService


def display_menu() -> None:
    print("\n" + "=" * 45)
    print("             FLOWPILOT")
    print("    Intelligent Productivity Analyzer")
    print("=" * 45)
    print("1. Create a task")
    print("2. View all tasks")
    print("3. Mark a task as completed")
    print("4. Update actual hours")
    print("5. Delete a task")
    print("6. View productivity report")
    print("7. Export reports to CSV")
    print("8. Exit")
    print("=" * 45)


def display_tasks(task_service: TaskService) -> None:
    tasks = task_service.get_all_tasks()

    if not tasks:
        print("\nNo tasks found. Create your first task!")
        return

    print("\nYOUR TASKS")
    print("-" * 70)

    for index, task in enumerate(tasks, start=1):
        status = "Completed" if task.completed else "Pending"

        print(f"\n{index}. {task.title}")
        print(f"   ID: {task.task_id}")
        print(f"   Priority: {task.priority.title()}")
        print(f"   Status: {status}")
        print(f"   Deadline: {task.deadline or 'Not set'}")
        print(f"   Estimated hours: {task.estimated_hours}")
        print(f"   Actual hours: {task.actual_hours}")

        if task.description:
            print(f"   Description: {task.description}")

    print("-" * 70)


def select_task(task_service: TaskService):
    tasks = task_service.get_all_tasks()

    if not tasks:
        print("\nNo tasks available.")
        return None

    display_tasks(task_service)

    task_id = input(
        "\nEnter the task ID shown above: "
    ).strip()

    try:
        return task_service.get_task_by_id(task_id)
    except ValueError:
        print("Task not found. Please check the task ID.")
        return None


def create_task(task_service: TaskService) -> None:
    print("\nCREATE A TASK")

    title = input("Task title: ").strip()
    description = input("Description (optional): ").strip()

    priority = input(
        "Priority (low/medium/high, default medium): "
    ).strip().lower() or "medium"

    deadline = input(
        "Deadline YYYY-MM-DD (optional): "
    ).strip() or None

    estimated_input = input(
        "Estimated hours (default 0): "
    ).strip() or "0"

    estimated_hours = float(estimated_input)

    task = task_service.create_task(
        title=title,
        description=description,
        priority=priority,
        deadline=deadline,
        estimated_hours=estimated_hours,
    )

    print(f"\nTask created successfully!")
    print(f"Task ID: {task.task_id}")


def complete_task(task_service: TaskService) -> None:
    task = select_task(task_service)

    if task is None:
        return

    task_service.complete_task(task.task_id)
    print(f"\n'{task.title}' marked as completed!")


def update_actual_hours(task_service: TaskService) -> None:
    task = select_task(task_service)

    if task is None:
        return

    hours = float(input("Enter total actual hours spent: ").strip())

    task_service.update_task(
        task.task_id,
        actual_hours=hours,
    )

    print(f"\nActual hours updated for '{task.title}'.")


def delete_task(task_service: TaskService) -> None:
    task = select_task(task_service)

    if task is None:
        return

    confirmation = input(
        f"Delete '{task.title}'? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        task_service.delete_task(task.task_id)
        print("Task deleted successfully.")
    else:
        print("Deletion cancelled.")


def display_productivity_report(task_service: TaskService) -> None:
    tasks = task_service.get_all_tasks()
    analyzer = ProductivityAnalyzer(tasks)
    report = analyzer.generate_report()

    print("\nPRODUCTIVITY REPORT")
    print("-" * 45)

    labels = {
        "total_tasks": "Total tasks",
        "completed_tasks": "Completed tasks",
        "pending_tasks": "Pending tasks",
        "completion_rate_percent": "Completion rate (%)",
        "overdue_tasks": "Overdue pending tasks",
        "estimated_hours": "Total estimated hours",
        "actual_hours": "Total actual hours",
        "time_variance_hours": "Time variance (hours)",
        "time_efficiency_percent": "Time efficiency (%)",
    }

    for key, label in labels.items():
        value = report[key]

        if value is None:
            value = "N/A"

        print(f"{label}: {value}")

    print("\nTasks by priority:")

    for priority, count in analyzer.tasks_by_priority().items():
        print(f"  {priority.title()}: {count}")

    print("-" * 45)


def export_reports(task_service: TaskService) -> None:
    tasks = task_service.get_all_tasks()
    analyzer = ProductivityAnalyzer(tasks)
    report_service = ReportService()

    tasks_path = report_service.export_tasks_to_csv(tasks)

    report_path = report_service.export_productivity_report(
        analyzer.generate_report()
    )

    print("\nReports exported successfully!")
    print(f"Tasks report: {tasks_path}")
    print(f"Productivity report: {report_path}")


def main() -> None:
    task_service = TaskService()

    print("\nWelcome to FlowPilot!")
    print(f"Today: {date.today().isoformat()}")
    print(f"Loaded {len(task_service.get_all_tasks())} saved task(s).")

    actions = {
        "1": create_task,
        "2": display_tasks,
        "3": complete_task,
        "4": update_actual_hours,
        "5": delete_task,
        "6": display_productivity_report,
        "7": export_reports,
    }

    while True:
        display_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "8":
            print("\nYour tasks are saved. Goodbye!")
            break

        action = actions.get(choice)

        if action is None:
            print("\nInvalid choice. Please enter a number from 1 to 8.")
            continue

        try:
            action(task_service)
        except ValueError as error:
            print(f"\nInvalid input: {error}")
        except OSError as error:
            print(f"\nFile operation failed: {error}")


if __name__ == "__main__":
    main()
