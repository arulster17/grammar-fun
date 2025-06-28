# grammar-fun

Some functionalities provided:

- Determine if grammar is LL(1).
- Convert non-LL(1) grammar to LL(1) (if possible).

Notes:

- Please use the symbol `<>` to represent the empty string (ε)
- Reserved names: eof, <>
- Do not use the character ^ in any terminals/nonterminals (used for left factoring)

Input Grammar File Format

```
Comments
>>>
Comma separated Ts (does not include EOF)
>>>
Comma separated NTs. The first NT will be considered the start symbol.
>>>
Line separated Prod Rules in form NT -> <> U (T U NT)^+ (do not include file -> root EOF)
```

Example Grammar that matches regex `R = a+`

```
This grammar matches regex R = a+. Terminal A represents 'a'.
>>>
A
>>>
ap
>>>
ap -> A ap
ap -> A
```
