import java.util.ArrayList;
import java.util.Random;
import java.time.LocalDate;

public class SampleProgram {

    public static void main(String[] args) {
        // Create an instance of Random
        Random random = new Random();

        // Generate a random number between 0 and 100
        int randomNumber = random.nextInt(101);
        System.out.println("Random Number: " + randomNumber);

        // Create an ArrayList and add some elements
        ArrayList<String> list = new ArrayList<>();
        list.add("Apple");
        list.add("Banana");
        list.add("Cherry");
        System.out.println("List of Fruits: " + list);

        // Get current date
        LocalDate currentDate = LocalDate.now();
        System.out.println("Today's Date: " + currentDate);

        // Display a random fruit from the list
        String randomFruit = list.get(random.nextInt(list.size()));
        System.out.println("Random Fruit: " + randomFruit);
    }
}
