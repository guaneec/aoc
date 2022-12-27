const DIRS: [(i16, i16); 7] = [(-1,0), (1,0), (0,-1), (0,1), (-1,0), (1,0), (0,-1)];
const D8: [(i16, i16); 8] = [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)];
type Elf = (i16, i16);
const R: usize = 128;

#[derive(Clone, Copy, PartialEq, Eq)]
enum State {
    Empty,
    Neutral,
    Up,
    Down,
    Left,
    Right,
}
const STATES: [State; 7] = [State::Up, State::Down, State::Left, State::Right, State::Up, State::Down, State::Left];

#[derive(Clone)]
struct Elves([[State; 2*R]; 2*R], Vec<Elf>);

fn main() {
    let s = std::fs::read_to_string("../../../data/2022/23.input.txt").unwrap();
    let mut elves = Elves([[State::Empty; 2*R]; 2*R], vec![]);
    for (i, l) in s.lines().enumerate() {
        for (j, c) in l.chars().enumerate() {
            if c == '#' {
                elves.0[i + R][j + R] = State::Neutral;
                elves.1.push(((i+R) as i16, (j+R) as i16))
            }
        }
    }
    {
        let mut elves = elves.clone();
        for i in 0..10 {
            step(&mut elves, i);
        }
        let imn = elves.1.iter().map(|e| e.0).min().unwrap();
        let imx = elves.1.iter().map(|e| e.0).max().unwrap();
        let jmn = elves.1.iter().map(|e| e.1).min().unwrap();
        let jmx = elves.1.iter().map(|e| e.1).max().unwrap();
        println!("{}", (imx-imn+1)*(jmx-jmn+1)-elves.1.len() as i16);
    }
    
    {
        let mut elves = elves.clone();
        for i in 0.. {
            if !step(&mut elves, i) {
                println!("{}", i+1);
                break;
            }
        }
    }
}

fn step(elves: &mut Elves, i: usize) -> bool {
    // move up 
    let mut moved = 0;
    for &e in &elves.1 {
        mark(&mut elves.0, e, i);
    }
    for (i, j) in elves.1.iter_mut() {
        let x = elves.0[*i as usize][*j as usize];
        let (ii, jj) = match x {
            State::Up => (*i-1, *j),
            State::Down => (*i+1, *j),
            State::Left => (*i, *j-1),
            State::Right => (*i, *j+1),
            _ => { continue; }
        };
        if elves.0[ii as usize][jj as usize] == State::Empty {
            elves.0[ii as usize][jj as usize] = State::Neutral;
            moved += 1;
        } else {
            assert!(elves.0[ii as usize][jj as usize] == State::Neutral);
            elves.0[ii as usize][jj as usize] = State::Empty;
            elves.0[*i as usize][*j as usize] = State::Neutral;
            elves.0[(ii*2-*i) as usize][(jj*2-*j) as usize] = State::Neutral;
            moved -= 1;
        }
    }
    for (i, j) in elves.1.iter_mut() {
        let x = elves.0[*i as usize][*j as usize];
        if x == State::Neutral { 
            continue; 
        }
        elves.0[*i as usize][*j as usize] = State::Empty;
        (*i, *j) = match x {
            State::Up => (*i-1, *j),
            State::Down => (*i+1, *j),
            State::Left => (*i, *j-1),
            State::Right => (*i, *j+1),
            _ => { panic!(); }
        };
    }
    moved > 0
}

fn mark(elves: &mut [[State; 2*R]; 2*R], elf: Elf, t: usize) {
    if D8.iter().all(|&(di, dj)| elves[(di+elf.0) as usize][(dj+elf.1) as usize] == State::Empty) { return; }
    for (&(di, dj), &state) in DIRS[t%4..t%4+4].iter().zip(STATES[t%4..t%4+4].iter()) {
        if D8.iter().filter(|&(ddi, ddj)| di*ddi+dj*ddj == 1).all(|&(ddi, ddj)| elves[(ddi+elf.0) as usize][(ddj+elf.1) as usize] == State::Empty) {
            elves[elf.0 as usize][elf.1 as usize] = state;
            return;
        }
    }
}