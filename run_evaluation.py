# prepare rosette benchmarks for the purpose of testing rosette solver
import time
import os
import json
import csv
from subprocess import Popen, PIPE, STDOUT, check_output
import signal
import argparse

from pprint import pprint

import solver
import sys

def quick_parse(input_file):
    with open(input_file, "r") as f:
        content = "\n".join(f.readlines())
        status, rosette_file = solver.gen_rosette(content, ".")
        return status, rosette_file


def prepare_calcite_benchmarks(input_dir, output_dir):    
    # get already generated rules, since some of them may be edited
    generated_rules = {}
    for filename in os.listdir(input_dir):
        if filename.endswith(".cos"):
            case_name = filename[:-4]
            with open(os.path.join(input_dir, filename), 'r') as source_file:
                cos = source_file.read()
                generated_rules[case_name] = cos

    labels = {}
    with open(os.path.join(input_dir, "rosette_supported.csv")) as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            name = row[0]
            labels[name] = True if row[1] == "T" else False

    for fname in os.listdir(input_dir):
        case_name = fname.split(".")[0]

        if fname.endswith(".cos") and labels[case_name]:
            status, ros_file = quick_parse(os.path.join(input_dir, fname))

            if status == True:
                with open(os.path.join(output_dir, case_name + ".rkt"), "w") as out_file:
                    out_file.write(ros_file)


def prepare_hw_benchmarks(input_dir, output_dir):
    # prepare hw benchmarks for evaluation
    for filename in os.listdir(input_dir):
        if filename.endswith(".cos"):
            case_name = filename[:-4]
            with open(os.path.join(input_dir, filename), "r") as f:
                content = "\n".join(f.readlines())
                status, rosette_file = solver.gen_rosette(content, ".")

                if status == True:
                    with open(os.path.join(output_dir, case_name + ".rkt"), "w") as out_file:
                        out_file.write(rosette_file)
                else:
                    print(case_name)


def run_equiv_check_benchmarks(input_dir, cosette_dir, log_dir, 
                               time_limit, symbreak, qex_enc, simplify=True):

    def run_equiv_check(rosette_file):

        flags = ""
        flags += " --symbreak" if symbreak else ""
        flags += " --qex-enc" if qex_enc else ""
        flags += " --simplify" if simplify else ""

        case_name = os.path.splitext(os.path.basename(rosette_file))[0]
        cmd_ros = 'cd {}; ./rosette_solve.sh {} {} {}'.format(cosette_dir, rosette_file, time_limit, flags)

        if log_dir:
            log_file = os.path.join(log_dir, case_name + ".log")
            cmd_ros += " > {}".format(log_file)

        proc = Popen(cmd_ros, shell=True, stdout=PIPE, stderr=PIPE)
        
        while True:
            retcode = proc.poll()
            if retcode is not None:
                result = proc.stdout.read() + proc.stderr.read()
                break
            else:
                time.sleep(.1)
                continue

        return result

    finished_cases = [os.path.splitext(os.path.basename(item))[0] for item in os.listdir(log_dir) 
                        if os.path.isfile(os.path.join(log_dir, item))]

    for fname in os.listdir(input_dir):
        if fname.endswith('.rkt') and not ("correct" in fname):
            if os.path.splitext(fname)[0] in finished_cases:
                print("[Ignore]{}".format(fname))
            else:
                print("[Input] Solving {}".format(fname))
                result = run_equiv_check(os.path.join(input_dir, fname))

