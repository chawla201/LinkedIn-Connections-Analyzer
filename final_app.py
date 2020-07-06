from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
from bs4 import BeautifulSoup
import datetime
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import webbrowser

def login(browser):
    username = input('Enter Username: ')
    password = input('Enter Password: ')
    browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    time.sleep(3)
    browser.find_element_by_name('session_key').send_keys(username + Keys.RETURN)
    browser.find_element_by_name('session_password').send_keys(password + Keys.RETURN)
    time.sleep(3)

def connections_scraper(browser):
    connections_page = "https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH"
    browser.get(connections_page)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    conn_num = soup.find_all('h3', class_='search-results__total')
    num = int(conn_num[0].text.strip().split()[0])
    time.sleep(3)
    i = 2
    x = 1
    names = []
    titles = []
    locations = []
    profiles = []
    print('Scraping your connections...\n')
    while True:
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(.75)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(.75)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(.75)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(.75)
        browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        name_tag = soup.find_all('span', class_='name actor-name')
        title_tag = soup.find_all('p', class_='subline-level-1')
        location_tag = soup.find_all('p', class_= 'subline-level-2')
        profile_tag = soup.find_all('a', class_= 'search-result__result-link')
        names += list(map(lambda x: x.text, name_tag))
        titles += list(map(lambda x: x.text.replace('\n','').strip(), title_tag))
        locations += list(map(lambda x: x.text.replace('\n','').strip(), location_tag))
        profiles += list(map(lambda x: 'https://linkedin.com' + x['href'], profile_tag))[::2]
        if len(names)>=num:
            break
        y = x
        x = len(names)
        if x==y:
            break
        browser.get('https://www.linkedin.com/search/results/people/?facetNetwork=%5B%22F%22%5D&origin=MEMBER_PROFILE_CANNED_SEARCH&page='+str(i))
        i+=1
        time.sleep(3)
    df = pd.DataFrame({'Name':names, 'Title':titles, 'Location':locations, 'Profile':profiles})
    return df

