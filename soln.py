import hashparser
filename = "b_better_start_small"
contributors, projects = hashparser.parse("input_data/" + filename + ".in.txt")
contributors = [contributors[p] for p in contributors]
projects = [projects[p] for p in projects]
print("Done")

skillMap = {}
for cbtr in contributors:
    for skill in cbtr.skills:
        if(skill not in skillMap):
            skillMap[skill] = [cbtr]
        else:
            skillMap[skill].append(cbtr)
for skill in skillMap:
    skillMap[skill].sort(reverse=True, key= lambda x : x.skills[skill])
print("Created SkillMap")
projects.sort(reverse=True, key= lambda x: x.score / x.duration)
config = []

engaged_until = {}
for cbtr in contributors:
    engaged_until[cbtr.name] = 0

for proj in projects:
    required = proj.skills
    possible = 1
    curr_cbtrs = []
    min_engaged = 0
    for skill, level in required:
        if(skill not in skillMap): 
            possible = 0
            break
        best_cbtr = skillMap[skill][0]
        for possible_cbtr in skillMap[skill]:
            if(possible_cbtr in curr_cbtrs):
                continue
            if possible_cbtr.skills[skill] < level:
                break
            # if engaged_until[possible_cbtr.name] < engaged_until[best_cbtr.name]:
            if possible_cbtr.skills[skill] < best_cbtr.skills[skill]:
                best_cbtr = possible_cbtr
        if(best_cbtr in curr_cbtrs):
            possible = 0
        if(best_cbtr.skills[skill] < level):
            possible = 0
        if(engaged_until[best_cbtr.name] > min_engaged):
            min_engaged = engaged_until[best_cbtr.name]
        curr_cbtrs.append(best_cbtr)
    if(not possible):
        continue
    for cbtr in curr_cbtrs:
        engaged_until[cbtr.name] = min_engaged + proj.duration
    config.append((proj, curr_cbtrs))

print(f"Eval: {hashparser.evaluate(contributors, config)}")
hashparser.dump(config, filename + ".out.txt")
print("Done!")

        