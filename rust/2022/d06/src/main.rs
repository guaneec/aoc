use std::{fs::read_to_string, collections::HashSet};

fn main() {
    let s = read_to_string("../../../data/2022/06.input.txt").unwrap();
    for l in [4, 14] {
        let x = (0..).filter(|i| s.as_bytes().iter().skip(*i as usize).take(l).collect::<HashSet<_>>().len() == l).next().unwrap() + l;
        println!("{}", x);
    }
}