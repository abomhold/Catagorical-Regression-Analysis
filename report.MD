# Linear Regression Model of Categorical UW Course Data

## Collection, Processing, and Analysis

## Introduction:

In undergraduate studies, course selection is often a hot topic for debate. Key considerations include identifying
challenging courses, assessing the relative difficulty of different disciplines, and strategically planning the timing
of particularly demanding classes. Traditionally, students have relied on anecdotal advice from senior peers, which,
while valuable, provides a perspective based on personal experience that may not comprehensively represent the academic
environment. This project aims to supplement anecdotal insights with objective data analysis to provide a more rounded
understanding of the factors that influence course difficulty. By analyzing various attributes of courses, such as
department, level, and campus, against the historical grade distributions, we seek to identify patterns and trends that
can inform students’ course planning decisions.
<br/><br/>

## Part One: Collection

The first step in the process is to collect the data. In our case there are two sourse that we will pull from, the UW
course cataluoge and the "DawgPath" course database. DawgPath is an internal UW site that contains a GPA distibution as
well other catagorical data. We will start with the course cataloge and use it to scape the department key words for
each course prefix.
This will be used later to leverage word frequincesy as an additonal metric. Then we will need to collect each course
from the DawgPath database.
<br/><br/>

### Course Catalogue

The UW course catalogue offers a wealth of information about course departments, which is crucial for gathering keywords
associated with each course prefix. These keywords will later be instrumental in analyzing word frequencies and deriving
additional metrics for the courses. The UW course catalogue is hosted as a simple HTML page meaning scraping will be
relitivly straight forward espciaaly using the BeautifulSoup package which will allows us to diectly sort through the
HTML by headers reducing complexity. This function constructs URLs for each department listed in the course catalogue
for different campuses. We achive this by pulling the top level campus course catalouge and the selecting all of the
links. We then add any link that matches the Regex pattern for a course URL. This is then return as a list of URLS.This
function constructs URLs for each department listed in the course catalogue for different campuses. Next, the
departmental HTML content is scraped and stored. We then collect all of the words in the department descriptions. We
filter out some of the redundant words and return a list of departments associated with each course prefix.

```python
def build_department_urls():
    # Define the URL suffix for each campus
    campuses = {'crscatb/', 'crscat/', 'crscatt/'}
    urls = {}
    # Loop through each campus to construct department URLs
    for campus in campuses:
        url = HTML_URL_HEADER + campus
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Loop through each link header to find department URLs
        for line in soup.findAll('li'):
            match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
            if match:
                department = match.group().split('.')[0].upper()
                # Store the full URL for each department
                urls[department] = url + match.group()
    return urls


def scrape_and_save_html(urls):
    html_dict = {}
    # Loop through each department URL to scrape its HTML content
    for department, dep_url in urls.items():
        response = requests.get(dep_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Store the prettified HTML content
        html_dict[department] = soup.prettify()
    return html_dict


def process_department_html(html_dict):
    dep_word_list = {}
    # Process the HTML content to extract department words
    for department, html_content in html_dict.items():
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract and clean the department header text
        dep_string = soup.h1.text.replace('\n', '').replace('   ', '  ').split('  ')
        # Filter out unwanted words
        dep_words = [string for string in dep_string if string and string not in ('UW TACOMA', 'UW BOTHELL')]
        # Store the words for each department
        dep_word_list[department] = dep_words
    return dep_word_list
```

<br/><br/>

### DawgPath Database

DawgPath is an internal University of Washington (UW) website utilized by students and advisors to access historical GPA
distributions and other relevant course data. Interestingly, the JSON data for each course, sourced from DawgPath,
contains more detailed information than what is visible on the website. The data collection process involves
constructing URLs for API requests. Each UW campus has a top-level JSON file listing all courses in its database. The
method involves iterating through each campus, retrieving course codes, and appending them to a standard JSON URL
format. Once complete, each course's JSON is requested and added to a new JSON under the concatenation of the department
prefix and course number. The resulting JSON is ~10826 entries and ~28MB. This structured approach facilitates the
efficient gathering of course information from DawgPath for our analysis.

