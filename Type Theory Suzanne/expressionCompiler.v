(* 
Opgave 3: Proving an expression compiler correct
Suzanne van den Bosch
Studentnummer: s4021444
*)

Require Import Arith.
Require Import Datatypes.
Require Import List.

(*3.1*)

Inductive Binop : Set :=
| Plus : Binop
| Mul : Binop.


Inductive Exp : Set :=
| Lit : nat -> Exp
| Oper : Binop -> Exp -> Exp -> Exp.

(*3.2*)

Fixpoint eval (e:Exp) : nat := 
match e with 
| Lit x => x
| Oper b x y => 
 match b with 
 | Plus => eval x + eval y
 | Mul => eval x * eval y
 end
end.

(*3.3*)

Inductive RPNexp : Set :=
| RPNlit : nat -> RPNexp
| RPNbinop : Binop -> RPNexp.

Definition RPN := list RPNexp. 

(*3.4*)

Fixpoint rpn (e:Exp) : RPN := 
match e with 
| Lit x => RPNlit x :: nil
| Oper b x y => rpn x ++ rpn y ++ RPNbinop b :: nil
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
     | RPNbinop b => 
         match l with 
          | nil => None
          | x :: l2 => 
             match l2 with
              | nil => None
              | y :: l3 => 
                match b with 
                | Plus => rpn_eval1 ((x + y) :: l3) t
                | Mul => rpn_eval1 ((x * y) :: l3) t
                end
             end
         end
    end
end.

Definition rpn_eval (r:RPN) := rpn_eval1 nil r.

(*3.6*)

Theorem helpTheorem : forall e:Exp, forall s: list nat, forall t:RPN, rpn_eval1 s ((rpn e) ++ t) = rpn_eval1 (eval e :: s) t.
induction e.
induction s.
induction t.
simpl.
reflexivity.
simpl.
reflexivity.
simpl.
reflexivity.
intros s t.
induction b.
simpl.
assert (extra1 := (rpn e1 ++ rpn e2 ++ RPNbinop Plus :: nil) ++ t = rpn e1 ++ (rpn e2 ++ ((RPNbinop Plus :: nil) ++ t))).
replace ((rpn e1 ++ rpn e2 ++ RPNbinop Plus :: nil) ++ t) with (rpn e1 ++ (rpn e2 ++ ((RPNbinop Plus :: nil) ++ t))).
assert (extra2: rpn_eval1 s (rpn e1 ++ rpn e2 ++ (RPNbinop Plus :: nil) ++ t) = rpn_eval1 (eval e1 :: s) (rpn e2 ++ (RPNbinop Plus :: nil) ++ t)).
apply IHe1 with (t := rpn e2 ++ (RPNbinop Plus :: nil) ++ t).
assert (extra3: rpn_eval1 (eval e1 :: s) (rpn e2 ++ (RPNbinop Plus :: nil) ++ t) = rpn_eval1 (eval e2 :: eval e1 :: s) ((RPNbinop Plus :: nil) ++ t)).
apply IHe2 with (t := (RPNbinop Plus :: nil) ++ t).
assert (extra4: rpn_eval1 (eval e2 :: eval e1 :: s) ((RPNbinop Plus :: nil) ++ t) = rpn_eval1 (eval e1 + eval e2 :: s) t).
simpl.
rewrite plus_comm.
reflexivity.
rewrite extra2.
rewrite extra3.
rewrite extra4.
reflexivity.
rewrite app_assoc.
rewrite app_assoc.
rewrite app_assoc.
reflexivity.
simpl.
assert (extra1 := (rpn e1 ++ rpn e2 ++ RPNbinop Mul :: nil) ++ t = rpn e1 ++ (rpn e2 ++ ((RPNbinop Mul :: nil) ++ t))).
replace ((rpn e1 ++ rpn e2 ++ RPNbinop Mul :: nil) ++ t) with (rpn e1 ++ (rpn e2 ++ ((RPNbinop Mul :: nil) ++ t))).
assert (extra2: rpn_eval1 s (rpn e1 ++ rpn e2 ++ (RPNbinop Mul :: nil) ++ t) = rpn_eval1 (eval e1 :: s) (rpn e2 ++ (RPNbinop Mul :: nil) ++ t)).
apply IHe1 with (t := rpn e2 ++ (RPNbinop Mul :: nil) ++ t).
assert (extra3: rpn_eval1 (eval e1 :: s) (rpn e2 ++ (RPNbinop Mul :: nil) ++ t) = rpn_eval1 (eval e2 :: eval e1 :: s) ((RPNbinop Mul :: nil) ++ t)).
apply IHe2 with (t := (RPNbinop Mul :: nil) ++ t).
assert (extra4: rpn_eval1 (eval e2 :: eval e1 :: s) ((RPNbinop Mul :: nil) ++ t) = rpn_eval1 (eval e1 * eval e2 :: s) t).
simpl.
rewrite mult_comm.
reflexivity.
rewrite extra2.
rewrite extra3.
rewrite extra4.
reflexivity.
rewrite app_assoc.
rewrite app_assoc.
rewrite app_assoc.
reflexivity.
Qed.


