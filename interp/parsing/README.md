# Some notes and links about parsing

## Some compilers

language | lexer | parser | grammar | tokens
---------|-------|--------|---------|--------
[CPython](https://github.com/python/cpython) | [hand-written](https://github.com/python/cpython/blob/master/Parser/tokenizer.c) | [custom parser gen](https://github.com/python/cpython/tree/master/Parser) | [Grammar](https://github.com/python/cpython/blob/master/Grammar/Grammar) | [Tokens](https://github.com/python/cpython/blob/master/Grammar/Tokens)
[GHC](https://github.com/ghc/ghc) | [Alex](https://github.com/ghc/ghc/blob/master/compiler/parser/Lexer.x) | [Happy](https://github.com/ghc/ghc/blob/master/compiler/parser/Parser.y)
Rust | ? | ?

