import java.util.Scanner; // Importing Scanner class from java.util package

public class InputOutputExample {
    public static void main(String[] args) {
        // Creating a Scanner object
        Scanner scanner = new Scanner(System.in);

        // Prompting user for input
        System.out.print("Enter your name: ");

        // Reading input from the user
        String name = scanner.nextLine();

        // Displaying the input back to the user
        System.out.println("Hello, " + name + "!");

        // Closing the Scanner object
        scanner.close();
    }
}
