import java.util.ArrayList;
import java.util.Scanner;
import java.util.UUID;
import java.util.Date;

public class TaskManager {
    public static class Task {
        private String id;
        private String name;
        private Date createdAt;
        private boolean isCompleted;

        public Task(String name) {
            this.id = UUID.randomUUID().toString();
            this.name = name;
            this.createdAt = new Date();
            this.isCompleted = false;
        }

        public String getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public Date getCreatedAt() {
            return createdAt;
        }

        public boolean isCompleted() {
            return isCompleted;
        }

        public void completeTask() {
            this.isCompleted = true;
        }

        @Override
        public String toString() {
            return "Task{" +
                   "id='" + id + '\'' +
                   ", name='" + name + '\'' +
                   ", createdAt=" + createdAt +
                   ", isCompleted=" + isCompleted +
                   '}';
        }
    }

    private ArrayList<Task> tasks;

    public TaskManager() {
        tasks = new ArrayList<>();
    }

    public void addTask(String taskName) {
        Task newTask = new Task(taskName);
        tasks.add(newTask);
        System.out.println("Added task: " + newTask);
    }

    public void completeTask(String taskId) {
        for (Task task : tasks) {
            if (task.getId().equals(taskId)) {
                task.completeTask();
                System.out.println("Completed task: " + task);
                return;
            }
        }
        System.out.println("Task with ID " + taskId + " not found.");
    }

    public void displayTasks() {
        if (tasks.isEmpty()) {
            System.out.println("No tasks to display.");
            return;
        }
        for (Task task : tasks) {
            System.out.println(task);
        }
    }

    public static void main(String[] args) {
        TaskManager manager = new TaskManager();
        Scanner scanner = new Scanner(System.in);

        while (true) {
            System.out.println("1. Add Task");
            System.out.println("2. Complete Task");
            System.out.println("3. Display Tasks");
            System.out.println("4. Exit");
            System.out.print("Choose an option: ");

            int choice = scanner.nextInt();
            scanner.nextLine(); // Consume newline left-over

            switch (choice) {
                case 1:
                    System.out.print("Enter task name: ");
                    String taskName = scanner.nextLine();
                    manager.addTask(taskName);
                    break;
                case 2:
                    System.out.print("Enter task ID to complete: ");
                    String taskId = scanner.nextLine();
                    manager.completeTask(taskId);
                    break;
                case 3:
                    manager.displayTasks();
                    break;
                case 4:
                    System.out.println("Exiting...");
                    System.exit(0);
                    break;
                default:
                    System.out.println("Invalid choice. Please select again.");
            }
        }
    }
}
