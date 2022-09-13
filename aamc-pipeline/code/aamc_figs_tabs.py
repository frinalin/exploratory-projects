# %%
# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import os


# %%
outpath = '../writeup/figs'


# %%
## FUNCTIONS
# %%
## Function: Figure formatting

def format_fig():
    # Customize legend orientation and position
    fig.update_layout ( 
        legend = dict(
            title = None, 
            orientation = 'h',  #horizontal
            x = 0.5,
            y = -.3,
            yanchor = 'bottom',
            xanchor = 'center'
        )
    )

    #fig.add_vline(x=2013.5, line_width=1, line_dash="dash", line_color="lightslategray")


    # Change legend labels
    newnames = {'total_undup_app': 'Applicants', 
        'total_undup_acc': 'Accepted',
        'total_undup_mat': 'Matriculated',
        'black_ac_app': 'Applicants',
        'black_ac_acc': 'Accepted',
        'black_ac_mat': 'Matriculated',
        'frac_black_app': 'Applicants',
        'frac_black_mat': 'Matriculants',
        'rate_black_acc': 'Black',
        'rate_white_acc': 'White',
        'rate_asian_acc': 'Asian',
        'gradrate_black_m': 'Black Men',
        'gradrate_black_f': 'Black Women',
        'gradrate_total_m': 'Men',
        'gradrate_total_f': 'Women',
        'gradrate_black': 'Black',
        'gradrate_asian': 'Asian', 
        'gradrate_white': 'White',
        'gradrate_total': 'Total'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))

    fig.show()

# %%
## Function: Format AAMC data

