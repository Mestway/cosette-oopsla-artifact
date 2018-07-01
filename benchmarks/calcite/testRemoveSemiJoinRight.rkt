#lang rosette 
 
(require "../cosette.rkt" "../sql.rkt" "../evaluator.rkt" "../syntax.rkt") 
 
(provide ros-instance)
 
(current-bitwidth #f)
 
(define-symbolic div_ (~> integer? integer? integer?))
 
(define dept-info (table-info "dept" (list "deptno" "name")))
 
(define emp-info (table-info "emp" (list "empno" "ename" "job" "mgr" "hiredate" "comm" "sal" "deptno" "slacker")))
 

(define (q1 tables) 
  (SELECT (VALS "emp.ename") 
  FROM (JOIN (AS (NAMED (list-ref tables 1)) ["emp"]) (JOIN (AS (NAMED (list-ref tables 0)) ["dept"]) (AS (NAMED (list-ref tables 1)) ["emp0"]))) 
  WHERE (AND (BINOP "emp.deptno" = "dept.deptno") (BINOP "dept.deptno" = "emp0.deptno"))))

(define (q2 tables) 
  (SELECT (VALS "emp1.ename") 
  FROM (JOIN (AS (NAMED (list-ref tables 1)) ["emp1"]) (JOIN (AS (NAMED (list-ref tables 0)) ["dept0"]) (AS (NAMED (list-ref tables 1)) ["emp2"]))) 
  WHERE (AND (BINOP "emp1.deptno" = "dept0.deptno") (BINOP "dept0.deptno" = "emp2.deptno"))))


(define ros-instance (list q1 q2 (list dept-info emp-info))) 
