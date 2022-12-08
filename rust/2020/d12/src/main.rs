use std::fs::read_to_string;

fn main() {
    let s = read_to_string("../../../data/2020/12.input.txt").unwrap();
    let mut n = 0;
    let mut e = 0;
    let mut dn = 0;
    let mut de = 1;
    for l in s.trim_end().lines() {
        let l = l.as_bytes();
        let x: i32 = std::str::from_utf8(&l[1..]).unwrap().parse().unwrap();
        match l[0] {
            b'N' => {n += x;}
            b'S' => {n -= x;}
            b'E' => {e += x;}
            b'W' => {e -= x;}
            b'L' => {for _ in 0..x/90 {(dn, de) = (de, -dn);}}
            b'R' => {for _ in 0..x/90 {(dn, de) = (-de, dn);};}
            b'F' => {n += dn * x; e += de * x; }
            _ => {}
        }
    }
    println!("{}", n.abs() + e.abs());
    let mut n = 0;
    let mut e = 0;
    let mut dn = 1;
    let mut de = 10;
    for l in s.trim_end().lines() {
        let l = l.as_bytes();
        let x: i32 = std::str::from_utf8(&l[1..]).unwrap().parse().unwrap();
        match l[0] {
            b'N' => {dn += x;}
            b'S' => {dn -= x;}
            b'E' => {de += x;}
            b'W' => {de -= x;}
            b'L' => {for _ in 0..x/90 {(dn, de) = (de, -dn);}}
            b'R' => {for _ in 0..x/90 {(dn, de) = (-de, dn);};}
            b'F' => {n += dn * x; e += de * x; }
            _ => {}
        }
    }
    println!("{}", n.abs() + e.abs());
}
