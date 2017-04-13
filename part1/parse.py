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
