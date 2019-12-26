m = Transpose[{{5, -1, 0, 0},
{-1, 3, 0, 0},
{0, -1, 4, 0},
{-1, 0, 0, 2}}]

f[x1_,x2_,x3_,x4_] := Times @@ (m.{x1,x2,x3,x4})

crits = Solve[D[f[x1,x2,x3,x4], x1] == D[f[x1,x2,x3,x4], x2] == D[f[x1,x2,x3,x4], x3] == D[f[x1,x2,x3,x4], x4] && x1+x2+x3+x4 == 100]

solr = crits // Map[{x1, x2, x3, x4, f[x1, x2, x3, x4]}//.# &, #] & // Select[#[[5]] > 0&] //  #[[1]][[1;;4]]&

nbs[x_] = {Floor[x], Floor[x+1]}

Print[ Tuples[nbs /@ solr] // Select[ Total[#] == 100 &] // MaximalBy[f @@ # &] // f @@ First[#] &] 

crits2 = Solve[
    {D[f[x1,x2,x3,x4], x1], D[f[x1,x2,x3,x4], x2], D[f[x1,x2,x3,x4], x3], D[f[x1,x2,x3,x4], x4]} == {1,1,1,1} a + {5,1,6,8} b && x1+x2+x3+x4 == 100 && 
    {5,1,6,8}.{x1,x2,x3,x4} == 500 && x1 >= 0 && x2 >= 0 && x3 >= 0 && x4 >= 0
    ]

solr2 = crits2 // Map[{x1, x2, x3, x4, f[x1, x2, x3, x4]}//.# &, #] & // Select[#[[5]] > 0&] //  #[[1]][[1;;4]]&

nbs2[x_] := Range[Floor[x]-10, Floor[x]+10]

Print[ Tuples[nbs2 /@ solr2] // Select[ Total[#] == 100 && {5,1,6,8}.# == 500 &] // MaximalBy[f @@ # &] // f @@ First[#] &] 

