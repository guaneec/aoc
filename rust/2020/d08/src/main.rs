use std::{fs::read_to_string, collections::HashSet};

fn run(ins: &Vec<(&str, i32)>, corrupted: i32) -> (i32, i32) {
    let mut ip = 0;
    let mut acc = 0;
    let mut visited = HashSet::<i32>::new();
    while !visited.contains(&ip) && ip < ins.len() as i32{
        visited.insert(ip);
        let (op, x) = ins[ip as usize];
        if op == "jmp" && ip != corrupted || op == "nop" && ip == corrupted {
            ip += x - 1;
        } else if op == "acc" {
            acc += x;
        }
        ip += 1;
    }
    (ip, acc)
}

fn main() {
    let s = read_to_string("../../../data/2020/08.input.txt").unwrap();
    let ins: Vec<(&str, i32)> = s.lines().filter(|&line| !line.is_empty()).map(|line| {
        let mut it = line.split_ascii_whitespace();
        let op = it.next().unwrap();
        let x: i32 = it.next().unwrap().parse().unwrap();
        (op, x)
    }).collect();
    let p1 = run(&ins, -1).1;
    let p2: i32 = (0..ins.len()).filter(|&i| ins[i].0 != "acc").map(|i| run(&ins, i as i32)).filter(|&(ip, _acc)| ip == ins.len() as i32).next().unwrap().1;
    
    println!("{}", p1);
    println!("{}", p2);
}
