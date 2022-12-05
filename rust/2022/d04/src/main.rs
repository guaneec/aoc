use std::fs::read_to_string;
use regex::Regex;

fn main() {
    let s = read_to_string("../../../data/2022/04.input.txt").unwrap();
    let re = Regex::new(r"^(\d+)-(\d+),(\d+)-(\d+)").unwrap();
    let (p1, p2): (u32, u32) = s.lines().map(|line| {
        let cap = re.captures(line).unwrap();
        let a: u32 = cap.get(1).unwrap().as_str().parse().unwrap();
        let b: u32 = cap.get(2).unwrap().as_str().parse().unwrap();
        let c: u32 = cap.get(3).unwrap().as_str().parse().unwrap();
        let d: u32 = cap.get(4).unwrap().as_str().parse().unwrap();
        (if a <= c && d <= b || c <= a && b <= d {1} else {0}, if d < a || b < c {0} else {1})
    }).fold((0, 0), |a, b| (a.0 + b.0, a.1 + b.1));
    println!("{}", p1);
    println!("{}", p2);
}
