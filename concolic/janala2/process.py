import os
import sys
import json

eq1a = []
eq1b = []
eq2a = []
eq2b = []

entries = []

vl_spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v2.json",
  "data": {"values": None},
  "mark": "line",
  "encoding": {
    "x": {"field": "table_size (#tuples)", "type": "quantitative"},
    "y": {"field": "time", "type": "quantitative"},
    "color": {"field": "Refinement?", "type": "nominal"}
  }
}

if __name__ == '__main__':
    
    datafile = sys.argv[1] if len(sys.argv) > 1 else "time.txt"

    with open(datafile) as f:
        lines = f.readlines()
        current = []
        for l in lines:
            if len(current) == 10:
                entries.append(current)
                current = []
            if l.startswith("real"):
                t_str = l[4:].strip()
                minute = float(t_str[0])
                sec = float(t_str[2:-1])
                current.append(round(minute * 60 + sec, 2))

        eq1a = entries[0]
        eq1b = entries[1]
        eq2a = entries[2]
        eq2b = entries[3]

        eq1_str =  ",\n".join(["{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"true\" }}".format((i + 1) * 10 , eq1a[i]) for i in range(len(eq1a))])
        eq1_str += ",\n" + ",\n".join(["{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"false\" }}".format((i + 1) * 10 , eq1b[i]) for i in range(len(eq1b))])
        eq1_str = "[" + eq1_str + "]"

        print("##### Vega-Lite Spec for Eq1a and Eq1b")
        print("")
        vl_spec["data"]["values"] = json.loads(eq1_str)
        print(json.dumps(vl_spec))


        eq2_str =  ",\n".join(["{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"true\" }}".format((i + 1) * 10 , eq2a[i]) for i in range(len(eq2a))])
        eq2_str += ",\n" + ",\n".join(["{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"false\" }}".format((i + 1) * 10 , eq2b[i]) for i in range(len(eq2b))])
        eq2_str = "[" + eq2_str + "]"

        print("")
        print("##### Vega-Lite Spec for Eq2a and Eq2b")
        print("")
        
        vl_spec["data"]["values"] = json.loads(eq2_str)
        print(json.dumps(vl_spec))

        #for i in range(len(eq1a)):
        #    print("{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"true\" }},".format((i + 1) * 10 , eq2a[i]))
        #    print("{{ \"table_size (#tuples)\" : {}, \"time\": {}, \"Refinement?\" : \"false\"  }},".format((i + 1) * 10, eq2b[i]))
            #print("{{ \"size\" : {}, \"time\": {}  }},".format(i * 10, eq2a[i]))
            #print("{{ \"size\" : {}, \"time\": {}  }},".format(i * 10, eq2b[i]))
        #print(eq1a)
        #print(eq1b)
        #print(eq2a)
        #print(eq2b)