def read_aamc_data():
    """ This function reads in and cleans the AAMC data tables A-14.1, A-14.2, and A-14.3. These contain applicant, acceptee, and matriculant counts by race and year from the 1978-1979 academic year to the 2019-202 academic year. 
    """
    # Import libraries
    import pandas as pd
    import numpy as np

    ## Format Table A-14.1: Applicants by race and year
    ## Alone and in combination

    # Read in data table
    df_applicants = pd.read_excel("C:/Users/frina/Dropbox/projects/5. Data/Representation in Health Care/AAMC/Medical School Applicant and Matriculant Data by Academic Year.xlsx", 
        sheet_name="A-14.1", 
        header=5, 
        skipfooter=1, 
        names = ['academic_year_of_application', 
            'aian_a', 'aian_c', 'aian_ac',
            'asian_a', 'asian_c', 'asian_ac',
            'black_a', 'black_c', 'black_ac',
            'hsip_a', 'hisp_c', 'hisp_ac',
            'nhopi_a', 'nhopi_c', 'nhopi_ac',
            'white_a', 'white_c', 'white_ac', 
            'other_a', 'other_c', 'other_ac', 
            'unknown',
            'nonus',
            'total_undup'],
        na_values = '-',
        convert_float = False)

    #df_applicants

    ## Format Table A-14.2: Acceptees by race and year
    ## Alone and in combination

    # Read in data table
    df_acceptees = pd.read_excel("C:/Users/frina/Dropbox/projects/5. Data/Representation in Health Care/AAMC/Medical School Applicant and Matriculant Data by Academic Year.xlsx", 
        sheet_name="A-14.2", 
        header=5, 
        skipfooter=1, 
        names = ['academic_year_of_application', 
            'aian_a', 'aian_c', 'aian_ac',
            'asian_a', 'asian_c', 'asian_ac',
            'black_a', 'black_c', 'black_ac',
            'hsip_a', 'hisp_c', 'hisp_ac',
            'nhopi_a', 'nhopi_c', 'nhopi_ac',
            'white_a', 'white_c', 'white_ac', 
            'other_a', 'other_c', 'other_ac', 
            'unknown',
            'nonus',
            'total_undup'],
        na_values = '-',
        convert_float = False)

    #df_acceptees

    ## Format Table A-14.3: Matriculants by race and year
    ## Alone and in combination

    # Read in data table
    df_matriculants = pd.read_excel("C:/Users/frina/Dropbox/projects/5. Data/Representation in Health Care/AAMC/Medical School Applicant and Matriculant Data by Academic Year.xlsx", 
        sheet_name="A-14.3", 
        header=5, 
        skipfooter=1, 
        names = ['academic_year_of_application', 
            'aian_a', 'aian_c', 'aian_ac',
            'asian_a', 'asian_c', 'asian_ac',
            'black_a', 'black_c', 'black_ac',
            'hsip_a', 'hisp_c', 'hisp_ac',
            'nhopi_a', 'nhopi_c', 'nhopi_ac',
            'white_a', 'white_c', 'white_ac', 
            'other_a', 'other_c', 'other_ac', 
            'unknown',
            'nonus',
            'total_undup'],
        na_values = '-',
        convert_float = False)

    # Combine tables
    data = df_applicants.merge(df_acceptees, how = 'left',
        on = 'academic_year_of_application',
        suffixes = [None, '_acc']).merge(df_matriculants, how = 'left',
        on = 'academic_year_of_application',
        suffixes = ['_app', '_mat'])

    # Create variables for plotting
    data[['year1','year2']] = data['academic_year_of_application'].str.split('-', expand=True)
    data = data.astype({'year1': 'int', 'year2': 'int'})

    ## GRADUATION AND ENROLLMENT DATA
    # Read in data table
    df_enrollment = pd.read_excel("C:/Users/frina/Dropbox/projects/5. Data/Representation in Health Care/AAMC/Medical School Enrollment and Graduates by Race Ethnicity Sex and Academic Year.xlsx", 
        sheet_name="Enrollment (AC)", 
        header=6, 
        skipfooter=1, 
        names = ['medical_school_name',
            'academic_year', 
            'aian_m', 'aian_f',
            'asian_m', 'asian_f', 
            'black_m', 'black_f',
            'hsip_m', 'hisp_f',
            'nhopi_m', 'nhopi_f', 
            'white_m', 'white_f', 
            'other_m', 'other_f',
            'unknown_m', 'unknown_f',
            'nonus_m', 'nonus_f',
            'total_m', 'total_f', 'total'])

    df_graduates = pd.read_excel("C:/Users/frina/Dropbox/projects/5. Data/Representation in Health Care/AAMC/Medical School Enrollment and Graduates by Race Ethnicity Sex and Academic Year.xlsx", 
        sheet_name="Graduates (AC)", 
        header=6, 
        skipfooter=1, 
        names = ['medical_school_name',
            'academic_year', 
            'aian_m', 'aian_f',
            'asian_m', 'asian_f', 
            'black_m', 'black_f',
            'hsip_m', 'hisp_f',
            'nhopi_m', 'nhopi_f', 
            'white_m', 'white_f', 
            'other_m', 'other_f',
            'unknown_m', 'unknown_f',
            'nonus_m', 'nonus_f',
            'total_m', 'total_f', 'total'])

    # Merge data
    data2 = df_enrollment.merge(df_graduates, how = 'inner',
        on = ['medical_school_name', 'academic_year'],
        suffixes = ['_en', '_gr'])

    # Year variables
    data2[['year1','year2']] = data2['academic_year'].str.split('-', expand=True)
    data2 = data2.astype({'year1': 'int', 'year2': 'int'})
    
    # # Create 4-year graduation counts
    indexer = pd.api.indexers.FixedForwardWindowIndexer(window_size=4)
    data2_rolling = data2.groupby('medical_school_name').rolling(window = indexer, min_periods = 4).sum().reset_index()
    data2_rolling = data2_rolling.drop(data2_rolling.filter(regex = '_en').columns, axis = 1)
    data3 = data2.merge(data2_rolling, how = 'left',
        left_index = True, right_index = True, 
        suffixes = [None, '_4yr'])

    # df_enrollment[['year1','year2']] = df_enrollment['academic_year'].str.split('-', expand=True)
    # df_enrollment = df_enrollment.astype({'year1': 'int', 'year2': 'int'})

    # df_graduates[['year1','year2']] = df_graduates['academic_year'].str.split('-', expand=True)
    # df_graduates = df_graduates.astype({'year1': 'int', 'year2': 'int'})
    # df_graduates['year_enrolled'] = df_graduates.year2 - 4

    return data, data3