```python
# Function to retrieve all courses stored in the database
def get_courses():
    # Define the campuses to fetch course data for
    campuses = {'seattle', 'tacoma', 'bothell'}
    courses = []
    # Loop through each campus
    for campus in campuses:
        # Construct the URL for the API call
        response = requests.get(f'{JSON_URL_HEADER}{campus}', cookies=cookie_jar)
        # Evaluate the text response to Python list
        courses += eval(response.text)
    return courses


# Function to build course URLs 
def build_urls(courses):
    urls = {}
    # Loop through each course to construct its URL
    for course in courses:
        key = course['key']
        url = f'{JSON_URL_HEADER}{key}'
        # Extract course prefix and number
        prefix, number = key[:-3].replace(' ', ''), key.split(' ')[-1]
        # Store the full URL with the course key
        urls[prefix + number] = url
    return urls


# Function to fetch course data in JSON format from URLs
def get_jsons(urls):
    raw_jsons = {}
    # Loop through each URL and fetch the JSON data
    for key, url in urls.items():
        response = requests.get(url, cookies=cookie_jar)
        # Parse the JSON response
        raw_jsons[key] = json.loads(response.text)
        # Log output as working to a file in case of interruptions 
        print(key, raw_jsons[key], file=log_file)
    return raw_jsons
```

<br/><br/>

## Part 2: Processing

In this second phase of our work, we concentrate on refining the collected data to improve its usability and efficiency
for analysis. This involves a series of steps aimed at streamlining the dataset for better performance in subsequent
processing and to work towards a format that our eventual model will understand.
<br/><br/>

### Remove Extra Data

Now that the data is collected, we must turn it into something usable. To start, we need to reduce the size of the
dataset. Removing the extra data upfront will reduce the time cost of the later functions. First, we removed all of the
courses that returned errors. It only eliminates ~9 classes, meaning the data set is pretty clean, and the scraping
process worked as intended. We also removed extra information we didn't need from the prereq data field. The most
significant removal is the extraction of only courses with GPA distribution, which eliminates ~4100 entries. Since our
course data will be compared to the grades, we don't want any classes that don't give grades.

```python
def remove_errors(data):
    # Remove courses from the dataset that contain a specific error pattern.
    # Searches for courses with an error message matching the pattern '.*Course.*'.
    courses_to_remove = [course for course in data if re.search('.*Course.*', str(data[course]['error']))]
    for course in courses_to_remove:
        print(f'REMOVING COURSE: {course}')
        del data[course]
    return data


def remove_options(data):
    # If 'prereq_graph' is present, deletes the 'options' key from it.
    for course, row in data.iterrows():
        graph = row.get('prereq_graph', {})
        if graph is not None:
            print(f'REMOVING FOR COURSE: {course}')
            del graph['x']['options']
    return data


def get_gpa_courses(data):
    # Identifies courses 'gpa_distro' is empty or has a total count of 0.
    # Iterates through the dataset and deletes such courses.
    courses_to_remove = [course for course in data if not data[course]['gpa_distro'] or
                         sum(grade['count'] for grade in data[course]['gpa_distro']) == 0]
    for course in courses_to_remove:
        print(f'REMOVING COURSE: {course}')
        del data[course]
    return data
```

<br/><br/>

### Clean  Data

The data cleaning and feature extraction for the course dataset involved key steps to enhance analysis. Initially, we
calculated and added 'percent_mastered' to the DataFrame, representing the percentage of grades above a GPA of 30. We
then standardized the course levels by rounding down each course's identifier to the nearest hundred.

```python
def percent_mastered(data):
    # Calculate the percentage of high grades (GPA >= 3.0)
    data['percent_mastered'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] for grade in distro if int(grade['gpa']) >= 30) / sum(
            grade['count'] for grade in distro) if distro else 0)  # Set to 0 if no distribution available
    return data


def add_level(data):
    # Deduce course level from course_id and add as new column
    data['course_level'] = data['course_id'].apply(lambda x: int(x[-3:]) // 100 * 100)  # Rounds down to nearest hundred
    return data
```

Subsequently, we flattened the 'coi_data' from each course, creating separate columns like 'course_coi', '
course_level_coi', 'curric_coi', and 'percent_in_range' for analyzing course complexity and curriculum aspects. The '
concurrent_courses' data was processed to identify common course pairings and student course load, and we added columns
indicating prerequisites and subsequent courses to understand curriculum progression.

