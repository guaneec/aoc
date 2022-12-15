use regex::Regex;

struct Sensor {
    x: i32,
    y: i32,
    d: i32,
}

const Y: i32 = 2000000;

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/15.input.txt").unwrap();
    let re = Regex::new(r"^Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)").unwrap();
    let mut sensors = vec![];
    let mut beacons = std::collections::HashSet::new();
    let mut events = vec![];
    for l in s.trim_end().lines() {
        let cap = re.captures(l).unwrap();
        let sx: i32 = cap.get(1).unwrap().as_str().parse().unwrap();
        let sy: i32 = cap.get(2).unwrap().as_str().parse().unwrap();
        let bx: i32 = cap.get(3).unwrap().as_str().parse().unwrap();
        let by: i32 = cap.get(4).unwrap().as_str().parse().unwrap();
        let d = (sx-bx).abs()+(sy-by).abs();
        let dx = d - (Y-sy).abs();
        if dx >= 0 {
            events.extend([(sx-dx, 1), (sx+dx+1, -1)]);
            if by == Y { beacons.insert(bx); }
        }
        sensors.push(Sensor {x: sx, y: sy, d });
    }
    let mut p1 = -(beacons.len() as i32);
    let mut prev = 0;
    let mut c = 0;
    events.sort();
    for (x, v) in events.iter() {
        p1 += if c > 0 {x - prev} else { 0 };
        c += v;
        prev = *x;
    }
    println!("{}", p1);
    let u2s: Vec<_> = sensors.iter().map(|s| s.x + s.y + s.d).collect();
    let isin = |x: i32, y: i32| sensors.iter().any(|s| (s.x-x).abs() + (s.y-y).abs() <= s.d);
    'o: for u1 in sensors.iter().map(|s| s.x + s.y - s.d).filter(|&u1| u2s.iter().any(|&u2| u2 + 2 == u1)) {
        for v2 in sensors.iter().map(|s| s.x - s.y + s.d) {
            let x = (u1 + v2) / 2;
            let y = (u1 - v2 - 2) / 2;
            if !isin(x, y) && x > 0 && y > 0 && x < 4000000 && y < 4000000 {
                println!("{}", (x as i64) * 4000000 + (y as i64));
                break 'o;
            }
        }
    }
}
