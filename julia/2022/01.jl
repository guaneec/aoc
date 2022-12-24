a = read("../../data/2022/01.input.txt", String) |> strip |> s->split(s, "\n\n") |> g->map(sum ∘(a->map(s->parse(Int,s), a)) ∘ split, g) |> a->sort!(a,rev=true)
a[1] |> println
a[1:3] |> sum |> println