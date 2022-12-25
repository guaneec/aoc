use std::{collections::{HashMap, HashSet, VecDeque, BinaryHeap}, cmp::Reverse};

use regex::Regex;

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/16.input.txt").unwrap();
    let re = Regex::new(r"Valve (.+) has flow rate=(.+); tunnels? leads? to valves? (.+)").unwrap();
    let mut valves = HashMap::new();
    let mut paths = HashMap::new();
    let mut i2a = vec![];
    let mut i2x = vec![];
    for l in s.split_terminator("\n") {
        let cap = re.captures(l).unwrap();
        let a = cap.get(1).unwrap().as_str();
        let x: i32 = cap.get(2).unwrap().as_str().parse().unwrap();
        let b: Vec<&str> = cap.get(3).unwrap().as_str().split(", ").collect();
        valves.insert(a, x);
        paths.insert(a, b);
        if a == "AA" || x > 0 {
            i2a.push(a);
            i2x.push(x);
        }
    }
    let iaa = i2a.iter().position(|&u| u == "AA").unwrap();
    let mut dd = HashMap::new();
    let mut dd2: Vec<Vec<(i32, usize)>> = std::iter::repeat(vec![]).take(i2a.len()).collect();
    for &x in valves.keys() {
        if x != "AA" && valves[x] == 0 {
            continue;
        }
        let mut v = vec![];
        let mut seen = HashSet::new();
        seen.insert(x);
        let mut q = VecDeque::new();
        q.push_back(x);
        let mut n = 1;
        let mut nn = 0;
        let mut d = 0;
        while !q.is_empty() {
            let i = q.pop_front().unwrap();
            if valves[i] > 0 && d > 0 {
                v.push((d, i));
                dd2[i2a.iter().position(|&u| u == x).unwrap()].push((d, i2a.iter().position(|&u| u == i).unwrap()))
            }
            for &nb in paths[i].iter() {
                if seen.contains(nb) { continue; }
                seen.insert(nb);
                q.push_back(nb);
                nn += 1;
            }
            n -= 1;
            if n == 0 {
                n = nn;
                nn = 0;
                d += 1;
            }
        }
        dd.insert(x, v);
    }
    let mut logs: HashMap<i32, i32> = HashMap::new();
    let s1: i32 = valves.values().sum();
    {
        let mut q = BinaryHeap::new();
        let end = 30;
        q.push(Reverse((0, (iaa, 1, 0))));
        let mut dists = HashMap::new();
        let mut p1 = -1;
        while !q.is_empty() {
            let Reverse((d, state)) = q.pop().unwrap();
            if dists.contains_key(&state) {
                continue;
            }
            dists.insert(state.clone(), d);
            let (x, t, open) = state;
            if t > end {
                p1 = s1 * end - d;
                break;
            }
            let ss1: i32 = (0..i2x.len()).filter(|&i| open >> i & 1 == 0).map(|i| i2x[i]).sum();
            if t <= 27 {
                let cand: i32 = s1 * 26 - d - (27 - t) * ss1;
                match logs.entry(open) {
                    std::collections::hash_map::Entry::Occupied(mut o) => {o.insert(cand.max(*o.get()));},
                    std::collections::hash_map::Entry::Vacant(v) => {v.insert(cand);},
                }
            }
            for (dn, y) in dd2[x].iter().copied() {
                if t + dn + 1 > end || open >> y == 1 { continue; }
                q.push(Reverse((d + ss1 * (dn + 1), (y, t + dn + 1, open | 1 << y))));
            }
            q.push(Reverse((d + ss1 * (end - t + 1), (x, end+1, open))));
        }
        println!("{}", p1);
    }
    let p2 = logs.iter().flat_map(|(&k, &v)| logs.iter().map(move |(&k2, &v2)| (k, k2, v+v2)))
        .filter(|&(k1, k2, _v)| k1 & k2 == 0).map(|(_k1, _k2, v)| v).max().unwrap();
    println!("{}", p2);
}
