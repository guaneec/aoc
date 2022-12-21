use std::collections::HashMap;
use std::ops::{Add, Sub, Mul, Div};

enum Monkey<'a> {
    Num(i128),
    Wait { left: &'a str, op: char, right: &'a str },
}

fn yell(name: &str, monkeys: &HashMap<&str, Monkey>) -> i128 {
    match monkeys[name] {
        Monkey::Num(x) => x,
        Monkey::Wait { left, op: '+', right } => yell(left, monkeys) + yell(right, monkeys),
        Monkey::Wait { left, op: '-', right } => yell(left, monkeys) - yell(right, monkeys),
        Monkey::Wait { left, op: '*', right } => yell(left, monkeys) * yell(right, monkeys),
        Monkey::Wait { left, op: '/', right } => yell(left, monkeys) / yell(right, monkeys),
        _ => panic!(),
    }
}

struct Poly1 {
    a0: Fraction,
    a1: Fraction,
}

impl Add for Poly1 {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Poly1 {a0: self.a0 + rhs.a0, a1: self.a1 + rhs.a1 }
    }
}

impl Sub for Poly1 {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        Poly1 {a0: self.a0 - rhs.a0, a1: self.a1 - rhs.a1 }
    }
}

impl Mul for Poly1 {
    type Output = Self;

    fn mul(self, rhs: Self) -> Self::Output {
        assert!(self.a1.num == 0 || rhs.a1.num == 0);
        Poly1 {a0: self.a0 * rhs.a0, a1: self.a0 * rhs.a1 + self.a1 * rhs.a0 }
    }
}

impl Div for Poly1 {
    type Output = Self;

    fn div(self, rhs: Self) -> Self::Output {
        assert!(rhs.a1.num == 0);
        Poly1 {a0: self.a0 / rhs.a0, a1: self.a1 / rhs.a0 }
    }
}

#[derive(Clone, Copy)]
struct Fraction {
    num: i128,
    den: i128,
}

fn gcd(a: i128, b: i128) -> i128 {
    let (a, b) = (a.max(b), a.min(b));
    _gcd(a, b)
}

fn _gcd(a: i128, b: i128) -> i128 {
    if b == 0 {a} else {_gcd(b, a % b)}
}

fn simple_frac(num: i128, den: i128) -> Fraction {
    let d = gcd(num.abs(), den.abs());
    let sign = if den < 0 {-1} else {1};
    Fraction { num: num / d * sign, den: den / d * sign }
}

impl Add for Fraction {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        simple_frac(self.num * rhs.den + self.den * rhs.num, self.den * rhs.den)
    }
}

impl Sub for Fraction {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        simple_frac(self.num * rhs.den - self.den * rhs.num, self.den * rhs.den)
    }
}

impl Mul for Fraction {
    type Output = Self;

    fn mul(self, rhs: Self) -> Self::Output {
        simple_frac(self.num * rhs.num, self.den * rhs.den)
    }
}

impl Div for Fraction {
    type Output = Self;

    fn div(self, rhs: Self) -> Self::Output {
        simple_frac(self.num * rhs.den, self.den * rhs.num)
    }
}


fn yell2(name: &str, monkeys: &HashMap<&str, Monkey>) -> Poly1 {
    if name == "humn" { return Poly1 { a0: Fraction { num: 0, den: 1}, a1: Fraction { num: 1, den: 1} }}
    match monkeys[name] {
        Monkey::Num(x) => Poly1 { a0: Fraction { num: x, den: 1}, a1: Fraction { num: 0, den: 1} },
        Monkey::Wait { left, op: '+', right } => yell2(left, monkeys) + yell2(right, monkeys),
        Monkey::Wait { left, op: '-', right } => yell2(left, monkeys) - yell2(right, monkeys),
        Monkey::Wait { left, op: '*', right } => yell2(left, monkeys) * yell2(right, monkeys),
        Monkey::Wait { left, op: '/', right } => yell2(left, monkeys) / yell2(right, monkeys),
        _ => panic!(),
    }
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/21.input.txt").unwrap();
    let mut monkeys: HashMap<&str, Monkey> = s.split_terminator('\n').map(|l| {
        let mut it = l.split(": ");
        let name = it.next().unwrap();
        let inst = it.next().unwrap();
        (name, if inst.bytes().next().unwrap().is_ascii_digit() {
            Monkey::Num(inst.parse().unwrap())
        } else {
            let mut it = inst.split_ascii_whitespace();
            let left = it.next().unwrap();
            let op = it.next().unwrap().chars().next().unwrap();
            let right = it.next().unwrap();
            Monkey::Wait { left, op, right }
        })
    }).collect();
    println!("{}", yell("root", &monkeys));
    monkeys.entry("root").and_modify(|m| {
        match m { 
            Monkey::Wait { op, .. } => {*op = '-'; }
            _ => {panic!();}
        };
    });
    let Poly1 {a0, a1} = yell2("root", &monkeys);
    println!("{}", -(a0 / a1).num);
}