def profile_scraper(df, browser):
    num_projects = []
    num_languages = []
    top_skills = []
    num_connections = []
    positions = []
    company = []
    duration = []
    institutes = []
    courses = []
    year_range = []
    ex_profiles = []
    ed_profiles = []
    print('Extracting information form individual profiles. Please wait...\n')
    for profile in df['Profile']:
        try:
            browser.get(profile)
            time.sleep(2)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            browser.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(.75)
            soup = BeautifulSoup(browser.page_source, 'lxml')

            conn_tag = soup.find_all('span', class_='t-16 t-bold')
            if conn_tag[0].text.strip().split()[0].isdigit() or conn_tag[0].text.strip().split()[0] == '500+':
                num_connections.append(conn_tag[0].text.strip().split()[0])
            elif len(soup.find_all('span', class_='t-16 t-black t-normal'))>0:
                num_connections.append(soup.find_all('span', class_='t-16 t-black t-normal')[0].text.strip().split()[0])
            else:
                num_connections.append(None)

            accom_tag = soup.find_all('h3', class_='pv-accomplishments-block__count t-32 t-black t-normal pr3')
            np = 0
            nl = 2
            for at in accom_tag:
                if at.text.strip().split('\n')[0].split()[-1] == 'projects' or at.text.strip().split('\n')[0].split()[-1] == 'project':
                    np = int(at.text.strip().split('\n')[1])
                if at.text.strip().split('\n')[0].split()[-1] == 'languages' or at.text.strip().split('\n')[0].split()[-1] == 'language':
                    nl = int(at.text.strip().split('\n')[1])
            num_projects.append(np)
            num_languages.append(nl)

            skills_tag = soup.find_all('span', class_='pv-skill-category-entity__name-text')
            ts = []
            for st in skills_tag:
                ts.append(st.text.strip())
            top_skills.append(ts)

            position_tag = soup.find_all('h3', class_='t-16 t-black t-bold')
            ex_pos = list(map(lambda x: x.text.strip(), position_tag))
            company_tag = soup.find_all('p', class_='pv-entity__secondary-title t-14 t-black t-normal')
            ex_comp = list(map(lambda x: x.text.strip().split('\n')[0], company_tag))
            ex_duration_tag = soup.find_all('span', class_='pv-entity__bullet-item-v2')
            durr = []
            for dur in ex_duration_tag:
                d_list = dur.text.strip().split()
                if d_list[0].isdigit():
                    if len(d_list)==2:
                        if d_list[1] == 'mo' or d_list[1]=='mos':
                            durr.append(int(d_list[0]))
                        if d_list[1] == 'yr' or d_list[1]=='yrs':
                            durr.append(int(d_list[0])*12)
                    if len(d_list)==4:
                        durr.append((int(d_list[0])*12)+int(d_list[2]))
                else:
                    durr.append(None)
            x = min(len(ex_comp), len(ex_pos), len(durr))
            ex_comp = ex_comp[:x]
            ex_pos = ex_pos[:x]
            durr = durr[:x]
            ex_profiles += [profile]*x
            positions += ex_pos
            company += ex_comp
            duration += durr

            institute_tag = soup.find_all('h3', class_='pv-entity__school-name t-16 t-black t-bold')
            inst = list(map(lambda x: x.text.strip(), institute_tag))
            course_tag = soup.find_all('p', class_='pv-entity__secondary-title pv-entity__degree-name t-14 t-black t-normal')
            course_t = list(map(lambda x: x.text.strip().split('\n')[1], course_tag))
            ed_date_tag = soup.find_all('p', class_='pv-entity__dates t-14 t-black--light t-normal')
            ed_dates = list(map(lambda x: x.text.strip().split('\n')[-1], ed_date_tag))
            y = min(len(inst), len(course_t), len(ed_dates))
            inst = inst[:y]
            course_t = course_t[:y]
            ed_dates = ed_dates[:y]
            ed_profiles += [profile]*y
            institutes += inst
            courses += course_t
            year_range += ed_dates
        except:
            continue
    df['Number of connections'] = num_connections
    df['Number of Projects'] = num_projects
    df['Number of Languages known'] = num_languages
    df['Top Skills'] = top_skills
    exp_df = pd.DataFrame({'Profile':ex_profiles, 'Position':positions, 'Company':company, 'Duration':duration})
    ed_df = pd.DataFrame({'Profile':ed_profiles, 'Institute':institutes, 'Degree':courses, 'Year range':year_range})
    
    return df, exp_df, ed_df

try:
    conn = pd.read_csv('connections_data.csv')
    exp = pd.read_csv('experience.csv')
    ed = pd.read_csv('education.csv')
except:
    browser = webdriver.Chrome(executable_path="E:/RnD/linkedin_scraper/chromedriver", options= webdriver.ChromeOptions())
    login(browser)
    print('\nPlease Wait. This may take a while...\n')
    time.sleep(3)
    connections = connections_scraper(browser)
    time.sleep(3)
    conn_data, exp_data, ed_data = profile_scraper(connections, browser)
    conn_data.to_csv('connections_data.csv', index=False)
    exp_data.to_csv('experience.csv', index=False)
    ed_data.to_csv('education.csv', index=False)
    browser.quit()
    conn = pd.read_csv('connections_data.csv')
    exp = pd.read_csv('experience.csv')
    ed = pd.read_csv('education.csv')

exp = exp[exp['Position']!='Student']
#conn = conn.drop_duplicates().reset_index(drop=True)
#ed = ed.drop_duplicates().reset_index(drop=True)
#exp = exp.drop_duplicates().reset_index(drop=True)


ed['start_year'] = list(map(lambda x: int(x.split()[0]), ed['Year range']))
end = []
for ran in ed['Year range']:
    try:
        end.append(int(ran.split()[2]))
    except:
        end.append(int(ran.split()[0])+4)
