# Import
from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Edit this variable to point to the path to your local copy of chromedriver.exe
# Don't have it? Download here: https://sites.google.com/a/chromium.org/chromedriver/downloads
path_to_chromedriver = 'chromedriver.exe'

###################################
# STEP 1: GET USER SEARCH OPTIONS #
###################################

def get_search_options():
    
    # Store all user search options in a dictionary
    search_options = {}

    # The prompts for each search parameter will be in a different function; the only required one is get_year(), which will be run automatically
    def get_year():
        # Prompt the user to select one of the 6 years available to search 
        while True:
            census_search_year = input('''[A] 1911
[B] 1901
[C] 1851
[D] 1841
[E] 1831
[F] 1821

Please type the corresponding letter for the year you wish to search: ''')

            # Check to see if the user has selected a valid response
            # If so, confirm year before continuing
            valid_answers = ['A', 'B', 'C', 'D', 'E', 'F']
            census_search_year = census_search_year.upper()
            if (census_search_year in valid_answers):
                try:
                    search_options.pop('County')
                except:
                    print()
                if (census_search_year == 'A'):
                    search_options['Year'] = '1911'
                elif (census_search_year == 'B'):
                    search_options['Year'] = '1901'
                elif (census_search_year == 'C'):
                    search_options['Year'] = '1851'
                elif (census_search_year == 'D'):
                    search_options['Year'] = '1841'
                elif (census_search_year == 'E'):
                    search_options['Year'] = '1831'
                elif (census_search_year == 'F'):
                    search_options['Year'] = '1821'
                break
            else:
                print('\nInvalid response.')


    # This is the function for gathering the search parameters for anything in a text input (e.g. surname, forename, DED)
    def get_search_string(parameter):
        print('\nEnter a value for the', parameter.upper(), 'field.')
        if (parameter == 'Surname'):
            print('Some examples: Reilly, Hamilton, Sheridan')
        elif (parameter == 'Forename'):
            print('Some examples: Patrick, John, Elizabeth')
        elif (parameter == 'Townland'):
            print('Some examples: Curragh West, Ballymaguire, Collinstown')
        elif (parameter == 'DED'):
            print('Some examples: Abbey, Tawnawully, Holywood')
        elif (parameter == 'Barony'):
            print('Some examples: Coleraine, West Carberry, Coole')
        elif (parameter == 'Parish'):
            print('Some examples: Aghadowey, Aghadown, Desertoghill')
        input_string = input('\nEnter a value, type DELETE to remove this parameter from your search, or type CANCEL to cancel input: ')
        input_string_upper = input_string.upper()
        if (input_string_upper == 'DELETE'):
            # If user wants to delete this parameter from her search, remove it from the search_options dictionary
            try:
                search_options.pop(parameter)
            except:
                print('\nSearch parameter is not present.')
        elif (input_string_upper != 'CANCEL'):
            search_options[parameter] = input_string



    # This is the function for gathering the search parameters for any number in a text input (e.g. age)
    def get_search_int(parameter):
        print('\nEnter a value for the', parameter.upper(), 'field.')
        if (parameter == 'Age'):
            print('Enter a number (generally between 0 and 105). Note that ages are searched in a +/- 5 years range.')
            print('In other words, if you enter 30, you will receive records of people aged 25 through 35.')
        input_string = input('\nEnter a value, type DELETE to remove this parameter from your search, or type CANCEL to cancel input: ')
        input_string_upper = input_string.upper()
        if (input_string_upper == 'DELETE'):
            # If user wants to delete this parameter from her search, remove it from the search_options dictionary
            try:
                search_options.pop(parameter)
            except:
                print('\nSearch parameter is not present.')
        elif (input_string_upper != 'CANCEL'):
            try:
                input_val = int(input_string)
                search_options[parameter] = input_val
            except ValueError:
                print('\nInput is not a valid number.')



    # This is the function to populate the sex parameter
    def get_sex():
        sex_input = input('\nEnter M or F, type DELETE to remove this parameter from your search, or type CANCEL to cancel input: ')
        sex_input = sex_input.upper()
        if (sex_input == 'DELETE'):
            # If user wants to delete this parameter from her search, remove it from the search_options dictionary
            try:
                search_options.pop('Sex')
            except:
                print('\nSearch parameter is not present.')
        elif (sex_input != 'CANCEL'):
            if (sex_input == 'M'):
                search_options['Sex'] = 'Male'
            elif (sex_input == 'F'):
                search_options['Sex'] = 'Female'
            else:
                input('\nInvalid response.')


    
    # Function for gathering county search parameter
    def get_county():
        # Different counties are available in different census years; this dictionary keeps track of them all
        counties = {
            'Antrim': ['1911', '1901', '1851', '1841', '1831', '1821'],
            'Armagh': ['1911', '1901', '1851'],
            'Carlow': ['1911', '1901', '1841', '1821'],
            'Cavan': ['1911', '1901', '1851', '1841', '1821'],
            'Clare': ['1911', '1901', '1851'],
            'Cork': ['1911', '1901',  '1841'],
            'Donegal': ['1911', '1901', '1851'],
            'Down': ['1911', '1901', '1851'],
            'Dublin': ['1911', '1901', '1851', '1841', '1821'],
            'Fermanagh': ['1911', '1901', '1851', '1841', '1821'],
            'Galway': ['1911', '1901', '1821'],
            'Kerry': ['1911', '1901', '1851'],
            'Kildare': ['1911', '1901', '1851'],
            'Kilkenny': ['1911', '1901', '1821'],
            'Kings Co': ['1911', '1901'], # referred to differently between year dropdowns
            'Kings': ['1821'], # referred to differently between year dropdowns
            'Leitrim': ['1911', '1901', '1851'],
            'Limerick': ['1911', '1901', '1851', '1841', '1821'],
            'Londonderry': ['1911', '1901', '1851', '1831'],
            'Longford': ['1911', '1901', '1851', '1841'],
            'Louth': ['1911', '1901'],
            'Mayo': ['1911', '1901', '1851', '1841', '1821'],
            'Meath': ['1911', '1901', '1851', '1821'],
            'Monaghan': ['1911', '1901', '1851', '1841'],
            'Queens Co': ['1911', '1901'], # referred to differently between year dropdowns
            'Queens': ['1841', '1851'], # referred to differently between year dropdowns
            'Roscommon': ['1911', '1901', '1851'],
            'Sligo': ['1911', '1901', '1851'],
            'Tipperary': ['1911', '1901', '1851'],
            'Tyrone': ['1911', '1901', '1851', '1841'],
            'Waterford': ['1911', '1901',  '1851'],
            'Westmeath': ['1911', '1901', '1841'],
            'Wexford': ['1911', '1901', '1851'],
            'Wicklow': ['1911', '1901', '1851', '1841']
        }

        acceptable_county_answers = []

        while True:
            print('\nFor your specified year, the following counties are available:')
            for county, county_years in counties.items():
                if (search_options['Year'] in county_years):
                    print(' ->', county)
                    acceptable_county_answers.append(county)
            county_input = input("Enter the name of a county, type DELETE to remove this parameter from your search, or type CANCEL to cancel input: ")
            county_input_upper = county_input.upper()
            county_input_title = county_input.title()
            if (county_input_upper == 'DELETE'):
                # If user wants to delete this parameter from her search, remove it from the search_options dictionary
                try:
                    search_options.pop('County')
                except:
                    print('\nSearch parameter is not present.')
                break
            elif (county_input_upper == 'CANCEL'):
                break
            elif (county_input_upper != 'CANCEL'):
                if (county_input_title in acceptable_county_answers):
                    # Check if the user has input Queen's or King's Counties, which need to be handled a bit differently
                    if (county_input_title == 'Queens Co'):
                        search_options['County'] = "Queen's Co."
                    elif (county_input_title == 'Kings Co'):
                        search_options['County'] = "King's Co."
                    elif (county_input_title == 'Queens'):
                        search_options['County'] = "Queen's"
                    elif (county_input_title == 'Kings'):
                        search_options['County'] = "King's"
                    else:
                        search_options['County'] = county_input_title
                    break
                else:
                    input('\nInvalid response.')


    # Run get_year() as soon as the program beings
    get_year()

    # Every time through this loop, the user's selected options will be displayed.
    # User will then be prompted to add additional search parameters.
    # Once the user does, the loop repeats until 'GO' is typed.
    while True:
        print('\nYou have selected the following search options:')
        for key, value in search_options.items():
            print(' ->', key + ':', value)
        edit_search = input('Type EDIT to add or remove search parameters, or type GO to run the search: ')
        edit_search = edit_search.upper()

        # If user types 'EDIT', send prompt for additional parameters
        if (edit_search == 'EDIT'):
            print('\nWhich search parameter would you like to edit?')
            # Available parameters for 1901 and 1911
            if(search_options['Year'] == '1901' or search_options['Year'] == '1911'):
                parameter_to_edit = input('Type YEAR, SURNAME, FORENAME, COUNTY, TOWNLAND, DED, AGE, or SEX; or CANCEL: ')
                paramter_to_edit = parameter_to_edit.upper()
                acceptable_parameters = ['YEAR', 'SURNAME', 'FORENAME', 'COUNTY', 'TOWNLAND', 'DED', 'AGE', 'SEX']
            # Available parameters for 1851 and 1841
            elif(search_options['Year'] == '1851' or search_options['Year'] == '1841'):
                parameter_to_edit = input('Type YEAR, SURNAME, FORENAME, COUNTY, BARONY, PARISH, TOWNLAND, FAMILYID, AGE, or SEX; or CANCEL: ')
                paramter_to_edit = parameter_to_edit.upper()
                acceptable_parameters = ['YEAR', 'SURNAME', 'FORENAME', 'COUNTY', 'BARONY', 'PARISH', 'TOWNLAND', 'FAMILYID', 'AGE', 'SEX']
            # Available parameters for 1831
            elif(search_options['Year'] == '1831'):
                parameter_to_edit = input('Type YEAR, SURNAME, FORENAME, COUNTY, BARONY, PARISH, TOWNLAND, or HOUSENUMBER; or CANCEL: ')
                paramter_to_edit = parameter_to_edit.upper()
                acceptable_parameters = ['YEAR', 'SURNAME', 'FORENAME', 'COUNTY', 'BARONY', 'PARISH', 'TOWNLAND', 'HOUSENUMBER']
            # Available parameters for 1821
            elif(search_options['Year'] == '1821'):
                parameter_to_edit = input('Type YEAR, SURNAME, FORENAME, COUNTY, PARISH, TOWNLAND, or HOUSENUMBER, or AGE; or CANCEL: ')
                paramter_to_edit = parameter_to_edit.upper()
                acceptable_parameters = ['YEAR', 'SURNAME', 'FORENAME', 'COUNTY', 'PARISH', 'TOWNLAND', 'HOUSENUMBER', 'AGE']
            if (parameter_to_edit in acceptable_parameters):
                if (parameter_to_edit == 'YEAR'):
                    # Because things change so much between census years, this is necessary
                    print('\nNote that changing the census year will clear all other parameters.')
                    continue_input = input('Continue? Type YES or NO: ')
                    continue_input = continue_input.upper()
                    if (continue_input == 'YES'):
                        search_options = {}
                        get_year()
                elif (parameter_to_edit == 'SURNAME'):
                    get_search_string('Surname')
                elif (parameter_to_edit == 'FORENAME'):
                    get_search_string('Forename')
                elif (parameter_to_edit == 'COUNTY'):
                    get_county()
                elif (parameter_to_edit == 'TOWNLAND'):
                    get_search_string('Townland')
                elif (parameter_to_edit == 'DED'):
                    get_search_string('DED')
                elif (parameter_to_edit == 'AGE'):
                    get_search_int('Age')
                elif(parameter_to_edit == 'SEX'):
                    get_sex()
                elif(parameter_to_edit == 'BARONY'):
                    get_search_string('Barony')
                elif(parameter_to_edit == 'PARISH'):
                    get_search_string('Parish')
                elif (parameter_to_edit == 'HOUSENUMBER'):
                    get_search_int('House Number')
                elif (parameter_to_edit == 'FAMILYID'):
                    get_search_int('Family ID')
        # If user types 'GO', run the search!
        elif (edit_search == 'GO'):
            break
        else:
            print('\nInvalid response.')
    input('\nThis program will now open a new browser window. Please do not close or interact with this new window, or the program may fail to complete. Press any key to begin.')
    run_search(search_options)


