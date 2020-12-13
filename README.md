# LinkedIn Connections Analyzer
### Web Scraping | Data Analysis | Web Development
Designed a web scraping script in Python using Selenium and Beautiful Soup libraries to extract
information of all the LinkedIn connections of the user, transformed the collected data and
performed basic data analysis on the synthesized data. Then developed a web application dashboard
using dash framework to present the findings of the analysis.
As can be observed above, the project is divided into 3 parts:

## 1. Web Scraping
Used the Selenium and Beautiful Soup libraries to perform web scraping to extract information from LinkedIn users' profiles. Used 3 methods: login, connections_scraper and profile_scraper. These were divided into 3 dataframes: connections_data, education and experience.

<strong>connections_data:</strong> Extracted Name, Title, Location, Profile, Number of connections, Number of Projects, Number of Languages known and Top Skills for the connections_data.

<strong>education:</strong> Extracted Institute, Degree and Year range for education.

<strong>experience:</strong> Extracted Profile, Position, Company, Duration for the experience dataframe.

### 2. Data Pre-processing/ Transformation
The collected data was in a raw form and had to be cleaned and transformed for it to be analysed and gained insights from. There are 3 dataframes namely: connections_data, experience and education.

For the connections_data dataframe, cleaned the Location column to just display the City name without the words like 'Area', divided Number of Connections into 6 categories of range such as 0-100, 100-200,... to 500+, Number of Languages, Number of Projects and created a dictionary for the Top 3 featured Skills of each of the connections and then finally counting the number of people for each skill.

For the education dataframe, on the basis of the institute and degree name classified the field of study into 3 categories (for the time being, for simplicity): Science, Management and Arts, found out the status of education on the basis of the year range provided on the profile for a particular education level. Also found out the the highest level of education for the connections based on the words 'Bachelor's', 'Master's' etc given in the education field on the profile.

For the experience dataframe, divided the position column into 3 categories: full time, interns, student representatives or volunteers, made 6 categories under the duration column starting with <6 months to 20+ years.

### 3. Visulization of the transformed data on Dash Framework using Plotly Express
Dash is the most downloaded, trusted framework for building ML & data science web apps. Full stack apps that would typically require a front-end, backend, and dev ops team can now be built and deployed in hours by data scientists with Dash. With Dash Open Source, Dash apps run on your local laptop or workstation, but cannot be easily accessed by others in your organization. To read more and understand Dash, visit https://plotly.com/dash/

Plotly's Python graphing library makes interactive, publication-quality graphs. The plotly.express module (usually imported as px) contains functions that can create entire figures at once, and is referred to as Plotly Express or PX. Plotly Express is a built-in part of the plotly library, and is the recommended starting point for creating most common figures. To know more about plotly, visit https://plotly.com/python/

Since this is the first time we have used Dash, the dashboard looks fairly simple (consisting of interactive bar charts and pie charts with tiles and tree maps), yet very informative. We plan to incorporate more changes with respect to intricacies in the level or field of study/work later.

Note: It's important to have the assets folder in the same folder you implement your application in, since it's necessary for the stlying purposes.


### Screenshots:
<img src='screenshots/screenshot%201.png' >
<img src='screenshots/screenshot%202.png' >
<img src='screenshots/screenshot%203.png' >
