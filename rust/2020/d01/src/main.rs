use std::collections::hash_set::HashSet;
use std::fs::File;
use std::io::prelude::*;
use std::io::{self, BufReader};
use std::vec::Vec;

fn sum2(slice: &[u32], target: u32) -> Option<u32> {
    let mut s = HashSet::<u32>::new();
    for x in slice {
        if s.contains(&x) {
            return Some(x * (target - x));
        }
        s.insert(target - x);
    }
    None
}

fn main() -> io::Result<()> {
    let f = File::open("../../../data/2020/01.input.txt")?;
    let f = BufReader::new(f);
    let mut v = Vec::<u32>::new();

    for line in f.lines() {
        let x = line.unwrap().trim().parse::<u32>().unwrap();
        v.push(x);
    }

    // p1
    println!("{}", sum2(&v, 2020).unwrap());
    // p2
    for i in 0..v.len() - 3 {
        match sum2(&v[i + 1..], 2020 - v[i]) {
            None => continue,
            Some(x) => {
                println!("{}", x * v[i]);
                break;
            }
        }
    }

    Ok(())
}