ed['passing_year'] = end

profiles = ed['Profile'].unique()
current_year = datetime.datetime.now().year
hins = []
hdeg = []
hstart = []
hpass = []
status = []
level = []
field = []
for prof in profiles:
    hins.append(ed[ed['Profile']==prof]['Institute'].iloc[0])
    hdeg.append(ed[ed['Profile']==prof]['Degree'].iloc[0])
    hstart.append(ed[ed['Profile']==prof]['start_year'].iloc[0])
    hpass.append(ed[ed['Profile']==prof]['passing_year'].iloc[0])
    if ed[ed['Profile']==prof]['passing_year'].iloc[0]<=current_year:
        status.append('Completed')
    else:
        status.append('Ongoing')
    deg = ed[ed['Profile']==prof]['Degree'].iloc[0]
    if (deg.lower().find('bachelor')!=-1 or deg.lower()[0]=='b'):
        level.append('Bachelor\'s')
    elif (deg.lower().find('master')!=-1 
          or deg.lower().find('post graduate')!=-1 
          or deg.lower()[0]=='m' 
          or deg.lower().find('pgdm')!=-1):
        level.append('Master\'s')
    elif (deg.lower().find('phd')!=-1 or deg.lower().find('Doctor of Philosophy')!=-1):
        level.append('Phd')
    elif (deg.lower().find('nanodegree')!=-1 or deg.lower().find('certificate program')!=-1):
        level.append('Diploma')
    else:
        level.append('Other')
    ins = ed[ed['Profile']==prof]['Institute'].iloc[0]
    if (deg.lower().find('engineer')!=-1 
        or deg.lower().find('technology')!=-1
        or deg.lower().find('science')!=-1 
        or deg.lower().find('computer')!=-1
        or ins.lower().find('technology')!=-1
        or ins.lower().find('science')!=-1
        or ins.lower().find('medical')!=-1
        or ins.lower().find('engineering')!=-1):
        field.append('Science')
    elif(deg.lower().find('management')!=-1 
         or deg.lower().find('mba')!=-1 
         or deg.lower().find('business')!=-1 
         or deg.lower().find('finance')!=-1 
         or deg.lower().find('accountancy')!=-1
         or ins.lower().find('business')!=-1):
        field.append('MNGMT')
    else:
        field.append('Arts')
dic = {'Profile':profiles, 
       'Institute':hins, 
       'Degree':hdeg, 
       'Field of study':field,
       'Level':level,
       'start_year':hstart, 
       'passing_year':hpass,
       'Level':level,
       'Status':status}
highest_ed = pd.DataFrame(dic)

conn_cat = []
skills = []
for ri, row in conn.iterrows():
    if row['Top Skills']!='[]':
        skills.append(row['Top Skills'])
    if row['Number of connections'] == '500+':
        conn_cat.append('500+')
    elif (int(row['Number of connections'])>400 and int(row['Number of connections'])<=500):
        conn_cat.append('400-500')
    elif (int(row['Number of connections'])>300 and int(row['Number of connections'])<=400):
        conn_cat.append('300-400')
    elif (int(row['Number of connections'])>200 and int(row['Number of connections'])<=300):
        conn_cat.append('200-300')
    elif (int(row['Number of connections'])>100 and int(row['Number of connections'])<=200):
        conn_cat.append('100-200')
    elif (int(row['Number of connections'])<=100):
        conn_cat.append('0-100')
conn["Number of connections"] = conn_cat

sk = []
i = 0
for skill in skills:
	try:
		x=skill.split('\'')
		sk.append(x[1])
		try:
			sk.append(x[3])
		except:
			continue
		try:
			sk.append(x[5])
		except:
			continue
	except:
		sk += skill
skills_dict = {}
for skill in sk:
    if skill in skills_dict:
        skills_dict[skill] += 1
    else:
        skills_dict[skill] = 1
