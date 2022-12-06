use std::fs::read_to_string;
use regex::Regex;

fn main() {
    let s = read_to_string("../../../data/2022/05.input.txt").unwrap();
    for p in 1..=2 {
        let mut it = s.split("\n\n");
        let ss = it.next().unwrap();
        let sk = it.next().unwrap();
        let m = ss.lines().count() - 1;
        let n = (ss.lines().next().unwrap().len() + 1) / 4;
        let mut stacks: Vec<Vec<u8>> = Vec::new();
        for i in 0..n {
            let mut stack = Vec::new();
            let mut j = (m - 1) as i32;
            while j >= 0 {
                let c = ss.lines().skip(j as usize).next().unwrap().as_bytes()[(1 + i * 4) as usize];
                if c == b' ' {
                    break;
                }
                stack.push(c);
                j -= 1;
            }
            stacks.push(stack);
        }
        let re = Regex::new(r"^move (\d+) from (\d+) to (\d+)").unwrap();
        for line in sk.lines() {
            if line.is_empty() {
                break;
            }
            let cap = re.captures(line).unwrap();
            let a: usize = cap.get(1).unwrap().as_str().parse().unwrap();
            let b: usize = cap.get(2).unwrap().as_str().parse().unwrap();
            let c: usize = cap.get(3).unwrap().as_str().parse().unwrap();
            let lb = stacks[b - 1].len() - a;
            let mut bb = stacks[b - 1].split_off(lb);
            if p == 1 {
                bb.reverse();
            }
            stacks[c - 1].append(&mut bb);
            stacks[b - 1].truncate(lb);
        }
        println!("{}", String::from_utf8(stacks.iter().map(|stack| stack[stack.len() - 1]).collect::<Vec<_>>()).unwrap());
    }
}
