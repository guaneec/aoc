use std::str::FromStr;
use std::ops::{Add, Mul};

use regex::Regex;

#[derive(PartialEq, Eq, Clone, Copy)]
struct V3(i32, i32, i32);
struct Face {
    topleft2: (i32, i32),
    topleft3: V3,
    ei: V3,
    ej: V3,
}

fn cross(a: V3, b: V3) -> V3 {
    V3(a.1*b.2-a.2*b.1, a.2*b.0-a.0*b.2, a.0*b.1-a.1*b.0)
}

fn dot(a: V3, b: V3) -> i32 {
    a.0*b.0+a.1*b.1+a.2*b.2
}

impl Add for V3 {
    type Output = V3;

    fn add(self, rhs: Self) -> Self::Output {
        V3(self.0+rhs.0, self.1+rhs.1, self.2+rhs.2)
    }
}

impl Mul<i32> for V3 {
    type Output = V3;

    fn mul(self, a: i32) -> Self::Output {
        V3(self.0*a, self.1*a, self.2*a)
    }
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/22.input.txt").unwrap();
    let a = (s.bytes().map(|c| (c == b'#' || c == b'.') as i32 as f64).sum::<f64>() / 6.).sqrt() as i32;
    let mut it = s.split("\n\n");
    let map: Vec<_> = it.next().unwrap().split_terminator('\n').collect();
    let cmds = it.next().unwrap();
    let pattern = Regex::from_str("[0-9]+|L|R").unwrap();
    let oob = |i: i32, j: i32| {
        i < 0 || j < 0 || i >= map.len() as i32 || j >= map[i as usize].len() as i32 || map[i as usize].as_bytes()[j as usize] == b' '
    };
    let imin: Vec<i32> = (0..).map_while(|j| 
        map.iter().enumerate().filter_map(|(i, r)| 
        r.as_bytes().get(j).filter(|&c| *c != b' ').map(|_c| i as i32)).min()
    ).collect();
    let imax: Vec<i32> = (0..).map_while(|j| 
        map.iter().enumerate().filter_map(|(i, r)| 
        r.as_bytes().get(j).filter(|&c| *c != b' ').map(|_c| i as i32)).max()
    ).collect();
    let jmin: Vec<i32> = map.iter().map(|&r| r.bytes().position(|c| c != b' ').unwrap() as i32).collect();
    let jmax: Vec<i32> = map.iter().map(|&r| r.bytes().rposition(|c| c != b' ').unwrap() as i32).collect();
    let i0 = 0;
    let j0 = map[0].find('.').unwrap() as i32;
    let mut i = i0;
    let mut j = j0;
    let mut di = 0;
    let mut dj = 1;
    for cmd in pattern.find_iter(&cmds) {
        match cmd.as_str() {
            "L" => { (di, dj) = (-dj, di); }
            "R" => { (di, dj) = (dj, -di); }
            x => {
                let x: i32 = x.parse().unwrap();
                for _ in 0..x {
                    let mut ii = i + di;
                    let mut jj = j + dj;
                    if oob(ii, jj) {
                        match (di, dj) {
                            (-1,0) => { ii = imax[j as usize]; }
                            (1,0) =>  { ii = imin[j as usize]; }
                            (0,-1) => { jj = jmax[i as usize]; }
                            (0,1) => { jj = jmin[i as usize]; }
                            _ => panic!()
                        }
                    }
                    if map[ii as usize].as_bytes()[jj as usize] == b'.' {
                        (i, j) = (ii, jj);
                    } else { break; }
                }
            }
        }
    }
    let p1 = 1000 * (i+1) + 4 * (j+1) + match (di, dj) {
        (-1,0) => 3,
        (1,0) =>  1,
        (0,-1) => 2,
        (0,1) => 0,
        _ => panic!()
    };
    println!("{}", p1);

    let mut faces: Vec<Face> = vec![];
    let mut q = vec![((i0, j0), V3(0, 0, 0), V3(1, 0, 0), V3(0, 1, 0))];
    while !q.is_empty() {
        let (r2, r3, ei, ej) = q.pop().unwrap();
        if oob(r2.0, r2.1) || faces.iter().any(|f| f.topleft2 == r2) { continue; }
        faces.push(Face { topleft2: r2, topleft3: r3, ei, ej });
        q.push(((r2.0+a, r2.1), r3+ei*(a-1), cross(ei, ej), ej));
        q.push(((r2.0-a, r2.1), r3+cross(ei, ej)*(a-1), cross(ej, ei), ej));
        q.push(((r2.0, r2.1+a), r3+ej*(a-1), ei, cross(ei, ej)));
        q.push(((r2.0, r2.1-a), r3+cross(ei, ej)*(a-1), ei, cross(ej, ei)));
    }    
    let mut i = i0;
    let mut j = j0;
    let mut di = 0;
    let mut dj = 1;
    for cmd in pattern.find_iter(&cmds) {
        match cmd.as_str() {
            "L" => { (di, dj) = (-dj, di); }
            "R" => { (di, dj) = (dj, -di); }
            x => {
                let x: i32 = x.parse().unwrap();
                for _ in 0..x {
                    let mut ii = i + di;
                    let mut jj = j + dj;
                    let mut dii = di;
                    let mut djj = dj;
                    if oob(ii, jj) {
                        let f = faces.iter().find(|&f| f.topleft2 == (i/a*a,j/a*a)).unwrap();
                        let v = f.ei * -di + f.ej * -dj;
                        let r = f.topleft3 + f.ei * (i%a) + f.ej * (j%a);
                        let f2 = faces.iter().find(|&f| cross(f.ei, f.ej) == v).unwrap();
                        ii = f2.topleft2.0 + dot(r+f2.topleft3*-1, f2.ei);
                        jj = f2.topleft2.1 + dot(r+f2.topleft3*-1, f2.ej);
                        dii = dot(cross(f.ei, f.ej), f2.ei);
                        djj = dot(cross(f.ei, f.ej), f2.ej);
                    }
                    if map[ii as usize].as_bytes()[jj as usize] == b'.' {
                        (i, j, di, dj) = (ii, jj, dii, djj);
                    } else { break; }
                }
            }
        }
    }
    let p2 = 1000 * (i+1) + 4 * (j+1) + match (di, dj) {
        (-1,0) => 3,
        (1,0) =>  1,
        (0,-1) => 2,
        (0,1) => 0,
        _ => panic!()
    };
    println!("{}", p2);
}