Theorem question_3_6 : forall e:Exp, Some (eval e) = rpn_eval (rpn e).
unfold rpn_eval.
induction e.
simpl.
reflexivity.
induction b.
simpl.
rewrite helpTheorem.
rewrite helpTheorem.
simpl.
rewrite plus_comm.
reflexivity.
simpl.
rewrite helpTheorem.
rewrite helpTheorem.
simpl.
rewrite mult_comm.
reflexivity.
Qed.


(*3.7*)

Inductive Expv : Set :=
| Litv : nat -> Expv
| Var : nat -> Expv
| Operv : Binop -> Expv -> Expv -> Expv.

Fixpoint lookup_var (n:nat) (varList:list nat) : nat :=
match varList with
| nil => 0
| h::t => 
    match n with
    | 0 => h
    | S n1 => lookup_var n1 t
    end
end.

Fixpoint evalv (e:Expv) (varList: list nat): nat := 
 match e with 
| Litv x => x
| Var x => lookup_var x varList
| Operv b x y =>
 match b with
 | Plus => evalv x varList + evalv y varList
 | Mul => evalv x varList * evalv y varList
 end
end.

Inductive RPNvExp : Set :=
| RPNvlit : nat -> RPNvExp
| RPNvar : nat -> RPNvExp
| RPNvbinop : Binop -> RPNvExp.

Definition RPNv := list RPNvExp. 

Fixpoint rpnv (e:Expv) : RPNv := 
 match e with 
| Litv x => RPNvlit x :: nil
| Var x => RPNvar x :: nil
| Operv b x y => rpnv x ++ rpnv y ++ RPNvbinop b :: nil
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
     | RPNvar x => Some (lookup_var x k)
     | RPNvbinop b =>
       match l with 
        | nil => None
        | x :: l2 => 
           match l2 with
            | nil => None
            | y :: l3 => 
              match b with 
              | Plus => rpn_evalv1 ((x + y) :: l3) r2 k
              | Mul => rpn_evalv1 ((x * y) :: l3) r2 k
              end
           end
       end
    end
end.

Definition rpn_evalv (r:RPNv) (l: list nat) := rpn_evalv1 nil r l.


Theorem helpTheoremvar : forall e:Expv, forall l varList: list nat, forall t:RPNv, rpn_evalv1 l ((rpnv e) ++ t) varList = rpn_evalv1 (evalv e varList :: l) t varList.
induction e.
simpl.
reflexivity.
simpl.
intros l varList.
induction t.
simpl.
reflexivity.
rewrite IHt.




Admitted.

Theorem question_3_6var : forall e:Expv, forall l:(list nat), Some (evalv e l) = rpn_evalv (rpnv e) l.
unfold rpn_evalv.
induction e.
simpl.
reflexivity.
simpl.
reflexivity.
intro l.
induction b.
simpl.
rewrite helpTheoremvar.
rewrite helpTheoremvar.
simpl.
rewrite plus_comm.
reflexivity.
simpl.
rewrite helpTheoremvar.
rewrite helpTheoremvar.
simpl.
rewrite mult_comm.
reflexivity.
Qed.
