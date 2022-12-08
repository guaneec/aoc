fn main() {
    let s = std::fs::read_to_string("../../../data/2020/13.input.txt").unwrap();
    let mut lines = s.lines();
    let t0: i64 = lines.next().unwrap().parse().unwrap();
    let times: Vec<Option<i64>> = lines.next().unwrap().split(",").map(|x| if x == "x" { None } else {Some(x.parse().unwrap())}).collect();
    let (wait, bus) = times.iter().filter_map(|&x| x).map(|x| ((t0 - 1) / x * x + x - t0, x)).min().unwrap();
    println!("{}", wait * bus);
    let mut p: i64 = 1;
    let mut r: i64 = 0;
    for (k, &v) in times.iter().enumerate() {
        match v {
            Some(v) => {
                r = (0..).map(|y| r + y * p as i64).find(|&y| y % v == (v-k as i64 % v) % v).unwrap();
                p *= v;
            }   
            _ => {}
        }
    }
    println!("{}", r);
}
