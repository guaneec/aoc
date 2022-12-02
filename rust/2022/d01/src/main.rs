use std::fs::File;
use std::io::prelude::*;
use std::io::BufReader;
use std::vec::Vec;

fn main() {
    let f = File::open("../../../data/2022/01.input.txt").unwrap();
    let f = BufReader::new(f);
    let mut v = Vec::<u32>::new();

    let mut s: u32 = 0;
    for line in f.lines() {
        match line.unwrap().as_str() {
            "" => {
                v.push(s);
                s = 0;
            },            
            x => s += x.parse::<u32>().unwrap(),
        }
    }

    println!("{}", v.iter().max().unwrap());
    v.sort_unstable_by(|a, b| b.cmp(a));
    println!("{}", v.iter().take(3).sum::<u32>());
}
