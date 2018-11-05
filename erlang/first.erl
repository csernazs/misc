-module(first).
-compile(export_all).


help_me(Animal) ->
    Talk = if Animal == cat  -> "meow";
        Animal == beef -> "mooo";
        Animal == dog  -> "bark";
        Animal == tree -> "bark";
        true -> "fgdadfgna"
    end,
    {Animal, "says " ++ Talk ++ "!"}.



