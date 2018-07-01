#lang rosette 
 
(require "../cosette.rkt" "../sql.rkt" "../evaluator.rkt" "../syntax.rkt") 
 
(provide ros-instance)
 
(current-bitwidth #f)
 
(define-symbolic div_ (~> integer? integer? integer?))
 
(define t-info (table-info "t" (list "k0" "c1" "f1_a0" "f2_a0" "f0_c0" "f1_c0" "f0_c1" "f1_c2" "f2_c3")))
 
(define account-info (table-info "account" (list "acctno" "type" "balance")))
 
(define bonus-info (table-info "bonus" (list "ename" "job" "sal" "comm")))
 
(define dept-info (table-info "dept" (list "deptno" "name")))
 
(define emp-info (table-info "emp" (list "empno" "ename" "job" "mgr" "hiredate" "comm" "sal" "deptno" "slacker")))
 
(define-symbolic* str_foo_ integer?) 

(define (q1 tables) 
  (SELECT (VALS "emp.ename") 
  FROM (JOIN (AS (NAMED (list-ref tables 4)) ["emp"]) (AS (NAMED (list-ref tables 3)) ["dept"])) 
  WHERE (AND (BINOP "emp.deptno" = "dept.deptno") (BINOP "emp.ename" = str_foo_))))

(define (q2 tables) 
  (SELECT (VALS "t1.ename") 
  FROM (JOIN (AS (SELECT (VALS "emp0.empno" "emp0.ename" "emp0.job" "emp0.mgr" "emp0.hiredate" "emp0.comm" "emp0.sal" "emp0.deptno" "emp0.slacker") 
  FROM (AS (NAMED (list-ref tables 4)) ["emp0"]) 
  WHERE (BINOP "emp0.ename" = str_foo_)) ["t1" (list "empno" "ename" "job" "mgr" "hiredate" "comm" "sal" "deptno" "slacker")]) (AS (NAMED (list-ref tables 3)) ["dept0"])) 
  WHERE (BINOP "t1.deptno" = "dept0.deptno")))


(define ros-instance (list q1 q2 (list t-info account-info bonus-info dept-info emp-info))) 