# %%
[data, data2] = read_aamc_data()

# %%
## Figure 1: Applicants, Acceptees, and Matriculants Over Time
# Total and Black

# Black
fig = px.line(data, x = 'year2', 
    y = ['black_ac_app', 'black_ac_acc',  'black_ac_mat'],
    #color = 'gender_race',
    width = 700, height = 400,
    markers = True,
    range_y = [0, 6500],
    labels = {
        'year2': 'Matriculation Year',
        'value': 'Count'
    },
    template = 'plotly_white')
fig.add_vline(x=2002.5, line_width=1, line_dash="dash", line_color="lightslategray")
format_fig()
fig.write_image(os.path.join(outpath, 'applicant_count_black.png'))

# Total
fig = px.line(data, x = 'year2', 
    y = ['total_undup_app', 'total_undup_acc',  'total_undup_mat'],
    #color = 'gender_race',
    width = 700, height = 400,
    markers = True,
    range_y = [0, 65000],
    labels = {
        'year2': 'Matriculation Year',
        'value': 'Count'
    },
    template = 'plotly_white')
format_fig()
fig.write_image(os.path.join(outpath, 'applicant_count_total.png'))

# %%
## Figure 2: Racial Composition of Matriculants Over Time
# White, Asian, Black, Other
# create data series
data['frac_black_mat'] = data.black_ac_mat / data.total_undup_mat
data['frac_white_mat'] = data.white_ac_mat / data.total_undup_mat
data['frac_asian_mat'] = data.asian_ac_mat / data.total_undup_mat
data['frac_aian_mat'] = data.aian_ac_mat / data.total_undup_mat
data['frac_nhopi_mat'] = data.nhopi_ac_mat / data.total_undup_mat
data['frac_other_mat'] = (data.total_undup_mat - (data.black_a_mat + data.white_a_mat + data.asian_a_mat)) / data.total_undup_mat

data['frac_black_app'] = data.black_ac_app / data.total_undup_app


# plot
fig = px.line(data, x = 'year2', 
    y = ['frac_black_app', 'frac_black_mat'],
    width = 700, height = 400,
    range_y = [0, 0.14], 
    markers = True,
    labels = {
        'value': 'Fraction Black',
        'year2': 'Matriculation Year'
    },
    template = 'plotly_white')
fig.add_vline(x=2002.5, line_width=1, line_dash="dash", line_color="lightslategray")
format_fig()
fig.write_image(os.path.join(outpath, 'matriculant_frac_black.png'))

# %%
## Figure 3: Acceptance Rates by Race Over Time
# White, Asian, Black, Other
# create data series
data['rate_black_acc'] = data.black_ac_acc / data.black_ac_app
data['rate_white_acc'] = data.white_ac_acc / data.white_ac_app
data['rate_asian_acc'] = data.asian_ac_acc / data.asian_ac_app

# plot
fig = px.line(data, x = 'year2', 
    y = ['rate_black_acc', 'rate_white_acc', 'rate_asian_acc'],
    width = 700, height = 400,
    range_y = [0, 0.9], 
    markers = True,
    labels = {
        'value': 'Acceptance Rate',
        'year2': 'Matriculation Year'
    },
    template = 'plotly_white')
fig.add_vline(x=2002.5, line_width=1, line_dash="dash", line_color="lightslategray")
format_fig()
fig.write_image(os.path.join(outpath, 'acceptance_rate_byrace.png'))

