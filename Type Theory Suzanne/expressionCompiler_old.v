(* 
Opgave 3: Proving an expression compiler correct
Suzanne van den Bosch
Studentnummer: s4021444
*)

Require Import Datatypes.
Require Import List.

(*3.1*)

Inductive Exp : Set :=
| Lit : nat -> Exp
| Plus : Exp -> Exp -> Exp 
| Mul : Exp -> Exp -> Exp.

(*3.2*)

Fixpoint eval (e:Exp) : nat := 
 match e with 
| Lit x => x
| Plus x y => eval x + eval y
| Mul x y => eval x * eval y
end.

(*3.3*)

Inductive RPN1 : Set :=
| RPNlit : nat -> RPN1
| RPNplus : RPN1
| RPNmul : RPN1.

Definition RPN := list RPN1. 

(*3.4*)

Fixpoint rpn (e:Exp) : RPN := 
 match e with 
| Lit x => RPNlit x :: nil
| Plus x y => rpn x  ++ rpn y ++ RPNplus :: nil
| Mul x y => rpn x  ++ rpn y ++ RPNmul :: nil
end.

(*3.5*)

Fixpoint rpn_eval1 (l : list nat) (r:RPN) : option nat := 
 match r with
| nil => 
    match l with 
     | nil => None
     | x :: _ => Some x
     end
| h::t => 
    match h with 
     | RPNlit x => rpn_eval1 (x::l) t
     | RPNplus => 
         match l with 
          | nil => None
          | x :: l2 => 
             match l2 with
              | nil => None
              | y :: l3 => rpn_eval1 ((x + y) :: l3) t
             end
         end
     | RPNmul => 
         match l with 
          | nil => None
          | x :: l2 => 
             match l2 with
              | nil => None
              | y :: l3 => Some (x * y)
             end
        end
    end
end.

Definition rpn_eval (r:RPN) := rpn_eval1 nil r.

(*3.6*)

Theorem question_3_6 : forall e:Exp, Some (eval e) = rpn_eval (rpn e).
Admitted.

(*3.7*)

Inductive Expv : Set :=
| Litv : nat -> Expv
| Var : nat -> Expv
| Plusv : Expv -> Expv -> Expv 
| Mulv : Expv -> Expv -> Expv.

Fixpoint lookup_var (n:nat) (l:list nat) : nat :=
match l with
| nil => 0
| h::t => 
    match n with
    | 0 => h
    | S n1 => lookup_var n1 t
    end
end.

Fixpoint store_var (n m :nat) (l:list nat) : (list nat) :=
match l with
| nil => 
    match n with 
    | 0 => m :: nil
    | S n1 => 0 :: store_var n1 m nil
    end
| h::t =>
    match n with 
    | 0 => m::t
    | S n1 => h :: store_var n1 m t
    end
end. 

Fixpoint evalv (e:Expv) (l: list nat): nat := 
 match e with 
| Litv x => x
| Var x => lookup_var x l
| Plusv x y => evalv x l + evalv y l
| Mulv x y => evalv x l * evalv y l
end.

Inductive RPNv1 : Set :=
| RPNvlit : nat -> RPNv1
| RPNvar : nat -> RPNv1
| RPNvplus : RPNv1
| RPNvmul : RPNv1.

Definition RPNv := list RPNv1. 

Fixpoint rpnv (e:Expv) : RPNv := 
 match e with 
| Litv x => RPNvlit x :: nil
| Var x => RPNvar x :: nil
| Plusv x y => rpnv x ++ rpnv y ++ RPNvplus :: nil
| Mulv x y => rpnv x ++ rpnv y ++ RPNvmul :: nil
end.

Fixpoint rpn_evalv1 (l : list nat) (r:RPNv) (k: list nat): option nat := 
 match r with
| nil => 
    match l with 
     | nil => None
     | x :: _ => Some x
     end
| h::r2 => 
    match h with 
     | RPNvlit x => rpn_evalv1 (x::l) r2 k
     | RPNvar x => Some (lookup_var x l)
     | RPNvplus => 
         match l with 
          | nil => None
          | x :: l2 => 
             match l2 with
              | nil => None
              | y :: l3 => Some (x + y)
             end
         end
     | RPNvmul => 
         match l with 
          | nil => None
          | x :: l2 => 
             match l2 with
              | nil => None
              | y :: l3 => Some (x * y)
             end
        end
    end
end.

Definition rpn_evalv (r:RPNv) (l: list nat) := rpn_evalv1 nil r l.

Theorem question_3_6var : forall e:Expv, forall l:(list nat), Some (evalv e l) = rpn_evalv (rpnv e) l.
Admitted.