# CS50P Final Project: Data Preprocessing and Basic Analysis
### Video Demo:  https://youtu.be/C7LvGN34AjU
### Me50:  https://github.com/me50/Lima82/tree/6884758df863054c6b2194c0cd2dc06e7400c71f
### Certificate:  https://courses.edx.org/certificates/c34e2703fd0a4bfb90e58a7ac05f71ea?_gl=1*q5xvzf*_gcl_au*MTA3MzM0ODI2OS4xNzI5OTU4MjE0*_ga*MTExMzI2MjQyMS4xNzI5OTU4MjE0*_ga_D3KS4KMDT0*MTcyOTk1ODIxNC4xLjEuMTcyOTk2MDUwMC40Ni4wLjA.
### Description:
In my role as a data analyst, I often deal with raw, unprocessed data. That is why I created this program which I would like to share with everyone. It can be adapted to any data frame with raw data. The main goal of my program is to prepare data for further analysis, and I've also included a small analytical component for demonstration purposes.

To show how it works, I created a CSV file "raw_data_for_final_project_CS50.csv”, containing a list of renowned artists from the past. The file includes two columns: Column1 has the artist's name, birth and death dates in parentheses separated by a dash, and Column2 contains information about the artist's art movement. I intentionally introduced various issues into the data, such as extra spaces before and after the full name, additional spaces between the first and second names, extra characters before the birth date, missing values, and duplicate rows. The list is not sorted alphabetically.

The program's output consists of four new files:
- A file with cleaned and alphabetically sorted data named "cleaned_data.csv";
- A file with demonstration outputs of the program's results named "demo_of_results.txt";
- A file with a graph illustrating the numbers of artists in a specific movement named "demo_visualization_movement.png";
- A file with a graph depicting the distribution of artists by age at the time of death named "demo_visualization_age.png".

The program is structured into three parts:

#### First part (data preprocessing):
- Import modules;
- Define a main function that encapsulates all subsequent related functions;
- Define the read_file() function to read a CSV file using the "os" module:
  - The function utilizes the "os" module to read a previously created file with data: “raw_data_for_final_project_CS50.csv”;
  - The file is stored in the project's root folder, alongside other project files;
  - It opens the file with unformatted data in columns, separated by tabs;
  - It presents the first 10 rows in the "demo_of_results.txt" file.
- Define the split_name_age() function to split "Column1" into "Dates," then into "Birth" and "Death":
  - Initially, the function, using the "re" module and regular expressions, separates information from the Column1;
  - It places the separated information into two new columns: “Name” (full name) and “Dates“ (life dates without parentheses, separated by a dash);
  - Then, the function further splits the “Dates” column into “Birth” (birth year) and “Death” (death year);
  - It removes two unnecessary columns: “Column1” and “Dates”;
  - The columns are ordered as asked, and the first 10 rows of the new table are displayed in the “demo_of_results.txt“ file.
- Define the find_drop_missing_values() function to search for missing values:
  - This function counts all missing values in the data frame and deletes all rows containing them, as they are unnecessary for the intended research;
  - Information about the number of missing values and their locations is displayed in the "demo_of_results.txt" file.
- Define the find_explicit_duplicates() function to search for duplicates:
  - The function looks for duplicates in the data frame and displays the count of these duplicates and their list in tabular form in the “demo_of_results.txt” file if they exist;
  - If no explicit duplicates are found, the function prints the phrase "Explicit duplicates didn't find.".
- Define the drop_explicit_duplicates() function to drop duplicates:
  - This function removes duplicates and updates the table's indexing.
- Define the remove_extra_spaces_and_characters_data() function to remove extra spaces, characters, change data type in columns "Birth" and "Death" to integer, apply lowercase() and title() functions:
  - The function removes extra spaces in the entire table and unnecessary characters before the date in the “Birth” column;
  - It changes the data type in the “Birth” and “Death” columns to integer. While it would be more appropriate for analytics to change the data type to datetime, in this case, working only with years and not needing these data as dates for further analysis, integer is used;
  - The “demo_of_results.txt“ file displays 10 rows of the data frame after the changes.
- Define the age_data() function to count age of artists at the moment of death:
  - The function adds a new column “Age” to the data frame, calculating the age of each artist at the time of death by subtracting the birth year from the death year;
  -  Afterward, the “Movement” column is moved to the end of the table, indexes are updated, and the data frame is sorted alphabetically by artist names.
- Define the print_main_dataframe_info() function to print main data frame information and statistical data summary:
  - The function prints necessary analytics for work to the “demo_of_results.txt” file. This includes general information about the data frame (data types, number of rows and columns, etc.);
  - Statistical information (mean, median, standard deviation, minimum, maximum, etc.) for numeric columns is also printed to the “demo_of_results.txt” file.

#### Second part (basic analysis):
- Define the visualization() function to visualize data from columns "Movement" and "Age":
  - This function groups data by the “Movement” and “Age” columns, calculates the count of values for each group, and displays the information in the “demo_of_results.txt file” as aggregated tables;
  - Subsequently, graphs are generated based on those aggregated tables, and they are saved as “demo_visualization_movement.png” and “demo_visualization_age.png” files;
  - Additionally, the first 10 rows of the final version of the data frame are displayed in the “demo_of_results.txt” file, along with a closing message.

#### Third part:
- Finally, the last save_to_csv() function is defined to save cleaned data to a CSV file:
  - This function saves the cleaned data frame to a new CSV file named “cleaned_data.csv”.

So, I’ve created a versatile data analyst program that, with minor modifications, can read a file, organize data, and prepare it for further analytical explorations.

Thank you for your time!

Best regards, Marina Orlenko




