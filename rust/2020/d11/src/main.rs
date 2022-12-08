use std::fs::read_to_string;

const DIRS: [(isize, isize); 8] = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)];

fn main() {
    let s = read_to_string("../../../data/2020/11.input.txt").unwrap();
    for p in [1, 2] {
        let mut plane: Vec<Vec<_>> = s.trim_end().lines().map(|l| l.trim_end().as_bytes().iter().copied().collect()).collect();
        let m = plane.len();
        let n = plane[0].len();
        loop {
            let adj = |i, j| {
                let plane = &plane;
                if p == 1 {
                    DIRS.into_iter()
                        .map(move |(dx, dy)| (i as isize + dx, j as isize + dy))
                        .filter(move |(xx, yy)| *xx >= 0 && *xx < m as isize && *yy >= 0 && *yy < n as isize)
                        .map(|(xx, yy)| plane[xx as usize][yy as usize]).collect::<Vec<_>>().into_iter()
                } else {
                    DIRS.into_iter()
                        .filter_map(move |(dx, dy)| (1..).map(|k| 
                            (i as isize +k*dx, j as isize +k*dy)).take_while(|&(ii, jj)| 0 <= ii && ii < m as isize && 0 <= jj && jj < n as isize)
                            .map(|(ii, jj)| plane[ii as usize][jj as usize]).filter( |&c| c != b'.').next()).collect::<Vec<_>>().into_iter()
                }
            };
            let mut tmp = plane.clone();
            for i in 0..m {
                for j in 0..n {
                    if plane[i][j] == b'L' && adj(i, j).filter(|&c| c == b'#').count() == 0 {
                        tmp[i][j] = b'#';
                    } else if plane[i][j] == b'#' && adj(i, j).filter(|&c| c == b'#').count() >= if p == 1 {4} else {5} {
                        tmp[i][j] = b'L';
                    }
                }
            }
            if tmp == plane {
                break;
            }
            plane = tmp;
        }
        println!("{}", plane.iter().map(|r| r.iter().filter(|&&c| c == b'#').count()).sum::<usize>());
    }
}
