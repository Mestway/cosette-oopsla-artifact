import os
import sys
import argparse
from pprint import pprint

from tabulate import tabulate

def calculate_table_size(input_dir):

    case_table_size = {}

    for fname in os.listdir(input_dir):
        if fname.endswith('.rkt') and (not fname.startswith("__")):
            case_name = fname.split(".")[0]
            with open(os.path.join(input_dir, fname), "r") as f:
                lines = [l for l in f.readlines() if "table-info" in l]
                 
                table_size = []
                for l in lines:
                    table_size.append(len(l[l.index("(list")+ 5:-4].split()))

                case_table_size[case_name] = table_size

    return case_table_size

def parse_outputs(log_dirs, table_size_dict={}, return_all=False):

    method_results = {}

    all_cases = []

    for log_dir in log_dirs:
        record = {}
        for fname in os.listdir(log_dir):
            case_name = fname.split(".")[0]
            all_cases.append(case_name)
            #print(case_name)
            #print(table_size_dict[case_name])
            case_result = []
            with open(os.path.join(log_dir, fname), encoding='utf-8') as f: 
                lines = [l.strip() for l in f.readlines() if "[table size]" in l]
                for l in lines:
                    
                    table_size = l[l.index("[table size]")+len("[table size]")+2: l.index("[real time]")-2]
                    real_time = int(l[l.index("[real time]")+len("[read time]"): l.index("ms")])

                    table_size = [int(i) for i in table_size.split()]

                    #if max(table_size) > 1:
                        #print (case_name)
                        #print(table_size)

                    case_result.append((table_size, real_time))

            record[case_name] = case_result
        method_results[log_dir] = record

    all_cases = list(set(all_cases))
    speed_up = []

    result = []

    for case in all_cases:
        records = []
        record_lens = []

        for method in method_results:
            record_lens.append(len(method_results[method][case]))

        if min(record_lens) == 0:
            continue

        for method in method_results:
            records.append(method_results[method][case][min(record_lens)-1])

        v = float(records[1][1]) / records[0][1]
        #if v > 1:
        #    print(case)
        #    print(v)

        speed_up.append(v)

        num_sv = 0
        for i in range(len(table_size_dict[case])):
            num_sv += records[0][0][i] * table_size_dict[case][i] + (0 if "qex" in log_dir else 1)

        result.append([case, num_sv, records[1][1], records[0][1], float("{:.2}".format(v))])

    def takeSecond(elem):
        return int(elem[4])
    
    return sorted(result, reverse=True, key=takeSecond)
    #print(len(speed_up))
    #print(len([x for x in speed_up if x > 2]))
    #for x in sorted(result, reverse=True, key=takeSecond):
    #    print("{} & {} & {} & {} & {} \\\\".format(x[0], x[1], x[2], x[3], x[4]))


def read_stats(folder, table_size_dict):
    query_size_collector = {}
    schema_size_collector = {}
    aggr_cases = 0
    stats = {}
    for fname in os.listdir(folder):
        #print(fname)
        case_name = fname.split(".")[0]
        full_schema_size = table_size_dict[case_name]
        with open(os.path.join(folder,fname), "r") as f:
            lines = f.readlines()
            aggr = False
            for l in lines:
                if l.startswith("[query size]"):
                    qsize = max([int(x) for x in (l[len("[query size]"):]).split()])
                elif l.startswith("[query aggr]"):
                    if "#t" in l:
                        aggr = True
                elif l.startswith("[table size]"):
                    sz = [int(x) for x in l[l.index("(")+1:l.index(")")].split()]                    
                    tsize = sum([sz[i] * full_schema_size[i] for i in range(len(sz))])
            
            stats[case_name]= (qsize, aggr)
            if aggr:
                aggr_cases += 1
            if qsize not in query_size_collector:
                query_size_collector[qsize] = 0
            query_size_collector[qsize] += 1
            if tsize not in schema_size_collector:
                schema_size_collector[tsize] = 0
            schema_size_collector[tsize] += 1

    return stats
    
def process_case_name(s):
    s = s.replace("test", "").replace("Aggregate", "Aggr").replace("Aggr", "Agg")
    s = s.replace("Grouping", "Group").replace("Constant", "Const").replace("With", "")
    s = s.replace("Inference", "Infer").replace("Conjunct", "Conj").replace("cse344au", "")
    s = s.replace("csep544","").replace("_", "-")
    if s.startswith("-"):
        s = s[1:]
    return s

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Analyze logs.')

    parser.add_argument('--dataset', dest='dataset', action='store', help='Name of the benchmark.', required=True)
    
    parser.add_argument('--benchmark-root', dest='benchmark_root', action='store', 
                        help='The root directory containing benchmarks.', default="benchmarks")
    
    parser.add_argument('--log-root', dest='log_root', action='store', 
                        help='The root directory storing logs.', default="output")

    parser.add_argument('--exclude-aggr', dest='exclude_aggr', action='store_true', 
                        help='Exclude benchmarks with aggregations.', default=False)

    parser.add_argument('--exclude-non-aggr', dest='exclude_non_aggr', action='store_true', 
                        help='Exclude benchmarks without aggregations.', default=False)

    args = parser.parse_args()

    dataset = args.dataset
    exclude_aggr = args.exclude_aggr
    exclude_non_aggr = args.exclude_non_aggr

    dataset_dir = os.path.join(args.benchmark_root, dataset)

    instance1 = [dataset_dir, 
                 os.path.join(args.log_root, f"{dataset}-symbreak"), 
                 os.path.join(args.log_root, f"{dataset}-nosymbreak")]
    instance2 = [dataset_dir, 
                 os.path.join(args.log_root, f"{dataset}-symbreak-qex"), 
                 os.path.join(args.log_root, f"{dataset}-nosymbreak-qex")]

    table_size_dict = calculate_table_size(instance1[0])
    stats = read_stats(instance1[1], table_size_dict)
    result1 = parse_outputs([instance1[1], instance1[2]], table_size_dict)
    result2 = parse_outputs([instance2[1], instance2[2]], table_size_dict)

    def wrap_time(x):
        #return x
        return round(x / 1000., 2)

    result2_dict = {}
    for x in result2:
        result2_dict[x[0]] = x

    header = ["\nName", "\n#subq", "Qex\n#SV", "Qex\nt_S(s)", "Qex\nt_S'(s)", "Qex\nSpeedup", 
              "Cos\n#SV", "Cos\nt_S(s)", "Cos\nt_S'(s)", "Cos\nSpeedup",]
    table = []

    cnt = 0
    for i in range(len(result1)):
        x = result1[i]
        y = result2_dict[x[0]]

        if (exclude_aggr and not stats[x[0]][1]) or (exclude_non_aggr and stats[x[0]][1]):
            continue

        row = [ process_case_name(x[0]), stats[x[0]][0],
                y[1], wrap_time(y[2]), wrap_time(y[3]), y[4],
                x[1], wrap_time(x[2]), wrap_time(x[3]), x[4]]
        
        table.append(row)

        #print("{} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(*row))
        cnt += 1

    # sort based on cosette speedup
    table = sorted(table, key=lambda x: -x[-1])
    print(f"==> Evaluation log for {dataset} dataset, row_num:{cnt}")
    print(tabulate(table, header))