###############################################
# STEP 2: OPEN THE BROWSER AND RUN THE SEARCH #
###############################################

def run_search(search_options):

    output_filename = 'irishcensus'
    # Dynamically generate a file name based on search parameters
    for key, value in search_options.items():
        # Best to keep special characters out of the filename
        new_value = str(value)
        new_value = new_value.replace("'", '')
        new_value = new_value.replace('.', '')
        new_value = new_value.replace(' ', '')
        output_filename += '-' + new_value
    
    output_file = open(output_filename + '.csv', 'w')

    try:

        # Open the browser and navigate to the National Archives of Ireland historical census search website
        browser = webdriver.Chrome(executable_path=path_to_chromedriver)
        browser.get('http://www.census.nationalarchives.ie/search/')

        # Get the necessary search elements and store them in variables
        search_year = Select(browser.find_element_by_id('census_year'))
        search_surname = browser.find_element_by_id('surname')
        search_forename = browser.find_element_by_id('forename')
        search_townland = browser.find_element_by_id('address')
        search_submit = browser.find_element_by_css_selector('input[value=Search]')

        # There are different fields, including different county dropdowns, for every census year -- deal with those here
        if (search_options['Year'] == '1911' or search_options['Year'] == '1901'):
            search_county = Select(browser.find_element_by_id('county19011911'))
            search_ded = browser.find_element_by_id('ded')
            search_age = browser.find_element_by_id('age')
            search_sex = Select(browser.find_element_by_id('sex'))
        elif (search_options['Year'] == '1851'):
            search_county = Select(browser.find_element_by_id('county1851'))
            search_age = browser.find_element_by_id('age')
            search_sex = Select(browser.find_element_by_id('sex'))
            search_barony = browser.find_element_by_id('barony')
            search_parish = browser.find_element_by_id('parish')
            search_familyid = browser.find_element_by_id('familyId')
        elif (search_options['Year'] == '1841'):
            search_county = Select(browser.find_element_by_id('county1841'))
            search_age = browser.find_element_by_id('age')
            search_sex = Select(browser.find_element_by_id('sex'))
            search_barony = browser.find_element_by_id('barony')
            search_parish = browser.find_element_by_id('parish')
            search_familyid = browser.find_element_by_id('familyId')
        elif (search_options['Year'] == '1831'):
            search_county = Select(browser.find_element_by_id('county1831'))
            search_barony = browser.find_element_by_id('barony')
            search_parish = browser.find_element_by_id('parish')
            search_housenumber = browser.find_element_by_id('houseNumber')
        elif (search_options['Year'] == '1821'):
            search_county = Select(browser.find_element_by_id('county1821'))
            search_age = browser.find_element_by_id('age')
            search_parish = browser.find_element_by_id('parish')
            search_housenumber = browser.find_element_by_id('houseNumber')

        # Fill in the form according to user search options (or lack thereof)
        search_year.select_by_visible_text(search_options['Year'])
        if ('Surname' in search_options):
            search_surname.send_keys(search_options['Surname'])
        if ('Forename' in search_options):
            search_forename.send_keys(search_options['Forename'])
        if ('County' in search_options):
            search_county.select_by_visible_text(search_options['County'])
        if ('Townland' in search_options):
            search_townland.send_keys(search_options['Townland'])
        if ('DED' in search_options):
            search_ded.send_keys(search_options['DED'])
        if ('Age' in search_options):
            search_age.send_keys(search_options['Age'])
        if ('Sex' in search_options):
            search_sex.select_by_visible_text(search_options['Sex'])
        if ('Barony' in search_options):
            search_barony.send_keys(search_options['Barony'])
        if ('Parish' in search_options):
            search_parish.send_keys(search_options['Parish'])
        if ('Family ID' in search_options):
            search_familyid.send_keys(search_options['Family ID'])
        if ('House Number' in search_options):
            search_housenumber.send_keys(search_options['House Number'])
        search_submit.click()

        # Test to see if the search returned any results
        try:

            # Sort results by surname
            sort_by_surname_link = browser.find_element_by_link_text('Surname')
            sort_by_surname_link.click()

            # Show 100 results at a time
            show_100_results_link = browser.find_element_by_link_text('100')
            show_100_results_link.click()

            # Check "Show all information"
            show_all_information = browser.find_element_by_id('show_all')
            show_all_information.click()

            # Add table column headers as the first line in the output CSV
            table_heads = browser.find_elements_by_tag_name('th')
            header_string = ''
            for head in table_heads:
                head_text = head.text
                header_string += head_text
                header_string += ','
            header_string += '\n'
            output_file.write(header_string)
            print('WRITING TO FILE:', header_string)

            # Iterate through all rows
            while True:
                table_rows = browser.find_elements_by_css_selector('tbody>tr')
                for row in table_rows:
                    columns = row.find_elements_by_tag_name('td')
                    row_string = ''
                    for column in columns:
                        column_text = column.text
                        # CSVs don't play nice with commas! (obviously)
                        # To remedy this, wrap items with commas in quotation marks
                        if (',' in column_text):
                            column_text = '"' + column_text + '"'
                        row_string += column_text
                        row_string += ','
                    row_string += '\n'
                    print('WRITING TO FILE:', row_string)
                    output_file.write(row_string)
                # If there's a "Next 100" link, click it! Otherwise, we're done
                try:
                    next_100_link = browser.find_element_by_link_text('Next 100')
                    next_100_link.click()
                    show_all_information = browser.find_element_by_id('show_all')
                    show_all_information.click()
                except:
                    browser.get('http://www.census.nationalarchives.ie/search/')
                    break

            # Quit browser
            browser.quit()
            print('All done! Check the results in', output_filename)

        except:
            browser.quit()
            print('\nNo results found!')

            no_results_input = input('Type CONTINUE to start over, or anything else to quit the program: ')
            no_results_input = no_results_input.upper()
            if (no_results_input == 'CONTINUE'):
                get_search_options()

    except:
        print('\nUnable to find the Chrome driver from the path_to_chromedriver variable. Please open this script in a text editor and adjust the path_to_chromedriver variable on Line 7 as necessary.')


# Run this function to start the program!
get_search_options()

