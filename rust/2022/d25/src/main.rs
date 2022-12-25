use std::str::FromStr;
use std::iter::Sum;
use std::fmt::Display;

struct Snafu(i64);

#[derive(Debug)]
struct SnafuErr;

impl FromStr for Snafu {
    type Err = SnafuErr;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut b = 1;
        let mut o = 0;
        for c in s.chars().rev() {
            o += ("=-012".chars().position(|d| d == c).ok_or(SnafuErr)? as i64 - 2) * b;
            b *= 5;
        }
        return Ok(Snafu(o));
    }
}

impl Sum for Snafu {
    fn sum<I: Iterator<Item = Self>>(iter: I) -> Self {
        Snafu(iter.map(|s| s.0).sum())
    }
}

impl Display for Snafu {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut buf = vec![];
        let mut x = self.0;
        while x != 0 {
            let r = x.rem_euclid(5);
            buf.push(['0', '1', '2', '=', '-'][r as usize]);
            x = (x - r) / 5 + (r > 2) as i64;
        }
        if buf.is_empty() { buf.push('0'); }
        write!(f, "{}", String::from_iter(buf.iter().rev()))
    }
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/25.input.txt").unwrap();
    let sum: Snafu = s.split_terminator('\n').map(|l| l.parse().unwrap()).sum();
    println!("{}", sum);
}
