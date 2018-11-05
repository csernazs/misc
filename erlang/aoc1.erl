-module(aoc1).
-export([solve/1, solve_list/1]).


read_all_contents(File) ->
    Result = file:read(File, 1024),
    read_all_contents(File, Result).


read_all_contents(File, {ok, Data}) ->
    case file:read(File, 1024) of
        {ok, Buffer} ->
            read_all_contents(File, {ok, Data ++ Buffer});
        eof ->
            Data
    end.


parseint(String) ->
    {Retval, []} = string:to_integer(String),
    Retval.


read_file(Filename) ->
    {ok, F} = file:open(Filename, read),
    [parseint([L]) || L <- string:trim(read_all_contents(F))].

solve_list([A,A|Remaining]) -> [A|solve_list([A|Remaining])];
solve_list([_,H|Remaining]) -> [0|solve_list([H|Remaining])];
solve_list([_]) -> [0].

solve_sides([A|Remaining]) ->
    case lists:last(Remaining) of
        A -> A;
        _ -> 0
    end.


solve(Filename) ->
    Data = read_file(Filename),
    lists:sum(solve_list(Data)) + solve_sides(Data).
