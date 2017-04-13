import pandas
from tabula import read_pdf_table


def get_amount(value):
    if value is None:
        return ""
    elif type(value) is float:
        return value
    else:
        return value.split(" ")[0]


def get_text(value):
    if pandas.isnull(value):
        return ""
    else:
        return " ".join(value.split(" ", 1)[1:])


df = read_pdf_table('/Users/utkbansal/Code/MonsoonFintech/part1/data/Balsheet.pdf')

print(list(df.columns.values))
df.dropna(axis='columns', how='all', inplace=True)
df.rename(columns={'Unnamed: 4': ''}, inplace=True)
# df['2016x'], df['Particlarsx'] = df['2016 Particulars'].apply(splitter)
df['2016'] = df['2016 Particulars'].apply(get_amount)
df['Particulars.1'] = df['2016 Particulars'].apply(get_text)
print(list(df.columns.values))
print(df)
df.to_csv('out.csv')


# convert_into('/Users/utkbansal/Code/MonsoonFintech/part1/data/Balsheet.pdf', 'direct.csv', output_format='csv')


class PDFToCSVConverter(object):
    def __init__(self, path):
        self.path = path
        # TODO: Check for existence of the file and permissions to read it
        self.data_frame = read_pdf_table(path)

    def remove_blank_columns(self):
        self.data_frame.dropna(axis='columns', how='all', inplace=True)

    def fix_columns_names(self):
        # If the column doesn't have a name it should be left blank
        pass

    def split_columns(self):
        # Split columns that are clubbed together
        pass

    def write(self, name='outfile.csv'):
        self.data_frame.to_csv(name)


if __name__ == '__main__':
    path = input("Enter the absolute path to the pdf file")
    converter = PDFToCSVConverter(path)
    converter.write()