use std::collections::HashSet;

struct Blizzard {
    i0: i32,
    j0: i32,
    di: i32,
    dj: i32,
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/24.input.txt").unwrap();
    let mut blizzards = vec![];
    let m = s.split_terminator('\n').count() as i32;
    let n = s.split_terminator('\n').next().unwrap().len() as i32;
    let i0 = 0;
    let i1 = m - 1;
    let mut j0 = 0;
    let mut j1 = 0;
    for (i, line) in s.split_terminator('\n').enumerate() {
        for (j, c) in line.chars().enumerate() {
            let (i, j) = (i as i32, j as i32);
            match c {
                '.' => {
                    if i == i0 { j0 = j; }
                    if i == i1 { j1 = j; }
                }
                '#' => {}
                _ => {
                    blizzards.push( Blizzard {
                        i0: i, j0: j, 
                        di: match c {'^' => -1, 'v' => 1, _ => 0}, 
                        dj: match c {'<' => -1, '>' => 1, _ => 0}, 
                    })
                }
            }
        }
    }
    let f = |t0: i32, start, end| {
        let mut q: HashSet<(i32, i32)> = [start].into_iter().collect();
        for t in t0.. {
            let blocked: HashSet<(i32, i32)> = blizzards.iter().map(|b| (
                1 + (b.i0 - 1 + b.di * (t + 1)).rem_euclid(m - 2),
                1 + (b.j0 - 1 + b.dj * (t + 1)).rem_euclid(n - 2),
            )).collect();
            assert!(!q.is_empty());
            let mut qq = vec![];
            for &(i, j) in q.iter() {
                if (i, j) == end { return t; }
                for (ii, jj) in [(i,j),(i,j-1),(i,j+1),(i-1,j),(i+1,j)] {
                    if (ii, jj) == start || (ii, jj) == end || (
                        ii > 0 && ii < m-1 && jj > 0 && jj < n-1 && !blocked.contains(&(ii, jj))
                    ) { qq.push((ii, jj)); }
                }
            }
            q = qq.into_iter().collect();
        }
        panic!()
    };
    let t1 = f(0, (i0, j0), (i1, j1));
    println!("{}", t1);
    let t2 = f(t1, (i1, j1), (i0, j0));
    let t3 = f(t2, (i0, j0), (i1, j1));
    println!("{}", t3);
}
