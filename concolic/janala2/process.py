import os

eq1a = []
eq1b = []
eq2a = []
eq2b = []

if __name__ == '__main__':
    with open("time.txt") as f:
        lines = f.readlines()
        current = eq1a
        for l in lines:
            if "equiv1b" in l:
                current = eq1b
            if "equiv2a" in l:
                current = eq2a
            if "equiv2b" in l:
                current = eq2b
            if l.startswith("real"):
                t_str = l[4:].strip()
                minute = float(t_str[0])
                sec = float(t_str[2:-1])
                current.append(round(minute * 60 + sec, 2))

        for i in range(len(eq1a)):
            print("{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"true\" }},".format((i + 1) * 10 , eq2a[i]))
            print("{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"false\"  }},".format((i + 1) * 10, eq2b[i]))
            #print("{{ \"size\" : {}, \"time\": {}  }},".format(i * 10, eq2a[i]))
            #print("{{ \"size\" : {}, \"time\": {}  }},".format(i * 10, eq2b[i]))
        print(eq1a)
        print(eq1b)
        print(eq2a)
        print(eq2b)
