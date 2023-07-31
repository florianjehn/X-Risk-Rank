import re
import pandas as pd

def extract_authors(df):
    """
    Extracts all author names from the 'Authors' column of the given DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the 'Authors' column.

    Returns:
        list: A list of all author names found in the 'Authors' column.

    Example:
        >>> import pandas as pd
        >>> data = {'Title': ['Paper 1', 'Paper 2'],
        ...         'Authors': ['John Doe, Jane Smith, Adam Johnson', 'Alice Williams, Bob Brown']}
        >>> df = pd.DataFrame(data)
        >>> extract_authors(df)
        ['John Doe', 'Jane Smith', 'Adam Johnson', 'Alice Williams', 'Bob Brown']
    """
    authors_list = df['Authors'].str.split(', ').explode().tolist()
    return authors_list

def clean_author_names(author_list):
    """
    Cleans the author names by converting them to lowercase, removing spaces,
    punctuation, and keeping only the last name and the first initial.

    Parameters:
        author_list (list): A list of author names to be cleaned.

    Returns:
        list: A list of cleaned author names.

    Example:
        >>> author_list = ['Doe J.', 'Smith J.', 'Johnson A.']
        >>> clean_author_names(author_list)
        ['doej', 'smithj', 'johnsona']
    """
    cleaned_authors = []
    for name in author_list:
        # Ignore names that are only a single name, as those are errors
        if len(name.split()) == 1:
            continue
        try:
            last_name = name.split()[0]
            first_initial = name.split()[1][0]
            cleaned = last_name + first_initial
            cleaned = cleaned.lower().replace(' ', '')
        except AttributeError as e:
            print(e)
            print(f'Error: {name}')
            break
        except IndexError as e:
            print(e)
            print(f'Error: {name}')
            break            
        cleaned_authors.append(cleaned)
    return cleaned_authors

def create_author_count_dataframe(author_list):
    """
    Counts the occurrences of each name in the author list and creates a DataFrame
    with the count in one column and the name in another column (First initial + Last Name).

    Parameters:
        author_list (list): A list of author names in the format last name + first initial (lowercase).

    Returns:
        pandas.DataFrame: A DataFrame with the count and the formatted name.

    Example:
        >>> author_list = ['doej', 'smithj', 'johnsona', 'williamsa', 'brownb', 'smithj']
        >>> create_author_count_dataframe(author_list)
           Count         Name
        0      1     JSmith
        1      1   AJohnson
        2      1  AWilliams
        3      1      BBrown
        4      2       JSmith
    """
    name_counts = {}
    formatted_names = []

    for name in author_list:
        name_counts[name] = name_counts.get(name, 0) + 1

    for name, count in name_counts.items():
        last_name, first_initial = name[0:-1].capitalize(), name[-1].upper()
        formatted_names.append(f"{first_initial}. {last_name}")

    data = {'Count': list(name_counts.values()), 'Name': formatted_names}
    df = pd.DataFrame(data)
    return df



if __name__ == "__main__":
    print(clean_author_names(['Doe J.', 'Smith J.', 'Johnson A.']))