```python
def flatten_coi_data(data):
    # Extract complexity of information (COI) data and add as new columns
    # Initialize lists for each new column
    course_coi, course_level_coi, curric_coi, percent_in_range = [], [], [], []
    for index, row in data.iterrows():
        coi_data = row.get('coi_data', {})
        # Append COI data, or None if missing
        course_coi.append(coi_data.get('course_coi'))
        course_level_coi.append(coi_data.get('course_level_coi'))
        curric_coi.append(coi_data.get('curric_coi'))
        percent_in_range.append(coi_data.get('percent_in_range'))
    # Add new columns to DataFrame
    data['course_coi'], data['course_level_coi'], data['curric_coi'], data[
        'percent_in_range'] = course_coi, course_level_coi, curric_coi, percent_in_range
    return data


def flatten_concurrent_courses(data):
    # Create a set of concurrent courses, ensuring each key is space-free
    courses = []
    for index, row in data.iterrows():
        concurrent_courses = row.get('concurrent_courses')
        # Create a set of courses without spaces, or None if missing
        fixed_set = {key.replace(' ', '') for key in concurrent_courses.keys()} if concurrent_courses else None
        courses.append(fixed_set)
    data['concurrent_courses'] = courses
    return data


def flatten_prereq(data):
    # Add prerequisite relationship data as new columns
    has_prereq_of, is_prereq_for = [], []
    for index, row in data.iterrows():
        prereq_graph = row.get('prereq_graph')
        self_course_id = row.get('course_id')
        # Generate sets for courses that are prerequisites or have this course as a prerequisite
        has_set = {course.replace(' ', '') for course in
                   prereq_graph.get('x', {}).get('edges', {}).get('from', {}).values() if
                   course != self_course_id} if prereq_graph else None
        is_set = {course.replace(' ', '') for course in
                  prereq_graph.get('x', {}).get('edges', {}).get('to', {}).values() if
                  course != self_course_id} if prereq_graph else None
        has_prereq_of.append(has_set)
        is_prereq_for.append(is_set)
    data['has_prereq'], data['is_prereq'] = has_prereq_of, is_prereq_for
    return data
```

We then tackled the 'course_offered' data for each course. By extracting the quarters
in which each course is available, we added a new column, 'course_offered', to the DataFrame. This column holds a set of
quarters specific to each course. We also accommodated special cases, such as jointly offered courses and entries split
by ';'. Where 'course_offered' data was unavailable or lacked specific quarter information, we assigned None.

```python
def flatten_course_offered(data):
    # Extract quarters when courses are offered and add as new column
    offered, quarter_mapping = [], {'A': 'autumn', 'W': 'winter', 'Sp': 'spring', 'S': 'summer'}
    for index in data.index:
        line = data.loc[index]['course_offered']
        quarter_set = set()
        # Map abbreviation to full quarter name, add None if missing
        if line:
            if 'jointly' in line:
                line = line.split(';')[1].strip() if ';' in line else ''
            for abbrev in quarter_mapping:
                if abbrev in line:
                    quarter_set.add(quarter_mapping[abbrev])
            if not line:
                quarter_set.add(None)
        else:
            quarter_set.add(None)
        offered.append(quarter_set)
    data['course_offered'] = offered
    return data
```

Next, we refined the 'course_description' for each course. By removing prepositions, short words, and numeric terms, we
created a new 'course_description' column in the DataFrame with clean and concise descriptions. This involved breaking
down each description into individual words and filtering them based on length as an easy way to ensure a focus on
substantial, course-relevant content.

```python
def flatten_description(data):
    # Clean and process course descriptions
    prepositions = {'aboard', 'about', 'above', ...}  # List of prepositions to exclude
    for course in data.index:
        course_description = data.loc[course, 'course_description']
        if course_description:
            # Remove punctuation, split into words, and filter based on length and type
            words = set(word for word in course_description.split() if
                        word.lower() not in prepositions and len(word) > 4 and not word.isdigit())
        else:
            words = {None}
        data.at[course, 'course_description'] = words
    return data
```

Furthermore, we mapped each course to its respective departments using a pre-constructed dictionary derived from
scraping the course catalogue. Using the 'course_abbrev' column, we added a set of department strings to each course
entry. Lastly, we removed all the columns from which we had extracted data and no longer needed. This approach of
continuous data trimming helps in reducing runtime and minimize errors.

```python
def add_departments(data):
    # Map courses to their departments
    with open('./files/departments.pkl', 'rb') as handle:
        dep_dict = pickle.load(handle)
    dep_list = []
    for course in data.index:
        key = data.loc[course, 'department_abbrev'].replace(' ', '')
    # Use department dictionary to map courses, add None if not found
    dep_list.append(set(dep_dict.get(key, {None})))
    data['departments'] = dep_list
    return data


def remove_extra_columns(data):
    # Remove columns that are no longer needed from DataFrame
    for column in ['coi_data', 'gpa_distro', 'prereq_graph', 'prereq_string']:
        if column in data.columns:
            del data[column]  # Delete column if it exists
    return data
```

All of the data in our dataframe is now completely machine-readable and easy to manipulate, we need to do one more phase
of cleaning to format the data in a format that is relevant to our model.
<br/><br/>

### Prepare Data

We need to refine and prepare our DataFrame for analysis within a machine learning framework. This requires that We


