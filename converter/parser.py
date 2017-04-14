import pandas
from pandas import isnull
from tabula import read_pdf_table


class PDFToCSVConverter(object):
    def __init__(self, path):
        self.path = path
        # TODO: Check for existence of the file and permissions to read it
        self.data_frame = read_pdf_table(path)
        self.cleaned_data = []
        self.clean_dataframe()

    def remove_blank_columns(self):
        self.data_frame.dropna(axis='columns', how='all', inplace=True)

    def fix_columns_names(self):
        # If the column doesn't have a name it should be left blank
        self.data_frame.rename(columns={'Unnamed: 4': ''}, inplace=True)

    def split_columns(self):
        """
        Split columns that are clubbed together
        """
        self.data_frame['2016.1'] = self.data_frame['2016 Particulars'].apply(self.get_amount)
        self.data_frame['Particulars.1'] = self.data_frame['2016 Particulars'].apply(self.get_text)
        # Removing the merged columns and repositioning the 2 new ones into its place
        del self.data_frame['2016 Particulars']
        cols = self.data_frame.columns.tolist()
        cols = cols[:2] + cols[-2:] + cols[2:5]
        self.data_frame = self.data_frame[cols]

    def clean_dataframe(self):
        """
        Cleanup the dataframe and generate self.cleaned_data
        """
        self.remove_blank_columns()
        self.fix_columns_names()
        self.split_columns()

        # Prepare cleaned_data
        for index, row in self.data_frame.iterrows():
            if not isnull(row[0]) and row[0] != '' and not str(row[0]).startswith('Total'):
                self.clean_data((row[0], row[1], row[2]))
            if not isnull(row[3]) and row[3] != '' and not str(row[3]).startswith('Total'):
                self.clean_data((row[3], row[4], row[5]))

    def write(self, path='data/outfile.csv'):
        """
        Write CSV contents to a file or file-like object
        """
        self.data_frame.to_csv(path)

    def clean_data(self, data):
        """
        Clean all the data and append to self.cleaned_data
        """
        # Convert everything to string
        data = [str(data[0]), str(data[1]), str(data[2])]

        # Get rid of Nan
        for index, value in enumerate(data):
            if value == 'nan':
                data[index] = ''

        if data[0].startswith('To '):
            data[0] = data[0].replace('To ', '', 1)
        if data[0].startswith('By '):
            data[0] = data[0].replace('By ', '', 1)

        data[0] = data[0].strip()
        self.cleaned_data.append(data)

    @staticmethod
    def get_amount(value):
        if value is None:
            return ""
        elif type(value) is float:
            return value
        else:
            return value.split(" ")[0]

    @staticmethod
    def get_text(value):
        if pandas.isnull(value):
            return ""
        else:
            return " ".join(value.split(" ", 1)[1:])


if __name__ == '__main__':
    # path = input("Enter the absolute path to the pdf file")
    path = '/Users/utkbansal/Downloads/parsing/Balsheet.pdf'
    converter = PDFToCSVConverter(path)
    # converter.save()
    print(converter.cleaned_data)
