fn main() {
    let s = std::fs::read_to_string("../../../data/2022/12.input.txt").unwrap();
    let mut grid: Vec<Vec<u8>> = s.trim_end().lines().map(|l| l.trim_end().as_bytes().iter().copied().collect()).collect();
    let mut ps = (0, 0);
    let mut pe = (0, 0);
    let m = grid.len();
    let n = grid[0].len();
    for i in 0..m {
        for j in 0..n {
            if grid[i][j] == b'S' {ps = (i, j); grid[i][j] = b'a'; }
            if grid[i][j] == b'E' {pe = (i, j); grid[i][j] = b'z'; }
        }
    }
    for part in [1, 2] {
        let mut q = vec![if part == 1 {ps} else {pe}];
        let mut s: std::collections::HashSet<(usize, usize)> = std::collections::HashSet::new();
        s.insert(q[0]);
        let mut d = 0;
        'o: loop {
            let mut qq = vec![];
            for (i, j) in q.iter().copied() {
                if if part == 1 {(i, j) == pe} else {grid[i][j] == b'a'} {
                    break 'o;
                }
                let i = i as i32;
                let j = j as i32;
                for (ii, jj) in [(i, j+1), (i, j-1), (i-1, j), (i+1, j)] {
                    if ii < 0 || ii >= m as i32 || jj < 0 || jj >= n as i32 || s.contains(&(ii as usize, jj as usize)) 
                    || (|a, b| if part == 1 {a > b + 1} else {b > a + 1})(grid[ii as usize][jj as usize], grid[i as usize][j as usize]) {
                        continue;
                    }
                    qq.push((ii as usize, jj as usize));
                    s.insert((ii as usize, jj as usize));
                }
            }
            d += 1;
            q = qq;
        }
        println!("{}", d);
    }
}