# %%
## Graduation and enrollment figures; explore
# Collapse across schools, 5-year bins
#data2['year_bin'] = np.floor((data2.year_enrolled / 5)) * 5 + 2
df_gradrate = data2.groupby('year1').sum().reset_index()
df_gradrate = df_gradrate[df_gradrate['year1'].isin([1983, 1987, 1991, 1995, 1999, 2003, 2007, 2011, 2015])]
df_gradrate['year_enrolled'] = df_gradrate.year1 - 1.5


# create grad rate variables
df_gradrate['gradrate_black'] = (df_gradrate.black_m_gr_4yr + df_gradrate.black_f_gr_4yr) / (df_gradrate.black_m_en + df_gradrate.black_f_en)
df_gradrate['gradrate_asian'] = (df_gradrate.asian_m_gr_4yr + df_gradrate.asian_f_gr_4yr) / (df_gradrate.asian_m_en + df_gradrate.asian_f_en)
df_gradrate['gradrate_white'] = (df_gradrate.white_m_gr_4yr + df_gradrate.white_f_gr_4yr) / (df_gradrate.white_m_en + df_gradrate.white_f_en)


# %%
## Plot graduation rates over time
fig = px.line(df_gradrate, x = 'year_enrolled', 
    y = ['gradrate_black', 'gradrate_white', 'gradrate_asian'],
    #color = 'gender_race',
    width = 700, height = 400,
    markers = True,
    range_y = [0, 1.1],
    range_x = [1977, 2017],
    labels = {
        'year_enrolled': 'Matriculation Year',
        'value': 'Fraction Graduated'
    },
    template = 'plotly_white')
fig.add_vline(x=1999.5, line_width=1, line_dash="dash", line_color="lightslategray")
format_fig()
fig.write_image(os.path.join(outpath, 'gradrate_byrace.png'))

# %%
## Plot graduation rates by school (1980-1999, and 2000-2015 enrollment years)
# Collapse to school level
df_gradbyschool = data2[data2.year1.between(1980, 2015)]
df_gradbyschool = df_gradbyschool.groupby('medical_school_name').sum().reset_index()

# create grad rate variables
df_gradbyschool['black_gr_4yr'] = df_gradbyschool.black_m_gr_4yr + df_gradbyschool.black_f_gr_4yr
df_gradbyschool['gradrate_black'] = (df_gradbyschool.black_m_gr_4yr + df_gradbyschool.black_f_gr_4yr) / (df_gradbyschool.black_m_en + df_gradbyschool.black_f_en)
df_gradbyschool['gradrate_asian'] = (df_gradbyschool.asian_m_gr_4yr + df_gradbyschool.asian_f_gr_4yr) / (df_gradbyschool.asian_m_en + df_gradbyschool.asian_f_en)
df_gradbyschool['gradrate_white'] = (df_gradbyschool.white_m_gr_4yr + df_gradbyschool.white_f_gr_4yr) / (df_gradbyschool.white_m_en + df_gradbyschool.white_f_en)



# %%
## Plot graduation rates by school
fig = px.scatter(df_gradbyschool[df_gradbyschool.black_gr_4yr > 100], x = 'gradrate_white', 
    y = ['gradrate_black'],
    hover_data = ['medical_school_name'],
    #color = 'gender_race',
    width = 700, height = 600,
    #markers = True,
    range_y = [0, 1.1],
    range_x = [0, 1.1],
    labels = {
        'gradrate_white': 'White Graduation Rate',
        'value': 'Black Graduation Rate'
    },
    #text = 'medical_school_name',
    template = 'plotly_white')
#fig.add_vline(x=2002, line_width=1, line_dash="dash", line_color="lightslategray")
format_fig()
fig.write_image(os.path.join(outpath, 'gradrate_byschool_byrace.png'))

