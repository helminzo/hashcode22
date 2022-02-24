data = ""
filename = "a_an_example.in.txt"
with open("./input_files/"+filename) as file:
    data = file.read()
data = data.split('\n') #array of lines

contributor_count, project_count = data[0].split(' ') #contains the total number of contributors and projects

data = data[1:] #discarding the first line

# print(contributor_count,project_count)
contributors = dict() #contains the contributor objects 
projects = dict() #containes the project objects 


## discard name variable?
class Contributor:
    name = ""
    skills = dict()
    def __init__(self,_name:str,_skills:list):
        self.name = _name
        self.skills = _skills

class Project:
    name = ""
    skills = dict()
    duration = 0
    best_before = 0
    def __init__(self, _name:str,_skills:list,_duration:int,_best_before:int, _score:int):
        self.score = _score
        self.name = _name
        self.skills = _skills
        self.duration = _duration
        self.best_before = _best_before

person = 0;
for i in range(int(contributor_count)):
    name, skill_count = data[person].split(' ')
    skill_count = int(skill_count)
    skill_arr = []
    for skill_no in range(skill_count):
        skill, level = data[person+skill_no+1].split(' ')
        skill_arr.append([skill,int(level)])
    
    person += skill_count+1
    contributors[name] = Contributor(name,skill_arr)

data = data[person:]

project_no = 0
for i in range(int(project_count)):
    project, duration, score, best_before, role_count = data[project_no].split(' ')
    skill_arr = []
    role_count = int(role_count)
    for skill_no in range(1,role_count+1):
        skill, level = data[project_no + skill_no].split(' ')
        skill_arr.append([skill,int(level)])
    projects[project] = Project(project,skill_arr,duration,best_before,score)
    project_no += role_count+1
    
# print(projects['WebChat'].skills)