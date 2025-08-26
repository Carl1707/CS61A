(define (factorial x)
  (cond ((= x 0) 1)
        (else (* x (factorial (- x 1))))))
(expect (factorial 5) 120)
(expect (factorial 0) 1)

; Return whether there are n perfect squares with no repeats that sum to total

    (define (fit total n)
        (define (f total n k)
            (if (and (= n 0) (= total 0))
                #t
            (if (< total (* k k))
                #f
                (or (f (- total (* k k) ) (- n 1) (+ k 1)) (f total n (+ k 1)))
            )))
        (f total n 1))

    (expect (fit 10 2) #t)  ; 1*1 + 3*3
    (expect (fit 9 1)  #t)  ; 3*3
    (expect (fit 9 2)  #f)  ;
    (expect (fit 9 3)  #f)  ; 1*1 + 2*2 + 2*2 doesn't count because of repeated 2*2
    (expect (fit 25 1)  #t) ; 5*5
    (expect (fit 25 2)  #t) ; 3*3 + 4*4