start with the calculate_mean_level function, where we
calculate the average level of concurrent courses. This involves extracting the last three digits from each course code,
assuming they represent the course level, multiplying them by 100, and then computing their mean, rounding off to the
nearest hundred. In cases where the concurrent courses list is either empty or contains None, our function is designed
to return None.

Next, we employ the get_words function to delve into the 'course_description' and 'course_title' columns of our
DataFrame. Here, we are extracting words and counting their frequencies. Our aim is to identify the top x most frequent
words, and then we create a new DataFrame that marks the presence of these top words in the course descriptions and
titles.

Subsequently, we focus on handling NaN values in our dataset. We fill NaN entries in specific columns - 'course_coi', '
course_level_coi', 'curric_coi', and 'percent_in_range' - with the mean values of those columns. We also extract
numerical values from the 'course_credits' column and convert them into floats. Additionally, we process the '
course_title' column to retain only words that are longer than four characters.

Further enhancing our DataFrame, we add a new column, 'mean_concur_level', which we calculate using our
calculate_mean_level function. We also categorize courses into STEM and Humanities based on their departmental
affiliations.

In analyzing seasonal offerings of courses, we create new columns for each season. These columns indicate whether a
course is offered in that particular season. We also process the 'has_prereq' column to check if the courses have
prerequisites.

Moreover, we reapply the get_words function to extract the top 100 words for a more in-depth analysis. We also create
dummy variables for different campuses, adding to the richness of our dataset.

Finally, we assemble a comprehensive set of features for our predictive model. This includes various columns from our
DataFrame, along with the newly created dummy variables and word columns. We designate 'percent_mastered' as our target
variable, presumably to predict or analyze the success rate or mastery level in the courses. Through these meticulous
steps, we are preparing a robust dataset that is primed for a sophisticated and insightful analysis.

```python
def calculate_mean_level(concurrent_courses):
    if not concurrent_courses or None in concurrent_courses:
        return None
    levels = [int(course[-3]) * 100 for course in concurrent_courses]
    # levels = [level for level in levels if level is not None]  # Filter out None values
    mean_level = round(sum(levels) / len(levels), -2)  # Round to nearest 100
    return mean_level


def get_words(x):
    all_words = [word for description in df['course_description'] for word in description]
    all_words += [word for description in df['course_title'] for word in description]
    # Count the frequency of each word
    word_counts = Counter(all_words)
    # Identify the top 10 most frequent words
    top_words = [word for word, count in word_counts.most_common(x)]
    # Assuming 'top_10_words' is a list of words you want to add as columns
    top_word_columns = {}
    for word in top_words:
        column_name = f"word_{word}"
        top_word_columns[column_name] = df.apply(
            lambda row: word in row['course_description'] or word in row['course_title'], axis=1)
    return pd.DataFrame(top_word_columns)


# Fill NaN values with the mean of each column
df['course_coi'].fillna(df['course_coi'].mean(), inplace=True)
df['course_level_coi'].fillna(df['course_level_coi'].mean(), inplace=True)
df['curric_coi'].fillna(df['curric_coi'].mean(), inplace=True)
df['percent_in_range'].fillna(df['percent_in_range'].mean(), inplace=True)

# Extract and convert 'course_credits' to float
df['course_credits'] = df['course_credits'].str.extract('(\d+\.?\d*)').astype(float)
df['course_title'] = df['course_title'].apply(lambda title: ' '.join([word for word in title.split() if len(word) > 4]))

df['mean_concur_level'] = df['concurrent_courses'].apply(calculate_mean_level)
df['mean_concur_level'].fillna(int(df['mean_concur_level'].mean() / 100) * 100, inplace=True)

df['is_stem'] = df['departments'].apply(lambda depts: any(dept in stem_departments for dept in depts))
df['is_humanities'] = df['departments'].apply(lambda depts: any(dept in humanities_departments for dept in depts))

seasons = set.union(*df['course_offered'])
for season in seasons:
    df[f'offered_{season}'] = df['course_offered'].apply(lambda x: season in x)

df['has_prereq'] = df['has_prereq'].apply(lambda x: None not in x)
df['course_title'] = df['course_title'].apply(lambda title: {word for word in title.split() if len(word) > 4})

new_columns_df = get_words(100)
campus_dummies = pd.get_dummies(df['course_campus'], drop_first=True)

# Combine all features for the model
# Assign X
x = df[['is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'offered_winter', 'offered_summer',
        'offered_spring', 'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level', 'course_coi',
        'course_level_coi', 'curric_coi', 'percent_in_range']].copy()
x = pd.concat([x, campus_dummies, new_columns_df], axis=1)
# Assign Y
y = df['percent_mastered']
```

### Part 3: Analysis