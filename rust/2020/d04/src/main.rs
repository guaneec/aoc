use std::{
    collections::{HashMap, HashSet},
    fs::File,
    io::{self, BufReader, Read},
    num::ParseIntError,
};

struct Passport<'a> {
    byr: u32,
    iyr: u32,
    eyr: u32,
    hgt: u32,
    unit: &'a str,
    hcl: &'a str,
    ecl: &'a str,
    pid: &'a str,
}

fn main() -> io::Result<()> {
    let f = File::open("../../../data/2020/04.input.txt")?;
    let mut f = BufReader::new(f);
    let mut s = String::new();
    let reqs = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        .into_iter()
        .collect::<HashSet<_>>();
    f.read_to_string(&mut s)?;
    let p1 = s
        .split("\n\n")
        .map(|ls| {
            ls.trim_end()
                .split(|c| c == ' ' || c == '\n')
                .map(|kv| {
                    let mut it = kv.split(':');
                    let k = it.next().unwrap();
                    let v = it.next().unwrap();
                    (k, v)
                })
                .map(|(k, _)| k)
                .collect::<HashSet<_>>()
        })
        .filter(|s| s.is_superset(&reqs))
        .count();
    let ecls: HashSet<_> = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        .into_iter()
        .collect();
    let p2 = s
        .split("\n\n")
        .map(|ls| {
            ls.trim_end()
                .split(|c| c == ' ' || c == '\n')
                .map(|kv| {
                    let mut it = kv.split(':');
                    let k = it.next().unwrap();
                    let v = it.next().unwrap();
                    (k, v)
                })
                .collect::<HashMap<_, _>>()
        })
        .filter(|h| reqs.iter().all(|k| h.contains_key(*k)))
        .map(|h| {
            let byr = h.get("byr").unwrap().parse::<u32>().unwrap();
            let iyr = h.get("iyr").unwrap().parse::<u32>().unwrap();
            let eyr = h.get("eyr").unwrap().parse::<u32>().unwrap();
            let sh = h.get("hgt").unwrap();
            let nh = sh.len();
            let hgt = sh[..nh - 2].parse()?;
            let unit = &sh[nh - 2..];
            let hcl = h.get("hcl").unwrap();
            let ecl = h.get("ecl").unwrap();
            let pid = h.get("pid").unwrap();

            Ok(Passport {
                byr,
                ecl,
                eyr,
                hcl,
                hgt,
                iyr,
                pid,
                unit,
            })
        })
        .filter(|t: &Result<Passport, ParseIntError>| match t {
            Ok(p) => {
                1920 <= p.byr
                    && p.byr <= 2002
                    && 2010 <= p.iyr
                    && p.iyr <= 2020
                    && 2020 <= p.eyr
                    && p.eyr <= 2030
                    && (p.unit == "cm" && 150 <= p.hgt && p.hgt <= 193
                        || p.unit == "in" && 59 <= p.hgt && p.hgt <= 76)
                    && p.hcl.starts_with('#')
                    && p.hcl.bytes().skip(1).all(|c| c.is_ascii_hexdigit())
                    && ecls.contains(p.ecl)
                    && p.pid.len() == 9
                    && p.pid.bytes().all(|c| c.is_ascii_digit())
            }
            _ => false,
        })
        .count();
    println!("{} {}", p1, p2);
    Ok(())
}
