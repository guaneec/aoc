use std::fs::read_to_string;

const DIRS: [(isize, isize); 4] = [(0, 1), (0, -1), (-1, 0), (1, 0)];

struct Sight<'a> {
    i: isize,
    j: isize,
    di: isize,
    dj: isize,
    m: usize,
    n: usize,
    map: &'a Vec<&'a[u8]>,
}

impl Iterator for Sight<'_> {
    type Item = u8;

    fn next(&mut self) -> Option<Self::Item> {
        self.i += self.di;
        self.j += self.dj;
        if !(0 <= self.i && self.i < self.m as isize && 0 <= self.j && self.j < self.n as isize) {
            None
        } else {
            Some(self.map[self.i as usize][self.j as usize])
        }
    }
}

fn main() {
    let s = read_to_string("../../../data/2022/08.input.txt").unwrap();
    let map = s.trim_end().lines().map(|s| s.trim_end().as_bytes()).collect::<Vec<_>>();
    let m = map.len();
    let n = map[0] .len();
    let p1: usize = (0..m).map(|i| (0..n).filter(|&j| 
        DIRS.iter().any(|&(di, dj)| (Sight {i: i as isize, j: j as isize, di, dj, m, n, map: &map}).all(|t| t < map[i][j]))).count()).sum();
    let p2 = (0..m).map(|i| (0..n).map(|j| 
        DIRS.iter().map(|&(di, dj)| 
        (Sight {i: i as isize, j: j as isize, di, dj, m, n, map: &map}).take_while(|&t| t < map[i][j]).count()
        + (Sight {i: i as isize, j: j as isize, di, dj, m, n, map: &map}).skip_while(|&t| t < map[i][j]).next().is_some() as usize
    ).product::<usize>()
    ).max().unwrap()).max().unwrap();
    println!("{}", p1);
    println!("{}", p2);
}