lang = []
for k,v in skills_dict.items():
    if k.lower().find('programming language')!=-1:
        lang.append(k)
for l in lang:
    try:
        skills_dict[l.split()[0]] += skills_dict[l]
        del skills_dict[l]
    except:
        continue
x=sorted(skills_dict.values(), reverse=True)
dic = {}
for skill_cnt in x:
    for k,v in skills_dict.items():
        if ((v==skill_cnt) and (k not in dic)):
            dic[k]=skill_cnt
skills_dict = dic

locs = []
for loc in list(conn['Location'].values):
    x = loc.split(',')[0]
    if x.split()[-1] == 'Area':
        locs.append(" ".join(x.split()[:-1]))
    else:
        locs.append(x)
locations = []
for x in locs:
    if x not in locations:
        locations.append(x)
lc = []
for loc in list(conn['Location'].values):
    for l in locations:
        x = loc.split(',')[0]
        if x.find(l)!=-1:
            lc.append(l)
            break
conn['Location'] = lc

dur = []
for index, d in exp.iterrows():
    try:
        if int(d["Duration"]) < 6:
            dur.append('< 6 Months')
        elif int(d["Duration"]) >= 6 and int(d["Duration"]) < 12:
            dur.append('6 Months to 1 Year')
        elif int(d["Duration"]) >= 12 and int(d["Duration"]) <= 60:
            dur.append('1-5 Years')
        elif int(d["Duration"]) > 60 and int(d["Duration"]) <= 120:
            dur.append('6-10 Years')
        elif int(d["Duration"]) > 120 and int(d["Duration"]) <= 240:
            dur.append('11-20 Years')
        else:
            dur.append('20+ Years')
    except:
        dur.append('< 6 Months')
exp["Experience"] = dur

cat = []
for pos in list(exp['Position']):
    if (pos.lower().find('intern')!=-1
        or pos.lower().find('internship')!=-1
        or pos.lower().find('trainee')!=-1):
        cat.append('Intern')
    elif (pos.lower().find('campus')!=-1
          or pos.lower().find('student')!=-1
          or pos.lower().find('teaching assistant')!=-1
          or pos.lower().find('ambassador')!=-1
          or pos.lower().find('college')!=-1
          or pos.lower().find('member')!=-1
          or pos.lower().find('core committee member')!=-1
          or pos.lower().find('volunteer')!=-1
          or pos.lower().find('hustler')!=-1
          or pos.lower().find('scholar')!=-1
          or pos.lower().find('contributor')!=-1
          or pos.lower().find('fest')!=-1
          or pos.lower().find('event')!=-1
          or pos.lower().find('representative')!=-1):
        cat.append('Student Representative/ Volunteer')
    else:
        cat.append('Full Time')
exp["Category"] = cat

category_count = pd.DataFrame(exp['Category'].value_counts()).reset_index().rename(columns={'index':'Category', 'Category':'Count'})
intern_company_count = pd.DataFrame(exp[exp['Category']=='Intern']['Company'].value_counts()).reset_index().rename(columns={'index':'Company', 'Company':'Count'})
ft_company_count = pd.DataFrame(exp[exp['Category']=='Full Time']['Company'].value_counts()).reset_index().rename(columns={'index':'Company', 'Company':'Count'})
srv_company_count = pd.DataFrame(exp[exp['Category']=='Student Representative/ Volunteer']['Company'].value_counts()).reset_index().rename(columns={'index':'Company', 'Company':'Count'})

skills_count = pd.DataFrame(columns=['Skill', 'Count'])
skills_count['Skill'] = list(skills_dict.keys())
skills_count['Count'] = list(skills_dict.values())

location_count = pd.DataFrame(conn['Location'].value_counts()).reset_index().rename(columns={'index':'Location', 'Location':'Count'})
exp_dur_count = pd.DataFrame(exp['Experience'].value_counts()).reset_index().rename(columns={'index':'Duration', 'Experience':'Count'})
conn_num_count = pd.DataFrame(conn['Number of connections'].value_counts()).reset_index().rename(columns={'index':'Number of connections', 'Number of connections':'Count'})
lang_count = pd.DataFrame(conn['Number of Languages known'].value_counts()).reset_index().rename(columns={'index':'Number of Languages known', 'Number of Languages known':'Count'})

