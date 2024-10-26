# Import modules
from IPython.display import display
import pandas as pd
import os
import sys
import csv
import seaborn as sns
import matplotlib.pyplot as plt


# Define a main function
def main():
    data = read_file()
    data_splited = split_name_age(data)
    data_drop_missing_values = find_drop_missing_values(data_splited)
    find_explicit_duplicates(data_drop_missing_values)
    clean_data = drop_explicit_duplicates(data_drop_missing_values)
    data_cleaned = remove_extra_spaces_and_characters_data(clean_data)
    final_data = age_data(data_cleaned)
    total_info(final_data)
    result = visualization(final_data)
    # Save cleaned data to a CSV file
    save_to_csv(final_data, "cleaned_data.csv")
    return result


# Define a function to read a CSV file using the "os" module
def read_file():
    path = "/workspaces/141852833/project/raw_data_for_final_project_CS50.csv"
    if os.path.exists(path):
        data = pd.read_csv(path, sep="\t", encoding="utf-8")
    else:
        print("Something is wrong")
    display(f"Our raw data for demo:\n{data.head(10)}\n")
    return data


# Define a function to split "Column1" to "Dates", then to "Birth" and "Death"
def split_name_age(data):
    # Split "Column1" to "Names" and "Dates" using regular expressions
    data[["Name", "Dates"]] = data["Column1"].str.extract(r"([^\d(]+)\s*\(([^)]+)\)")
    # Split "Dates" to "Birth" and "Death"
    data[["Birth", "Death"]] = data["Dates"].str.split("-", expand=True)
    # Drop unnecessary columns
    data.drop(["Column1", "Dates"], axis=1, inplace=True)
    # Rename "Column2" to "Movement"
    data = data.rename(columns={"Column2": "Movement"})
    # Move the column "Movement" to the end of the table
    data = data[["Name", "Birth", "Death", "Movement"]]
    display(f"Our raw data with splited columns for demo:\n{data.head(10)}\n")
    return data


# Define a function to search for missing values
def find_drop_missing_values(data_splited):
    # Count and sort missing values in data
    display(f"Missing values:\n{data_splited.isna().sum().sort_values()}\n")
    # Drop missing values and update indexing
    data_drop_missing_values = data_splited.dropna().reset_index(drop=True)
    return data_drop_missing_values


# Define a function to search for duplicates
def find_explicit_duplicates(data_drop_missing_values):
    # Count explisit duplicates
    explicit_duplicates_count = display(
        f"We have {data_drop_missing_values.duplicated().sum()} explisit duplicates!\n"
    )
    explicit_duplicates = None
    explicit_duplicates_count = 0
    # Check if count of explicit greater than zero and then display the duplicates as a table
    if data_drop_missing_values.duplicated().sum() > 0:
        explicit_duplicates = display(
            f"Explicit duplicates are:\n{data_drop_missing_values[data_drop_missing_values.duplicated(keep=False)]}\n"
        )
    else:
        display("Explicit duplicates did't find")
    return explicit_duplicates_count, explicit_duplicates


# Define a function to drop the duplicates
def drop_explicit_duplicates(data_drop_missing_values):
    return data_drop_missing_values.drop_duplicates().reset_index()


# Define a function to remove extra spaces, characters, change data type in columns "Birth" and "Death" to integer, apply lowercase()
# and title() functions
def remove_extra_spaces_and_characters_data(clean_data):
    # Strip leading and trailing spaces from all rows
    clean_data = clean_data.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Remove extra whitespaces between first name and last name
    clean_data["Name"] = clean_data["Name"].apply(lambda x: " ".join(x.split()))
    # Remove any characters before numbers at "Birth" column
    clean_data["Birth"] = clean_data["Birth"].replace(r"\D", "", regex=True)
    # Change type for integer in columns "Birth" and "Death"
    clean_data["Birth"] = clean_data["Birth"].astype(int)
    clean_data["Death"] = clean_data["Death"].astype(int)
    # Make all text in lowercase and all words are titled
    clean_data = clean_data.map(
        lambda x: x.lower().title() if isinstance(x, str) else x
    )
    clean_data.drop(["index"], axis=1, inplace=True)
    display(f"Our cleaned data for demo:\n{clean_data.head(10)}\n")
    return clean_data


# Define a function to count age of Artists at the moment of death
def age_data(data_cleaned):
    # Add a new column "Age" and count age of Artists at the moment of death
    data_cleaned["Age"] = data_cleaned["Death"] - data_cleaned["Birth"]
    # Move the column "Movement" to the end of a table and sort values in alphabetical order
    data_cleaned = (
        data_cleaned[["Name", "Birth", "Death", "Age", "Movement"]]
        .sort_values(by="Name")
        .reset_index(drop=True)
    )
    return data_cleaned


# Define a function to print main DataFrame infornation and statistical data summary
def total_info(final_data):
    display(f"DataFrame information:\n")
    display(f"{final_data.info()}\n")
    display(f"Statistical data summary:\n{final_data.describe()}\n")
    return final_data


# Define a function to visualize data from columns "Movement" and "Age"
def visualization(final_data):
    # Prepare info for the first visualization, count values from "Movement" grouped by movements
    res1 = final_data.groupby(["Movement"]).agg({"Movement": "count"})
    res1.columns = ["Movement_count"]
    res1 = res1.sort_values(by="Movement_count", ascending=False).reset_index()
    display(f"Count Artists by Movement:\n{res1}\n")
    plt.figure(figsize=(15, 10))
    sns.barplot(
        data=res1, x="Movement_count", y="Movement", palette="viridis", hue="Movement"
    ).set(title="Artist's by Movement")
    plt.ylabel("Movement")
    plt.xlabel("Atrist's count")
    sns.despine()
    plt.savefig("demo_visualisation_movement.png")
    # Prepare info for the second visualization, count values from "Age" grouped by ages
    res2 = final_data.groupby(["Age"]).agg({"Age": "count"})
    res2.columns = ["Age_count"]
    res2 = res2.sort_values(by="Age_count", ascending=False).reset_index()
    display(f"Count Artists by Age:\n{res2}\n")
    plt.figure(figsize=(15, 10))
    sns.histplot(data=final_data, x="Age", bins=20, color="Green", kde=True).set(
        title="Artist's by Age"
    )
    plt.xlabel("Atrist's by Age")
    sns.despine()
    plt.savefig("demo_visualisation_age.png")
    display(f"First 10 rows of our final dataset for demo:\n{final_data.head(10)}\n")
    display("The End! Thank you for your time!\nBest regards, Marina Orlenko")
    return final_data


# Define a function to save cleaned data to a CSV file
def save_to_csv(data, filename):
    data.to_csv(filename, index=False)


if __name__ == "__main__":
    output_file = "demo_of_results.txt"

    # Open a new file
    with open(output_file, "w") as f:
        # Redirect standart output to a file
        sys.stdout = f
        main()

    # Restore standart output to a file
    sys.stdout = sys.__stdout__
