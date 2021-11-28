use std::fs::File;
use std::io::prelude::*;
use std::io::{self, BufReader};
use std::str::FromStr;

use nom::bytes::complete::tag;
use nom::character::complete::{alpha1, anychar, digit1};
use nom::combinator::map_res;
use nom::IResult;

struct Entry {
    lo: u8,
    hi: u8,
    c: char,
    s: String,
}

fn parse_entry(input: &str) -> IResult<&str, Entry> {
    let (input, lo) = map_res(digit1, |s: &str| s.parse::<u8>())(input)?;
    let (input, _) = tag("-")(input)?;
    let (input, hi) = map_res(digit1, |s: &str| s.parse::<u8>())(input)?;
    let (input, _) = tag(" ")(input)?;
    let (input, c) = anychar(input)?;
    let (input, _) = tag(": ")(input)?;
    let (input, s) = alpha1(input)?;
    Ok((
        input,
        Entry {
            lo,
            hi,
            c,
            s: String::from_str(s).unwrap(),
        },
    ))
}
fn main() -> io::Result<()> {
    let f = File::open("../../../data/2020/02.input.txt")?;
    let f = BufReader::new(f);
    let p1 = |e: &Entry| {
        let count = e.s.chars().filter(|c| *c == e.c).count() as u8;
        e.lo <= count && count <= e.hi
    };
    let p2 = |e: &Entry| {
        (e.s.as_bytes()[e.lo as usize - 1] as char == e.c)
            != (e.s.as_bytes()[e.hi as usize - 1] as char == e.c)
    };
    let (c1, c2) = f
        .lines()
        .map(|l| l.unwrap())
        .map(|l| parse_entry(&l).unwrap().1)
        .map(|e| (p1(&e), p2(&e)))
        .fold((0, 0), |(c1, c2), (b1, b2)| {
            (c1 + b1 as u16, c2 + b2 as u16)
        });
    println!("{}", c1);
    println!("{}", c2);
    Ok(())
}
