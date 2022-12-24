const W: usize = 128;
const H: usize = 32;

type Buf = [[bool; W]; H];
type Buf4 = [[bool; 2 * W]; 2 * H];

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/24.input.txt").unwrap();
    let m = s.split_terminator('\n').count();
    let n = s.split_terminator('\n').next().unwrap().len();
    let i0 = 1;
    let i1 = m;
    let mut j0 = 0;
    let mut j1 = 0;
    let mut lefts: Buf4 = [[true; 2 * W]; 2 * H];
    let mut rights: Buf4 = [[true; 2 * W]; 2 * H];
    let mut ups: Buf4 = [[true; 2 * W]; 2 * H];
    let mut downs: Buf4 = [[true; 2 * W]; 2 * H];
    for (i, line) in s.split_terminator('\n').enumerate() {
        for (j, c) in line.chars().enumerate() {
            match c {
                '.' => {
                    if i + 1 == i0 {
                        j0 = j + 1;
                    }
                    if i + 1 == i1 {
                        j1 = j + 1;
                    }
                }
                '#' => {}
                _ => {
                    let a = match c {
                        '<' => &mut lefts,
                        '>' => &mut rights,
                        '^' => &mut ups,
                        'v' => &mut downs,
                        _ => panic!(),
                    };
                    a[i + 1][j + 1] = false;
                    a[i + 1 + m - 2][j + 1] = false;
                    a[i + 1 + m - 2][j + 1 + n - 2] = false;
                    a[i + 1][j + 1 + n - 2] = false;
                }
            }
        }
    }
    let f = |t0: i32, start: (usize, usize), end: (usize, usize)| {
        let mut q: Buf = [[false; W]; H];
        q[start.0][start.1] = true;
        for t in t0.. {
            if q[end.0][end.1] {
                return t;
            }
            let mut qq = q.clone();
            for i in 1..=m {
                for j in 1..=n {
                    qq[i][j] |= q[i - 1][j] | q[i + 1][j] | q[i][j - 1] | q[i][j + 1];
                }
            }
            for i in 2..=m - 1 {
                for j in 2..=n - 1 {
                    let (n, m) = (n as i32, m as i32);
                    qq[i][j] &= lefts[i][j + (t + 1).rem_euclid(n - 2) as usize]
                        & rights[i][j + (-t - 1).rem_euclid(n - 2) as usize]
                        & ups[i + (t + 1).rem_euclid(m - 2) as usize][j]
                        & downs[i + (-t - 1).rem_euclid(m - 2) as usize][j];
                }
            }
            for j in 1..=n {
                qq[i0][j] &= j == j0;
                qq[i1][j] &= j == j1;
            }
            for i in 2..=m - 1 {
                qq[i][1] = false;
                qq[i][n] = false;
            }
            q = qq;
        }
        -1
    };
    let t1 = f(0, (i0, j0), (i1, j1));
    println!("{}", t1);
    let t2 = f(t1, (i1, j1), (i0, j0));
    let t3 = f(t2, (i0, j0), (i1, j1));
    println!("{}", t3);
}
