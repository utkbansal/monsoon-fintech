import pandas
from tabula import read_pdf_table


class PDFToCSVConverter(object):
    def __init__(self, path):
        self.path = path
        # TODO: Check for existence of the file and permissions to read it
        self.data_frame = read_pdf_table(path)

    def remove_blank_columns(self):
        self.data_frame.dropna(axis='columns', how='all', inplace=True)

    def fix_columns_names(self):
        # If the column doesn't have a name it should be left blank
        self.data_frame.rename(columns={'Unnamed: 4': ''}, inplace=True)

    def split_columns(self):
        # Split columns that are clubbed together
        self.data_frame['2016.1'] = self.data_frame['2016 Particulars'].apply(self.get_amount)
        self.data_frame['Particulars.1'] = self.data_frame['2016 Particulars'].apply(self.get_text)

    def write(self, path='data/outfile.csv'):
        self.remove_blank_columns()
        self.fix_columns_names()
        self.split_columns()
        self.data_frame.to_csv(path)

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
    path = '/Users/utkbansal/Code/MonsoonFintech/part1/data/Balsheet.pdf'
    converter = PDFToCSVConverter(path)
    converter.write()
