use std::collections::{HashMap, HashSet};

fn p1(g: &mut HashMap<i32, HashSet<i32>>, floor: i32, x: i32, y: i32) -> (i32, bool) {
    if y == floor {
        return (0, true);
    }
    if (*g.entry(x).or_insert(HashSet::new())).contains(&y) {
        return (0, false);
    }
    g.entry(x).and_modify(|e| {e.insert(y);});
    let mut s = 0;
    for (ss, l) in [x, x-1, x+1].iter().map(|&xx| p1(g, floor, xx, y+1)) {
        s += ss;
        if l {
            return (s, true);
        }
    }
    (s + 1, false)
}

fn p2(g: &mut HashMap<i32, HashSet<i32>>, floor: i32, x: i32, y: i32) -> i32 {
    if y == floor || (*g.entry(x).or_insert(HashSet::new())).contains(&y) { return 0; }
    g.entry(x).and_modify(|e| {e.insert(y);});
    1 + [x, x-1, x+1].iter().map(|&xx| p2(g, floor, xx, y+1)).sum::<i32>()
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/14.input.txt").unwrap();
    let mut grid = HashMap::new();
    let mut floor = 0;
    for l in s.trim_end().lines() {
        let mut px = -1;
        let mut py = -1;
        for p in l.trim_end().split(" -> ") {
            let mut it = p.split(",");
            let x = it.next().unwrap().parse().unwrap();
            let y = it.next().unwrap().parse().unwrap();
            if px != -1 {
                let dx = ((x - px) as i32).signum();
                let dy = ((y - py) as i32).signum();
                let (mut xx, mut yy) = (px, py);
                loop {
                    (*grid.entry(xx).or_insert(HashSet::new())).insert(yy);
                    if (xx, yy) == (x, y) { break; }
                    (xx, yy) = (xx + dx, yy + dy);
                }
            }
            (px, py) = (x, y);
            floor = floor.max(y + 2);
        }
    }
    println!("{}", p1(&mut grid.clone(), floor, 500, 0).0);
    println!("{}", p2(&mut grid, floor, 500, 0));
}
