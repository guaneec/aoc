import { getInput } from "../aoc/util.js";

const s = getInput(2017, 7);
const es = s
  .trim()
  .split("\n")
  .map(x => {
    const [a, b] = x.split("->");
    const [_, bot, ws] = a.match(/(\w+)\s+\((\d+)\)/);
    const tops = b ? b.split(",").map(x => x.trim()) : [];
    return [bot, +ws, tops];
  });

const aa = new Set();
es.forEach(l => aa.add(l[0]));
es.forEach(l => l[2].forEach(x => aa.delete(x)));

const o = {};
es.forEach(([b, w, ts]) => {
  o[b] = [b, w, ts];
});

const root = [...aa][0];

const weights = {};
function calcWeight([b, w, ts]) {
  if (weights[b]) return weights[b];
  const ww = ts.reduce((a, b) => a + calcWeight(o[b]), w);
  weights[b] = ww;
  return ww;
};

const balanced = ([b, w, ts]) =>
  !ts.length || ts.every(x => weights[x] == weights[ts[0]]);

es.forEach(e => calcWeight(e));

function oddmode(xs) {
  if (xs[0] != xs[1]) {
    return xs[2] == xs[0] ? [xs[1], xs[0], 1] : [xs[0], xs[1], 0];
  }
  for (i = 2; i < xs.length; ++i) {
    if (xs[i] != xs[0]) return [xs[i], xs[0], i];
  }
}

function findtilt(b) {
  var [_, w, ts] = o[b];
  for (i = 0; i < ts.length; ++i) {
    if (!balanced(o[ts[i]])) return findtilt(ts[i]);
  }
  const wws = ts.map(x => weights[x]);
  var [od, mo, i] = oddmode(wws);
  return [o[ts[i]], o[ts[i]][1] - (od - mo)];
}

console.log(root);
console.log(findtilt(root)[1]);
