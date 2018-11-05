-module(aoc2).
-export([solve/1, minmax/1]).

localmin(A, B) when A<B -> A;
localmin(A, B) when A>=B -> B.

localmax(A, B) when A>B -> A;
localmax(A, B) when A=<B -> B.


minmax([H|T]) ->
    minmax(T, H, H).

minmax([H|T], LocalMin, LocalMax) ->
    NewMin = localmin(H, LocalMin),
    NewMax = localmax(H, LocalMax),
    minmax(T, NewMin, NewMax);

minmax([], LocalMin, LocalMax) ->
    {LocalMin, LocalMax}.

solve_row(Row) ->
    {Min, Max} = minmax(Row),
    Max-Min.

solve(Matrix) ->
    lists:sum([solve_row(R) || R <- Matrix]).