intern_company_count['Category'] = ['Intern']*intern_company_count.shape[0]
intern_company_count['Category count'] = [category_count['Count'].iloc[1]]*intern_company_count.shape[0]
ft_company_count['Category'] = ['Full Time']*ft_company_count.shape[0]
ft_company_count['Category count'] = [category_count['Count'].iloc[0]]*ft_company_count.shape[0]
srv_company_count['Category'] = ['Student Representative/ Volunteer']*srv_company_count.shape[0]
srv_company_count['Category count'] = [category_count['Count'].iloc[2]]*srv_company_count.shape[0]

status_count = pd.DataFrame(highest_ed['Status'].value_counts().reset_index().rename(columns={'index':'category name', 'Status':'Count'}))
level_count = pd.DataFrame(highest_ed['Level'].value_counts().reset_index().rename(columns={'index':'category name', 'Level':'Count'}))
fos_count = pd.DataFrame(highest_ed['Field of study'].value_counts().reset_index().rename(columns={'index':'category name', 'Field of study':'Count'}))

category_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(category_count['Count']))), category_count['Count']))
intern_company_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(intern_company_count['Count']))), intern_company_count['Count'])) 
ft_company_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(ft_company_count['Count']))), ft_company_count['Count'])) 
srv_company_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(srv_company_count['Count']))), srv_company_count['Count']))
skills_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(skills_count['Count']))), skills_count['Count']))
location_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(location_count['Count']))), location_count['Count']))
exp_dur_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(exp_dur_count['Count']))), exp_dur_count['Count'])) 
conn_num_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(conn_num_count['Count']))), conn_num_count['Count'])) 
lang_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(lang_count['Count']))), lang_count['Count']))
status_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(status_count['Count']))), status_count['Count'])) 
level_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(level_count['Count']))), level_count['Count'])) 
fos_count['Count %'] = list(map(lambda x: '%.2f'%(x*100/sum(list(fos_count['Count']))), fos_count['Count']))

tt_int = int(len(intern_company_count)*0.1)
tt_ft = int(len(ft_company_count)*0.1)
tt_srv = int(len(srv_company_count)*0.1)

