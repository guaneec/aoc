use std::fs::read_to_string;

fn pack(s: &str) -> u32 {
    let mut o = 0;
    for &c in s.as_bytes() {
        o |= 1 << c - b'a';
    }
    o
}

fn main() {
    let s = read_to_string("../../../data/2020/06.input.txt").unwrap();
    let p1: u32 = s.split("\n\n").filter(|&g| g != "").map(|g| g.split('\n').filter(|&l| l != "").map(|l| pack(l)).reduce(|a, b| a | b).unwrap().count_ones()).sum();
    let p2: u32 = s.split("\n\n").filter(|&g| g != "").map(|g| g.split('\n').filter(|&l| l != "").map(|l| pack(l)).reduce(|a, b| a & b).unwrap().count_ones()).sum();
    println!("{}", p1);
    println!("{}", p2);
}
