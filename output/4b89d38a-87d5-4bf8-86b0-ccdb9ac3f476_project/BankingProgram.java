import java.util.Scanner;

public class BankingProgram {

    static double balance = 0; // Our account has a balance such as dollars and cents
    static Scanner scanner = new Scanner(System.in); // Accepting user input
    static boolean isRunning = true; // Continue this program as long as a user doesn't exit

    public static void main(String[] args) {
        // As a beginner, it might be helpful to you to break up your project into separate steps
        // Then tackle this project one step at a time

        // Different steps our program is going to take
        // 1. Declare our variables
        // 2. Display a menu
        // 3. Get and process user's choice
        // 4. Show balance
        // 5. Make a deposit
        // 6. Withdraw funds
        // 7. Exit message

        // Declare variables

        // Display a menu to the user
        while (isRunning) {
            System.out.println("Banking Program");
            System.out.println("**************************");
            System.out.println("1. Show Balance");
            System.out.println("2. Deposit");
            System.out.println("3. Withdraw");
            System.out.println("4. Exit");
            System.out.println("**************************");

            // Get and process the user's choice
            System.out.print("Enter your choice (1-4): ");
            int choice = scanner.nextInt();

            // Process the user's choice
            switch (choice) {
                case 1:
                    // Call a method to show our balance
                    System.out.println("Show balance");
                    showBalance(balance);
                    break;
                case 2:
                    // Call a method to deposit
                    System.out.println("Deposit");
                    balance += deposit();
                    break;
                case 3:
                    // Call a method to withdraw
                    System.out.println("Withdraw");
                    balance -= withdraw(balance);
                    break;
                case 4:
                    // Exit
                    isRunning = false;
                    System.out.println("**************************");
                    System.out.println("Thank you, have a nice day!");
                    break;
                default:
                    System.out.println("Invalid choice");
            }
        }

        scanner.close(); // Close our scanner when we're done with it
    }

    // Method to show balance
    static void showBalance(double balance) {
        System.out.println("**************************");
        System.out.printf("Your balance is: $%.2f%n", balance);
        System.out.println("**************************");
    }

    // Method to make a deposit
    static double deposit() {
        System.out.print("Enter an amount to be deposited: ");
        double amount = scanner.nextDouble();

        if (amount < 0) {
            System.out.println("Amount can't be negative");
            return 0;
        } else {
            return amount;
        }
    }

    // Method to withdraw funds
    static double withdraw(double balance) {
        System.out.print("Enter amount to be withdrawn: ");
        double amount = scanner.nextDouble();

        if (amount > balance) {
            System.out.println("Insufficient funds");
            return 0;
        } else if (amount < 0) {
            System.out.println("Amount can't be negative");
            return 0;
        } else {
            return amount;
        }
    }
}