
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

class Result:
    def __init__(self, user_page_text):
        self.user_page_text = user_page_text
        self.soup = BeautifulSoup(self.user_page_text, 'html.parser')
        self.results_table = self.get_results_table()
        self.name = self.get_name()
        self.id = self.get_id()
        self.num_results = len(self.results_table)

        # event counts
        self.unique_events_counts = self.results_table['Event'].value_counts()
        self.num_unique_events = len(self.unique_events_counts)
        self.most_frequent_event = self.unique_events_counts.idxmax()

        #other
        self.overall_pb = self.get_overall_pb()
        self.overall_best_Age_grade = self.get_overall_best_age_grade()
        self.event_type = self.get_event_type()




    def convert_to_seconds(self,time_str: str):

        """
        converts strings of time in format 10:33 or 01:01:42 into time in seconds
        """

        parts = time_str.split(':')
        if len(parts) == 2:
            time_str = '00:' + time_str

        return pd.to_timedelta(time_str).total_seconds()


    def get_results_table(self):

        # The third table is the table of results
        results_table = self.soup.find_all('table')[2]

        html_string_io = StringIO(str(results_table))
        results_table_df = pd.read_html(html_string_io)[0]

        # Step 1: Convert the date and time strings
        results_table_df['Run Date'] = pd.to_datetime(results_table_df['Run Date'], format='%d/%m/%Y')
        
        results_table_df['Time'] = results_table_df['Time'].apply(self.convert_to_seconds)

        return results_table_df
    
    def get_name(self):
        user_string = self.soup.h2.get_text()
        name_string = user_string.split('\xa0')[0][:-1]
        return name_string

    def get_id(self):
        user_string = self.soup.h2.get_text()
        id_string = user_string.split('\xa0')[1][1:-1]
        return id_string
    
    def get_overall_pb(self):

        df = self.results_table
        min_index = df['Time'].idxmin()
        min_row = df.loc[min_index]

        return min_row.to_dict()

    def get_overall_best_age_grade(self):

        df = self.results_table
        df['Age_Grade_Numeric'] = df['Age Grade'].str.rstrip('%').astype(float) / 100
        max_index = df['Age_Grade_Numeric'].idxmax()
        max_row = df.loc[max_index]

        return max_row.to_dict()
    
    def get_event_type(self):
        event_text = self.soup.find_all('table')[2].caption.get_text()

        if '5k' in event_text:
            event_type = '5k'
        elif 'junior' in event_text:
            event_type = 'junior'
        else:
            event_type = 'unknown'

        return event_type


        


    # def get_results_table(id):

    #     page = get_url(id)

    #     results_table_df = self.get_results_table(page)

    #     return results_table_df

if __name__ == "__main__":

    with open("ExampleInput1.html", "r") as file:
        text = file.read()
    
    print(text)

    user_results = Result(text)
    print(user_results.results_table)
    
    # print nice version of soup
    print(user_results.soup.prettify())