company_count = intern_company_count[:tt_int].append(ft_company_count[:tt_ft]).append(srv_company_count[:tt_srv])

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
                html.Div([
            html.H1(children='LinkedIn Connections Analyzer with Visualization',style={'textAlign': 'center'}),
            html.Div([
            html.H6(children=
              'LinkedIn has always been one of the most useful social media networks for us. The reason is simple: it is business-oriented and (almost) clutter-free.The best thing is that people are connected for a reason there: when sending a connection request, you can/need to specify how you are connected to a person. This way your network contains a wealth of business-oriented information: you can find out how you are related to any company or person you need to get in touch with. Alternatively, you can be introduced to anyone outside your immediate network using your first-level connections.Tapping into your Linkedin connections can be a great way to discover new career opportunities for personal and professional growth.',
              style={'textAlign': 'center', 'margin-bottom':'25px'})
            ])
                    ])
            ], className='title twelve columns')
        ], id='header', className='title', style={'margin-bottom':'25px', 'margin-top':'0px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='location_graph',
                figure=px.treemap(location_count,path=['Location'], values='Count %', title='Demographic Distribution of Connections', color='Count', color_continuous_scale=['#AED6F1', '#3498DB']).update_layout(title_x=0.5, coloraxis_showscale=False)
                )], className='contain six columns'
            ),
        html.Div([
            dcc.Graph(id='skills_graph',
                figure=px.bar(skills_count[:10][::-1], x= 'Count %', y='Skill', title='Most Popular Skills amongst your Connections', orientation='h', color='Count', color_continuous_scale=['#AED6F1', '#3498DB']).update_layout(title_x=0.5, coloraxis_showscale=False)
                )], className='contain six columns'
            )
    ], className='row', id='row1', style={'margin-bottom':'10px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='conn_graph',
                figure=px.bar(conn_num_count[::-1], y='Number of connections', x = 'Count %', range_x=[0, 100], title='Network Strength of your Connections', orientation='h',color='Count', color_continuous_scale=['#AED6F1', '#3498DB']).update_layout(title_x=0.5, coloraxis_showscale=False)
                )], className='contain five columns'
            ),
        html.Div([
            dcc.Graph(id='lang_graph',
                figure=px.pie(lang_count, names='Number of Languages known', values='Count %', title='Number of Languages known',color ='Number of Languages known', color_discrete_sequence=px.colors.sequential.Blues[-9:-3][::-1]).update_layout(title_x=0.5)
                )], className='contain five columns'
            ),
        html.Div([
            html.Div([
                html.H6('%.2f'%exp[exp['Category']=='Intern']['Duration'].mean()),
                html.P('Average Duration of Internships (in Months)')
                ], className='mini_container', style={'margin-bottom':'20px', 'margin-top':'20px'}),
            html.Div([
                html.H6('%.2f'%((len(exp[exp['Category']=='Intern'])/len(exp))*100)+'%'),
                html.P('Connections who have worked as interns')
                ], className='mini_container', style={'margin-bottom':'20px'}),
            html.Div([
                html.H6('%.2f'%((len(exp[exp['Category']=='Full Time'])/len(exp))*100)+'%'),
                html.P('Connections who have worked full time')
                ], className='mini_container')
            ], className='two columns')
    ], className='row', id='row2', style={'margin-bottom':'10px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='cat_comp_tree',
                    figure=px.treemap(company_count,path=['Category', 'Company'], values='Count %', title='Popular Companies in Each Category', color='Category', color_discrete_map={'Full Time':'#3498DB', 'Intern':'#85C1E9', 'Student Representative/ Volunteer':'#AED6F1'}).update_layout(title_x=0.5))
            ], className='contain six columns'),
        html.Div([
            dcc.Graph(id='duration_plot',
                    figure= px.bar(exp_dur_count[::-1], y='Duration', x='Count %', title='Duration of the Job', orientation='h',color='Count', color_continuous_scale=['#AED6F1', '#3498DB'], range_x=[0, 100]).update_layout(title_x=0.5,coloraxis_showscale=False)
                    )], className='contain six columns')
    ], className='row', id='row3', style={'margin-bottom':'10px'}),
    html.Div([
        html.Div([
            dcc.Graph(id='fos_plot',
                    figure=px.pie(fos_count, names='category name', values='Count %', title='Field of Study',color ='category name',color_discrete_sequence=px.colors.sequential.Blues[-9:-3][::-1]).update_layout(title_x=0.5))
            ], className='contain four columns', style={'margin-right':'12px', 'margin-left':'10px'}),
        html.Div([
            dcc.Graph(id='level_plot',
                    figure=px.pie(level_count, names='category name', values='Count %', title='Level of Highest Education',color='category name',color_discrete_sequence=px.colors.sequential.Blues[-9:-3][::-1]).update_layout(title_x=0.5))
            ], className='contain four columns', style={'margin-right':'12px'}),
        html.Div([
            dcc.Graph(id='status_plot',
                    figure=px.pie(status_count, names='category name', values='Count %', title='Status of Education',color='category name',color_discrete_sequence=px.colors.sequential.Blues[-9:-3][::-1]).update_layout(title_x=0.5))
            ], className='contain four columns')
    ], className='row', id='row4', style={'margin-bottom':'10px'})
])

webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s').open('http://127.0.0.1:8050/')

if __name__ == '__main__':
    app.run_server(debug=True)

