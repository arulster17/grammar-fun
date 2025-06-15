# grammar-fun

Some functionalities provided:

- Determine if grammar is LL(1).
- Convert non-LL(1) grammar to LL(1) (if possible).

Input Grammar File Format

```
Comments
>>>
Comma separated Ts (does not include EOF)
>>>
Comma separated NTs
>>>
Line separated Prod Rules in form NT -> e U (T U NT)^+ (do not include file -> root EOF)
```

Example Grammar that matches regex `R = a+`

```
This grammar matches regex R = a+. Terminal A represents 'a'.
>>>
A
>>>
ap,as
>>>
ap -> A as
ap -> A
```
