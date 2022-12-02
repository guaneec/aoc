use std::fs::File;
use std::io::BufReader;
use std::io::prelude::*;

fn main() {
    let f = File::open("../../../data/2022/02.input.txt").unwrap();
    let f = BufReader::new(f);
    let mut p1: u32 = 0;
    let mut p2: u32 = 0;
    for line in f.lines() {
        let line = line.unwrap();
        let a = (line.as_bytes()[0] - b'A') as i32;
        let b = (line.as_bytes()[2] - b'X') as i32;
        p1 += [1, 2, 3][b as usize] + [3, 6, 0][((b - a + 3) % 3) as usize];
        p2 += [1, 2, 3][((a + b + 2) % 3) as usize] + [0, 3, 6][b as usize];
    }
    println!("{}", p1);
    println!("{}", p2);
}