def run_prop_check_benchmarks(input_dir, cosette_dir, log_dir, 
                               time_limit, symbreak, qex_enc):

    def run_prop_check(rosette_file):

        flags = ""
        flags += " --symbreak" if symbreak else ""
        flags += " --qex-enc" if qex_enc else ""

        case_name = os.path.splitext(os.path.basename(rosette_file))[0]
        cmd_ros = 'cd {}; sh qex_solve.sh {} {} {}'.format(cosette_dir, rosette_file, time_limit, flags)

        if log_dir:
            log_file = os.path.join(log_dir, case_name + ".log")
            cmd_ros += " > {}".format(log_file)

        proc = Popen(cmd_ros, shell=True, stdout=PIPE, stderr=PIPE)
        
        while True:
            retcode = proc.poll()
            if retcode is not None:
                result = proc.stdout.read() + proc.stderr.read()
                break
            else:
                time.sleep(.1)
                continue
                
        return result

    if log_dir is not None:
        finished_cases = [os.path.splitext(os.path.basename(item))[0] for item in os.listdir(log_dir) 
                        if os.path.isfile(os.path.join(log_dir, item))]
    else:
        finished_cases = []

    for fname in os.listdir(input_dir):
        if fname.endswith('.rkt') and not ("correct" in fname):
            if os.path.splitext(fname)[0] in finished_cases:
                print("[Ignore]{}".format(fname))
            else:
                print("[Input] Solving {}".format(fname))
                result = run_prop_check(os.path.join(input_dir, fname))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Evaluate symbolic refinement algorithm.')

    parser.add_argument('--dataset', dest='dataset', action='store', help='Name of the benchmark.', required=True)
    
    parser.add_argument('--benchmark-root', dest='benchmark_root', action='store', 
                        help='The root directory containing benchmarks.', default="benchmarks")
    
    parser.add_argument('--output-root', dest='output_dir', action='store', 
                        help='The output directory location.', default="output")

    args = parser.parse_args()

    dataset = args.dataset
    dataset_dir = os.path.join(args.benchmark_root, dataset)
    output_dir = args.output_dir

    for subdir in [f"{dataset}-symbreak",f"{dataset}-nosymbreak",
                   f"{dataset}-symbreak-qex",f"{dataset}-nosymbreak-qex"]:
        d = os.path.join(output_dir, subdir)
        if not os.path.exists(d):
            os.makedirs(d)

    apply_func = run_equiv_check_benchmarks if dataset in ["calcite", "cex"] else run_prop_check_benchmarks

    # reduce time limit to make evaluation faster 
    tl = 300 if dataset == "calcite" else (60 if dataset == "cex" else 120)
    
    apply_func(dataset_dir, ".", os.path.join(output_dir, f"{dataset}-symbreak"), time_limit=tl, symbreak=True, qex_enc=False)
    apply_func(dataset_dir, ".", os.path.join(output_dir, f"{dataset}-nosymbreak"), time_limit=tl, symbreak=False, qex_enc=False)
    apply_func(dataset_dir, ".", os.path.join(output_dir, f"{dataset}-symbreak-qex"), time_limit=tl, symbreak=True, qex_enc=True)
    apply_func(dataset_dir, ".", os.path.join(output_dir, f"{dataset}-nosymbreak-qex"), time_limit=tl, symbreak=False, qex_enc=True)

    #run_equiv_check_benchmarks("benchmarks/calcite", ".", "./output/calcite-symbreak", time_limit=300, symbreak=True, simplify=True, qex_enc=False)
    #run_equiv_check_benchmarks("benchmarks/calcite", ".", "./output/calcite-nosymbreak-qex", time_limit=300, symbreak=False, simplify=True, qex_enc=True)
    #run_equiv_check_benchmarks("benchmarks/calcite", ".", "./output/calcite-symbreak", time_limit=300, symbreak=True, simplify=True, qex_enc=False)
    #run_equiv_check_benchmarks("benchmarks/calcite", ".", "./output/calcite-nosymbreak-qex", time_limit=300, symbreak=False, simplify=True, qex_enc=True)
    
    #run_equiv_check_benchmarks("benchmarks/cex", ".", "./output/cex-symbreak", time_limit=60, symbreak=True, simplify=True, qex_enc=False)
    #run_equiv_check_benchmarks("benchmarks/cex", ".", "./output/cex-nosymbreak", time_limit=60, symbreak=False, simplify=True, qex_enc=False)
    #run_equiv_check_benchmarks("benchmarks/cex", ".", "./output/cex-symbreak-qex", time_limit=60, symbreak=True, simplify=True, qex_enc=True)
    #run_equiv_check_benchmarks("benchmarks/cex", ".", "./output/cex-nosymbreak-qex", time_limit=60, symbreak=False, simplify=True, qex_enc=True)

    #run_prop_check_benchmarks("benchmarks/qex", ".", "./output/qex-symbreak", 120, True, False)
    #run_prop_check_benchmarks("benchmarks/qex", ".", "./output/qex-nosymbreak", 120, False, False)
    #run_prop_check_benchmarks("benchmarks/qex", ".", "./output/qex-symbreak-qex", 120, True, True)
    #run_prop_check_benchmarks("benchmarks/qex", ".", "./output/qex-nosymbreak-qex", 120, False, True)
