use regex::Regex;

struct Blueprint {
    oreore: i32,
    claore: i32,
    obsore: i32,
    obscla: i32,
    geoore: i32,
    geoobs: i32,
}

fn ceildiv(a: i32, b: i32) -> i32 {
    if b == 0 {87878787} else {(a+b-1)/b}
}

fn maxgeo(end: i32, b: &Blueprint, t: i32, ore: i32, cla: i32, obs: i32, geo: i32, dore: i32, dcla: i32, dobs: i32, dgeo: i32) -> i32 {
    let mut m = geo + (end + 1 - t) * dgeo;
    let tt = end-2-t;
    let dt = ceildiv(0.max(b.oreore-ore), dore) + 1;
    if tt > 0 && ore+dore*(tt-1)< [b.oreore, b.claore, b.obsore, b.geoore].into_iter().max().unwrap()*tt && t+dt<=end {
        m = m.max(maxgeo(end, &b, t+dt, ore+dt*dore-b.oreore, cla+dt*dcla, obs+dt*dobs, geo+dt*dgeo, dore+1, dcla, dobs, dgeo));
    }
    let tt = end-4-t;
    let dt = ceildiv(0.max(b.claore-ore), dore) + 1;
    if tt > 0 && cla+dcla*(tt-1)< b.obscla*tt && t+dt<=end {
        m = m.max(maxgeo(end, &b, t+dt, ore+dt*dore-b.claore, cla+dt*dcla, obs+dt*dobs, geo+dt*dgeo, dore, dcla+1, dobs, dgeo));
    }
    let tt = end-2-t;
    let dt = ceildiv(0.max(b.obsore - ore), dore).max(ceildiv(0.max(b.obscla - cla), dcla)) + 1;
    if tt > 0 && obs+dobs*(tt-1)<b.geoobs*tt && t+dt<= end {
        m = m.max(maxgeo(end, &b, t+dt, ore+dt*dore-b.obsore, cla+dt*dcla-b.obscla, obs+dt*dobs, geo+dt*dgeo, dore, dcla, dobs+1, dgeo));
    }
    let dt = ceildiv(0.max(b.geoore - ore), dore).max(ceildiv(0.max(b.geoobs - obs), dobs)) + 1;
    if t+dt<=end {
        m = m.max(maxgeo(end, &b, t+dt, ore+dt*dore-b.geoore, cla+dt*dcla, obs+dt*dobs-b.geoobs, geo+dt*dgeo, dore, dcla, dobs, dgeo+1));
    }
    m
}

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/19.input.txt").unwrap();
    let re = Regex::new("[0-9]+").unwrap();
    let blueprints: Vec<_> = s.split_terminator('\n').map(|l| {
        let mut matches = re.find_iter(l).skip(1);
        Blueprint {
            oreore: matches.next().unwrap().as_str().parse().unwrap(),
            claore: matches.next().unwrap().as_str().parse().unwrap(),
            obsore: matches.next().unwrap().as_str().parse().unwrap(),
            obscla: matches.next().unwrap().as_str().parse().unwrap(),
            geoore: matches.next().unwrap().as_str().parse().unwrap(),
            geoobs: matches.next().unwrap().as_str().parse().unwrap(),
        }
    }).collect();
    println!("{}", blueprints.iter().enumerate().map(|(i, b)| (i+1) as i32 * maxgeo(24, b, 1, 0, 0, 0, 0, 1, 0, 0, 0)).sum::<i32>());
    println!("{}", blueprints[..3].iter().map(|b| maxgeo(32, b, 1, 0, 0, 0, 0, 1, 0, 0, 0)).product::<i32>());
}
