# Task 1:
def func1(name):
    characters={
        "悟空": { "x": 0, "y": 0, "z": 1 },
        "丁滿": { "x": -1, "y": 4, "z": -1 },
        "辛巴": { "x": -3, "y": 3, "z": 1 },
        "貝吉塔": { "x": -4, "y": -1, "z": 1 },
        "特南克斯": { "x": 1, "y": -2, "z": 1 },
        "弗利沙": { "x": 4, "y": -1, "z": -1 },
    }
    def distance(a, b):
        ax,ay,az=characters[a]["x"],characters[a]["y"],characters[a]["z"]
        bx,by,bz=characters[b]["x"],characters[b]["y"],characters[b]["z"]
        result=abs(ax-bx)+abs(ay-by)
        if az!=bz:
            result+=2
        return result
    dist_list=[]
    for other in characters:
        if other!=name:
            d=distance(other,name)
            dist_list.append({"name":other,"distance":d})
    max_dist=max(char["distance"] for char in dist_list)
    farthest=[char["name"] for char in dist_list if char["distance"]==max_dist]
    min_dist=min(char["distance"] for char in dist_list)
    nearest=[char["name"] for char in dist_list if char["distance"]==min_dist]

    print("最遠：",farthest)
    print("最近：",nearest)

func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")

# Task 2:
booked = []
def isOverlap(start1, end1, start2, end2):
    return start1 < end2 and start2 < end1
def isAvailable(s, start, end):
    return not any(
        b["name"]==s["name"]
        and b["available"] is False
        and isOverlap(b["start"], b["end"], start, end) 
        for b in booked
    )
def func2(ss, start, end, criteria):
    field=""
    value=0
    op=""
    if ">=" in criteria:
        field, value=criteria.split(">=")
        op=">="
    elif "<=" in criteria:
        field, value=criteria.split("<=")
        op="<="
    elif "=" in criteria:
        field, value=criteria.split("=")
        op="="

    if field != "name":
        value=float(value)
    
    candidates = []
    for s in ss:
        if op == ">=" and s[field] >= value:
            candidates.append(s)
        elif op == "=" and s[field] == value:
            candidates.append(s)
        elif op == "<=" and s[field] <= value:
            candidates.append(s)

    free=[s for s in candidates if isAvailable(s, start, end)]

    if len(free)==0:
        print("Sorry")
        return
    
    if len(free)==1:
        best=free[0]
    else:
        best=min(free, key=lambda s:abs(s[field] - value))
    print(best["name"])
    booked.append({
        "name":best["name"],
        "start":start,
        "end":end,
        "available":False
    })

services=[{"name":"S1", "r":4.5, "c":1000},
          {"name":"S2", "r":3, "c":1200},
          {"name":"S3", "r":3.8, "c":800}]

func2(services, 15, 17, "c>=800") # S3 
func2(services, 11, 13, "r<=4") # S3 
func2(services, 10, 12, "name=S3") # Sorry 
func2(services, 15, 18, "r>=4.5") # S1 
func2(services, 16, 18, "r>=4") # Sorry 
func2(services, 13, 17, "name=S1") # Sorry 
func2(services, 8, 9, "c<=1500") # S2

# Task 3:
def func3(index):
    addlist=[-2, -3, 1, 2]
    value=25
    for n in range(index):
        value += addlist[n%len(addlist)]
    print(value)
 
func3(1) # print 23
func3(5) # print 21 
func3(10) # print 16 
func3(30) # print 6

# Task 4:
def func4(sp, stat, n):
    fit = []
    for i in range(len(sp)):
        if stat[i]=="0" and sp[i]>=n:
            fit.append((i,sp[i] - n))
    if len(fit)>0:
        best = min(fit, key=lambda x: x[1])
        print(best[0])
        return
    fallback = [(i, sp[i]) for i in range(len(sp)) if stat[i] == "0"]

    if len(fallback)>0:
        best = max(fallback, key=lambda x: x[1])
        print(best[0])
    else:
        print("Sorry")
    
func4([3, 1, 5, 4, 3, 2], "101000", 2) # print 5 
func4([1, 0, 5, 1, 3], "10100", 4) # print 4 
func4([4, 6, 5, 8], "1000", 4) # print 2