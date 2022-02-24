def parse(filename):
    data = ""
    with open(filename) as file:
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
        score = 0
        def __init__(self, _name:str,_skills:list,_duration:int,_best_before:int, _score:int):
            self.score = int(_score)
            self.name = _name
            self.skills = _skills
            self.duration = int(_duration)
            self.best_before = int(_best_before)

    person = 0
    for i in range(int(contributor_count)):
        name, skill_count = data[person].split(' ')
        skill_count = int(skill_count)
        skill_dict = {}
        for skill_no in range(skill_count):
            skill, level = data[person+skill_no+1].split(' ')
            skill_dict[skill] = int(level)
        
        person += skill_count+1
        contributors[name] = Contributor(name,skill_dict)

    data = data[person:]

    project_no = 0
    for i in range(int(project_count)):
        project, duration, score, best_before, role_count = data[project_no].split(' ')
        skill_arr = []
        role_count = int(role_count)
        for skill_no in range(1,role_count+1):
            skill, level = data[project_no + skill_no].split(' ')
            skill_arr.append([skill, int(level)])

        projects[project] = Project(project,skill_arr,duration,best_before,score)
        project_no += role_count+1
    return contributors, projects

def evaluate(contributors, config):
    '''
    config is a list of tuples, where the ith element specifies the 
    ith project taken in order as (project, [list of contributors])
    '''

    score = 0
    engagements = {}
    for cbtr in contributors:
        engagements[cbtr.name] = 0

    #   project, contributors
    for proj, cbtrs in config:
        #Find the earliest day this project can start
        earliest = 0
        for cbtr in cbtrs:
            if(engagements[cbtr.name] > earliest):
                earliest = engagements[cbtr.name]
        for cbtr in cbtrs:
            engagements[cbtr.name] = earliest + proj.duration
        finish_day = earliest + proj.duration
    
        required = proj.skills
        # Check if proj can be carried out by the assigned people
        encountered = []
        for skill, level in required:

            foundCtbr = 0
            for cbtr in cbtrs:
                if (
                    skill in cbtr.skills and 
                    cbtr.skills[skill] >= level and
                    cbtr not in encountered
                ):
                    foundCtbr = 1
                    encountered.append(cbtr)
                    break
            if(foundCtbr == 0):
                print(f"Invalid config. There are no contributors on project {proj.name} that have skill {skill} at level {required[skill]}\n")
                return score

        # Now that we have know that this is a valid project




        # Update the score for the participants.
        score += proj.score - max(0, finish_day - proj.best_before)
    return score

def dump(config, outFileName):
    with open(outFileName, 'w') as f:
        f.write(f"{len(config)}\n")
        for proj, cbtrs in config:
            f.write(f"{proj.name}\n")
            for cbtr in cbtrs:
                f.write(f"{cbtr.name} ")
            f.write("\n")

    