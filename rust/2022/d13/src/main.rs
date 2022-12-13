#[derive(Eq, Clone)]
enum Elem {
    Item(i32),
    Sub(Vec<Elem>),
}

fn consume(s: &[u8], i: usize) -> (Elem, usize) {
    let mut i = i;
    if s[i] == b'[' {
        i += 1;
        let mut v = vec![];
        while s[i] != b']' {
            let (e, ii) = consume(s, i);
            i = ii;
            v.push(e);
            if s[i] == b',' { i += 1; }
        }
        (Elem::Sub(v), i + 1)
    } else {
        let mut x = 0;
        while s[i].is_ascii_digit() {
            x = x * 10 + (s[i] - b'0') as i32;
            i += 1;
        }
        (Elem::Item(x), i)
    }
}

impl Ord for Elem {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        match (self, other) {
            (Self::Item(l0), Self::Item(r0)) => l0.cmp(r0),
            (Self::Sub(l0), Self::Sub(r0)) => l0.cmp(r0),
            (Self::Sub(l0), Self::Item(r0)) => l0.cmp(&vec![Self::Item(*r0)]),
            (Self::Item(l0), Self::Sub(r0)) => vec![Self::Item(*l0)].cmp(r0),
        }
    }
}

impl PartialOrd for Elem {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for Elem {
    fn eq(&self, other: &Self) -> bool {
        self.cmp(other) == std::cmp::Ordering::Equal
    }
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/13.input.txt").unwrap();
    let e2 = consume("[[2]]".as_bytes(), 0).0;
    let e6 = consume("[[6]]".as_bytes(), 0).0;
    let mut v = vec![e2.clone(), e6.clone()];
    let mut o = 0;
    for (i, g) in s.split("\n\n").enumerate() {
        let mut lines = g.lines();
        let left = consume(lines.next().unwrap().as_bytes(), 0).0;
        let right = consume(lines.next().unwrap().as_bytes(), 0).0;
        if left < right {
            o += i + 1;
        }
        v.push(left);
        v.push(right);
    }
    println!("{}", o);
    v.sort();
    let i2 =  v.iter().position(|e| e == &e2).unwrap() + 1;
    let i6 =  v.iter().position(|e| e == &e6).unwrap() + 1;
    println!("{}", i2 * i6);
}
