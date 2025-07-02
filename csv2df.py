
def csv2df():
    import pandas as pd

    # Load the CSV file into a pandas DataFrame
    file_path = 'input/register_allocation.csv'
    df = pd.read_csv(file_path)

    # Convert the DataFrame into a dictionary
    log_dict = df.to_dict(orient='records')

    # Save the dictionary log to a .log file
    with open('output/regfile_dictionary.log', 'w') as log_file:
        for record in log_dict:
            log_file.write(f"{record}\n")

if __name__ == "__main__":
    csv2df()
