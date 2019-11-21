# Lambda Calculator

An implementation of Alonzo Church's Lambda Calculus.

> The λ calculus can be called the smallest universal programming language of the
world. The λ calculus consists of a single transformation rule (variable substitution)
and a single function definition scheme. It was introduced in the 1930s by Alonzo
Church as a way of formalizing the concept of effective computability. The λ calculus
is universal in the sense that any computable function can be expressed and evaluated
using this formalism. It is thus equivalent to Turing machines. However, the λ calculus
emphasizes the use of transformation rules and does not care about the actual machine
implementing them. It is an approach more related to software than to hardware.

Source: https://www.inf.fu-berlin.de/lehre/WS03/alpi/lambda.pdf

### Parse, reduce and evaluate lambda calculus expressions in a convenient REPL.

```
>>> (\ab.a)(\x.x)
λbx.x
```


## Install

Simply clone this repo and setup a python virtual environment.

```bash
$ git clone https://github.com/blakelockley/lambda
$ cd lamdba
$ virtualenv .venv --python=python3
$ source .venv/bin/activate
```

## Running the REPL

Launch the lamdba calculator REPL.

```
$ python main.py
* Welcome to the lambda REPL!
* Hint: You can use '\' to represent to lambda character (λ).
>>> 
```

Enter any lambda expression to be evaluated and reduced using `\` or `λ` to denote the start of a function.

```
>>> \x.x
λx.x
```

Use parans to denote the begining and end of a function.
> Note, parans anywhere following a `\` will be treated as part of that function's expression within the scope of the current parans!

This example show the successor function applied to the lambda calculus notation of the number 1 (`λsz.sz`). This expression is reduced to the value of 2 (in lamdba calculus notation).

```
>>> (\wyx.y(wyx))(\sz.sz)
λyx.y(yx)
```
