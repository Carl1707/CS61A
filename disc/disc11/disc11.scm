(define-macro (assign sym1 sym2 expr1 expr2)
  `(begin
     ;; 第一个 define 会覆盖 sym1 的值
     (define ,sym1 ,expr1)
     ;; 所以在第二个 define 中，我们不能直接用 expr2，
     ;; 因为如果 expr2 依赖于 sym1 的旧值，那个值已经没了。
     ;; 因此，我们在宏展开时就计算出 expr2 的值，把它变成一个常量。
     (define ,sym2 ,(eval expr2))
   ))

(define-macro (switch expr cases)
    `(let ((val ,expr))
	  ,(cons
	    'cond
	    (map (lambda (case) (cons
	           `(equal? ,val ,(car case))
		       ,(cadr case)))
		     cases))))