#%%
# Stats on graduation rate gap
print(df_gradbyschool.gradrate_white.mean())
print(df_gradbyschool.gradrate_black.mean())

print(df_gradrate.gradrate_white.mean())
print(df_gradrate.gradrate_black.mean())




# %%
## MAKE a table of top 10 producers of Black physicians, 1980-1999 and 2000-2015. Including graduation rates
## 1980-1999
df_gradbyschool1 = data2[data2.year1.between(1984, 1999)]
df_gradbyschool1 = df_gradbyschool1.groupby('medical_school_name').sum().reset_index()

# create grad rate variables
df_gradbyschool1['black_gr'] = df_gradbyschool1.black_m_gr + df_gradbyschool1.black_f_gr
df_gradbyschool1['total_gr'] = df_gradbyschool1.total_m_gr + df_gradbyschool1.total_f_gr
df_gradbyschool1['frac_black'] = df_gradbyschool1.black_gr / df_gradbyschool1.total_gr
df_gradbyschool1['gradrate_black'] = (df_gradbyschool1.black_m_gr_4yr + df_gradbyschool1.black_f_gr_4yr) / (df_gradbyschool1.black_m_en + df_gradbyschool1.black_f_en)
df_gradbyschool1['gradrate_asian'] = (df_gradbyschool1.asian_m_gr_4yr + df_gradbyschool1.asian_f_gr_4yr) / (df_gradbyschool1.asian_m_en + df_gradbyschool1.asian_f_en)
df_gradbyschool1['gradrate_white'] = (df_gradbyschool1.white_m_gr_4yr + df_gradbyschool1.white_f_gr_4yr) / (df_gradbyschool1.white_m_en + df_gradbyschool1.white_f_en)

df_gradbyschool1['black_share_of_total'] = df_gradbyschool1.black_gr / (df_gradbyschool1.black_gr.sum())

table_19841999 = df_gradbyschool1.nlargest(10, 'black_gr').filter(['medical_school_name',
    'black_gr', 'frac_black', 'black_share_of_total', 'gradrate_black'])

## 2000-2015
df_gradbyschool1 = data2[data2.year1.between(2000, 2015)]
df_gradbyschool1 = df_gradbyschool1.groupby('medical_school_name').sum().reset_index()

# create grad rate variables
df_gradbyschool1['black_gr'] = df_gradbyschool1.black_m_gr + df_gradbyschool1.black_f_gr
df_gradbyschool1['total_gr'] = df_gradbyschool1.total_m_gr + df_gradbyschool1.total_f_gr
df_gradbyschool1['frac_black'] = df_gradbyschool1.black_gr / df_gradbyschool1.total_gr
df_gradbyschool1['gradrate_black'] = (df_gradbyschool1.black_m_gr_4yr + df_gradbyschool1.black_f_gr_4yr) / (df_gradbyschool1.black_m_en + df_gradbyschool1.black_f_en)
df_gradbyschool1['gradrate_asian'] = (df_gradbyschool1.asian_m_gr_4yr + df_gradbyschool1.asian_f_gr_4yr) / (df_gradbyschool1.asian_m_en + df_gradbyschool1.asian_f_en)
df_gradbyschool1['gradrate_white'] = (df_gradbyschool1.white_m_gr_4yr + df_gradbyschool1.white_f_gr_4yr) / (df_gradbyschool1.white_m_en + df_gradbyschool1.white_f_en)

df_gradbyschool1['black_share_of_total'] = df_gradbyschool1.black_gr / (df_gradbyschool1.black_gr.sum())

table_20002015 = df_gradbyschool1.nlargest(10, 'black_gr').filter(['medical_school_name',
    'black_gr', 'frac_black', 'black_share_of_total', 'gradrate_black'])

## Output the tables
table_19841999.to_csv(os.path.join(outpath, 'table_19841999.csv'), index = False)
table_20002015.to_csv(os.path.join(outpath, 'table_20002015.csv'), index = False)

# %%
