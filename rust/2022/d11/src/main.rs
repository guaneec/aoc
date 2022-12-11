#[derive(Debug)]
#[derive(Clone)]
struct Monke {
    items: Vec<u64>,
    opa: Option<u64>,
    opb: Option<u64>,
    add: bool,
    div: u64,
    dt: usize,
    df: usize,
    count: usize,
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/11.input.txt").unwrap();
        for p in [1, 2] {
        let mut monkes = Vec::new();
        let mut m = 1;
        for g in s.split("\n\n") {
            let mut lines = g.lines();
            lines.next().unwrap();
            let items = lines.next().unwrap().trim_end().split(": ").skip(1).next().unwrap().split(", ").map(|x| x.parse().unwrap()).collect();
            let mut it = lines.next().unwrap().trim_end().split("= ").skip(1).next().unwrap().split(" ");
            let opa = it.next().unwrap().parse().ok();
            let add = it.next().unwrap() == "+";
            let opb = it.next().unwrap().parse().ok();
            let div = lines.next().unwrap().trim_end().split("by ").skip(1).next().unwrap().parse().unwrap();
            m *= div;
            let dt = lines.next().unwrap().trim_end().split("monkey ").skip(1).next().unwrap().parse().unwrap();
            let df = lines.next().unwrap().trim_end().split("monkey ").skip(1).next().unwrap().parse().unwrap();
            monkes.push(Monke {items, opa, add, opb, div, dt, df, count: 0});
        }
        for _ in 0..if p == 1 {20} else {10000} {
            for i in 0..monkes.len() {
                let monke = monkes[i].clone();
                for &item in &monke.items {
                    let opa = monke.opa.unwrap_or(item);
                    let opb = monke.opb.unwrap_or(item);
                    let mut item = if monke.add {opa + opb} else {opa * opb};
                    if p == 1 { item /= 3; } else { item %= m; }
                    monkes[if item % monke.div == 0 {monke.dt} else {monke.df}].items.push(item);
                }
                monkes[i].count += monkes[i].items.len();
                monkes[i].items.clear();
            }
        }
        let (a, b) = monkes.iter().map(|monke| monke.count).fold((0, 0), |(a, b), c| if c > a {(c, a)} else if c > b {(a, c)} else {(a, b)});
        println!("{}", a * b);      
    }
}
