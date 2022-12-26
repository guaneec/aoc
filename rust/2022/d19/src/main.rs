use std::collections::BinaryHeap;

use regex::Regex;

struct Blueprint {
    oreore: i32,
    claore: i32,
    obsore: i32,
    obscla: i32,
    geoore: i32,
    geoobs: i32,
}

fn ceildiv(a: i32, b: i32) -> i32 {
    if b == 0 {87878787} else {(a+b-1)/b}
}

#[derive(PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
struct State {
    t: i32, ore: i32, cla: i32, obs: i32, dore: i32, dcla: i32, dobs: i32
}

#[derive(PartialEq, Eq, PartialOrd, Ord)]
struct AstarItem {
    bound: i32,
    cur: i32,
    item: State,
}

fn h(end: i32, b: &Blueprint, s: &State) -> i32 {
    let tt = end-2-s.t;
    let dt = 1;
    let mut m = 0;
    if tt > 0 && s.obs+s.dobs*(tt-1)<b.geoobs*tt && s.t+dt<= end {
        m = m.max(h(end, &b, &State {t: s.t+dt, ore:0, cla:0, obs:s.obs+dt*s.dobs, dore:0, dcla:0, dobs:s.dobs+1 } ));
    }
    let dt = ceildiv(0.max(b.geoobs - s.obs), s.dobs) + 1;
    if s.t+dt<=end {
        m = m.max(end+1-(s.t+dt) + h(end, &b, &State {t: s.t+dt, ore:0, cla:0, obs:s.obs+dt*s.dobs-b.geoobs, dore:0, dcla:0, dobs:s.dobs }));
    }
    m
}

fn f(end: i32, b: &Blueprint, s0: &State) -> i32 {
    let mut q = BinaryHeap::new();
    q.push(AstarItem{ bound:h(end, &b, &s0), cur:0, item: s0.clone() });
    loop {
        let z = q.pop().unwrap();
        let x = z.item;
        if x.t == end+1 { return z.cur; }
        let tt = end-2-x.t;
        let dt = ceildiv(0.max(b.oreore-x.ore), x.dore) + 1;
        if tt > 0 && x.ore+x.dore*(tt-1)< [b.oreore, b.claore, b.obsore, b.geoore].into_iter().max().unwrap()*tt && x.t+dt<=end {
            let y = State {t: x.t+dt, ore:x.ore+dt*x.dore-b.oreore, cla:x.cla+dt*x.dcla, obs:x.obs+dt*x.dobs, dore:x.dore+1, dcla:x.dcla, dobs:x.dobs };
            q.push(AstarItem { bound:  z.cur + h(end, &b, &y), cur: z.cur, item: y });
        }
        let tt = end-4-x.t;
        let dt = ceildiv(0.max(b.claore-x.ore), x.dore) + 1;
        if tt > 0 && x.cla+x.dcla*(tt-1)< b.obscla*tt && x.t+dt<=end {
            let y = State {t: x.t+dt, ore:x.ore+dt*x.dore-b.claore, cla:x.cla+dt*x.dcla, obs:x.obs+dt*x.dobs, dore:x.dore, dcla:x.dcla+1, dobs:x.dobs };
            q.push(AstarItem { bound:  z.cur + h(end, &b, &y), cur: z.cur, item: y });
        }
        let tt = end-2-x.t;
        let dt = ceildiv(0.max(b.obsore - x.ore), x.dore).max(ceildiv(0.max(b.obscla - x.cla), x.dcla)) + 1;
        if tt > 0 && x.obs+x.dobs*(tt-1)<b.geoobs*tt && x.t+dt<= end {
            let y = State {t: x.t+dt, ore:x.ore+dt*x.dore-b.obsore, cla:x.cla+dt*x.dcla-b.obscla, obs:x.obs+dt*x.dobs, dore:x.dore, dcla:x.dcla, dobs:x.dobs+1 };
            q.push(AstarItem { bound:  z.cur + h(end, &b, &y), cur: z.cur, item: y });
        }
        let dt = ceildiv(0.max(b.geoore - x.ore),x.dore).max(ceildiv(0.max(b.geoobs - x.obs), x.dobs)) + 1;
        if x.t+dt<=end {
            let y = State {t: x.t+dt, ore:x.ore+dt*x.dore-b.geoore, cla:x.cla+dt*x.dcla, obs:x.obs+dt*x.dobs-b.geoobs, dore:x.dore, dcla:x.dcla, dobs:x.dobs };
            q.push(AstarItem { bound:  z.cur+(end+1-(x.t+dt)) + h(end, &b, &y), cur: z.cur+(end+1-(x.t+dt)), item: y });
        }
        q.push(AstarItem { bound: z.cur, cur: z.cur, item: State { t:end+1, ore: 0, cla: 0, obs: 0, dore: 0, dcla: 0, dobs: 0 } })
    }
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/19.input.txt").unwrap();
    let re = Regex::new("[0-9]+").unwrap();
    let blueprints: Vec<_> = s.split_terminator('\n').map(|l| {
        let mut matches = re.find_iter(l).skip(1);
        Blueprint {
            oreore: matches.next().unwrap().as_str().parse().unwrap(),
            claore: matches.next().unwrap().as_str().parse().unwrap(),
            obsore: matches.next().unwrap().as_str().parse().unwrap(),
            obscla: matches.next().unwrap().as_str().parse().unwrap(),
            geoore: matches.next().unwrap().as_str().parse().unwrap(),
            geoobs: matches.next().unwrap().as_str().parse().unwrap(),
        }
    }).collect();
    println!("{}", blueprints.iter().enumerate().map(|(i, b)| (i+1) as i32 * f(24, b, &State { t: 1, ore: 0, cla: 0, obs: 0, dore: 1, dcla: 0, dobs: 0 })).sum::<i32>());
    println!("{}", blueprints[..3].iter().map(|b| f(32, b, &State { t: 1, ore: 0, cla: 0, obs: 0, dore: 1, dcla: 0, dobs: 0 })).product::<i32>());
}
