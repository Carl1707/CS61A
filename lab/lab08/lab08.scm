(define (over-or-under num1 num2)
  (cond ((< num1 num2) -1)
        ((= num1 num2)  0)
        ((> num1 num2)  1)
    )
  )

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b)
  (if (zero? b) a
                (gcd b (modulo a b))
    )
  )

(define (remove item lst)
  (cond
    ((null? lst) nil)
    ((equal? (car lst) item) (remove item (cdr lst)))
    (else (cons (car lst) (remove item (cdr lst)))
      )
    )
  )

(define (duplicate lst)
  (cond
    ((null? lst) nil)
    (else (cons (car lst) (cons (car lst) (duplicate (cdr lst)))
            )
      )
    )
  )

(expect (duplicate '(1 2 3)) (1 1 2 2 3 3))

(expect (duplicate '(1 1)) (1 1 1 1))

(define (composed f g)
  (lambda (x) (f (g x)))
  )

(define (repeat f n)
  (if (= n 1) (lambda (x) (f x))
              (lambda (x) (f ((repeat f (- n 1)) x))
                )
    ;第二个也应该返回一个函数，而不是一个值
    )
  )
