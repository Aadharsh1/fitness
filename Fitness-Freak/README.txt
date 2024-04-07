Installation
    To set up the Fitness Freak project, please follow these steps:

    1. Place Project Folder: Move the entire project folder into the www directory of your WAMP server installation. For example, it should be located at C:\wamp64\www\Fitness-Freak.

    2. Start Containers: Run Docker Desktop. Open a terminal and navigate to the directory containing the compose.yaml file. 
    Then, execute the following command to start the necessary containers: docker compose up --build

    Note: It's not required to manually run the SQL scripts, as the MySQL databases are containerized.

    3. Access Application: After the containers are up and running, open the login.html page, located under the test_ui folder, on wamp server to start using the application. The path to this file is FITNESS-FREAK/test_ui/login.html.


Login Details

You can use the following accounts to log in and test the application:

    First Account
        Email: anshaziq@gmail.com
        Password: fitness333

    Second Account:
        Email: tazngmt@gmail.com
        Password: fitness123


Features and Testing Scenarios

    Workout Plans: 
        - Navigate to the user profile and adjust the height and weight settings. Observe how the suggested workout plans change based on these inputs.

    Challenge Verification: 
        - Use the images located in the Test_Images folder (FITNESS-FREAK/Test_Images) for challenge verification. 
        - After successful verification, the updated loyalty points will be visible in the user profile.

    Product Purchases and Notifications: 
        - Users can input a number of loyalty points up to a maximum of 15% of the total undiscounted price when purchasing products.
        - Experiment with purchasing different quantities and types of products. Notice how the email you receive changes. 
        - AMQP-based notifications will be sent to the email provided on the Stripe API payment page.