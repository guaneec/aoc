use std::collections::{HashSet, HashMap};

const DIRS: [(i32, i32); 7] = [(-1,0), (1,0), (0,-1), (0,1), (-1,0), (1,0), (0,-1)];
const D8: [(i32, i32); 8] = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)];
type Elf = (i32, i32);
fn dest(elves: &HashSet<Elf>, elf: Elf, t: usize) -> Elf {
    if D8.iter().all(|&(di, dj)| !elves.contains(&(di+elf.0, dj+elf.1))) { return elf; }
    for &(di, dj) in DIRS[t%4..t%4+4].iter() {
        if D8.iter().filter(|&(ddi, ddj)| di*ddi+dj*ddj == 1).all(|&(ddi, ddj)| !elves.contains(&(ddi+elf.0, ddj+elf.1))) {
            return (di+elf.0, dj+elf.1);
        }
    }
    elf
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/23.input.txt").unwrap();
    let elves: HashSet<_> = s.lines().enumerate().flat_map(|(i, l)| 
        l.chars().enumerate().filter(|&(_j, c)| c == '#').map(move |(j, _c)| (i as i32, j as i32))).collect();
    {
        let mut elves = elves.clone();
        for i in 0..10 {
            let mut c: HashMap<Elf, u8> = HashMap::new();
            for &e in elves.iter() {
                *c.entry(dest(&elves, e, i)).or_default() += 1;
            }
            elves = elves.iter().map(|&e| if c[&dest(&elves, e, i)] == 1 {dest(&elves, e, i)} else {e}).collect();
        }
        let imn = elves.iter().map(|e| e.0).min().unwrap();
        let imx = elves.iter().map(|e| e.0).max().unwrap();
        let jmn = elves.iter().map(|e| e.1).min().unwrap();
        let jmx = elves.iter().map(|e| e.1).max().unwrap();
        println!("{}", (imx-imn+1)*(jmx-jmn+1)-elves.len() as i32);
    }
    
    {
        let mut elves = elves.clone();
        for i in 0.. {
            let mut c: HashMap<Elf, u8> = HashMap::new();
            for &e in elves.iter() {
                *c.entry(dest(&elves, e, i)).or_default() += 1;
            }
            let prev = elves.clone();
            elves.clear();
            for &e in &prev {
                let ee = dest(&prev, e, i);
                if !elves.insert(ee) {
                    elves.remove(&ee);
                    elves.insert(e);
                    elves.insert((ee.0*2-e.0, ee.1*2-e.1));
                }
            }
            if prev == elves {
                println!("{}", i+1);
                break;
            }
        }
    }
}
