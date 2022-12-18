use std::collections::HashSet;

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/18.input.txt").unwrap();
    let droplets: HashSet<_> = s.split_terminator('\n').map(|l| {
        let mut it = l.split(',');
        let x: i32 = it.next().unwrap().parse().unwrap();
        let y: i32 = it.next().unwrap().parse().unwrap();
        let z: i32 = it.next().unwrap().parse().unwrap();
        (x, y, z)
    }).collect();
    let x1 = droplets.iter().map(|p| p.0).min().unwrap() - 1;
    let x2 = droplets.iter().map(|p| p.0).max().unwrap() + 1;
    let y1 = droplets.iter().map(|p| p.1).min().unwrap() - 1;
    let y2 = droplets.iter().map(|p| p.1).max().unwrap() + 1;
    let z1 = droplets.iter().map(|p| p.2).min().unwrap() - 1;
    let z2 = droplets.iter().map(|p| p.2).max().unwrap() + 1;
    let p1: i32 = droplets.iter().flat_map(|&(x, y, z)| [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)].into_iter()).map(|p| (!droplets.contains(&p)) as i32).sum();
    println!("{}", p1);
    let mut q = vec![(x1, y1, z1)];
    let mut p2 = 0;
    let mut visisted = HashSet::new();
    while !q.is_empty() {
        let (x, y, z) = q.pop().unwrap();
        if visisted.contains(&(x, y, z)) { continue; }
        visisted.insert((x, y, z));
        for p in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)] {
            if droplets.contains(&p) {p2 += 1;}
            else if x1 <= x && x <= x2 && y1 <= y && y <= y2 && z1 <= z && z <= z2 {q.push(p);}
        }
    }
    println!("{}", p2);
}
