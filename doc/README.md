# SEG-Y Ordering Query Plan

The SEG-Y Ordering Query Plan is a simple DSL intended to ease writing queries to order 
and filter large volumes of SEG-Y files in a HPC context. It can be easily translated
to SQL, which is later used in this process.

The language has two basic operations, **ordering** and **filtering**. Both are optional
and can be included in any order in the query. It is also case-insensitive and allows does not require
any specific identation.

## Filtering
The filtering operation is written as such:
```
filter:
    [EXPRESSION] ;
```
where `[EXPRESSION]` should be replaced by a boolean expression. The expression should represent how the SEG-Y data is
filtered, and allows for comparisons between numbers and boolean expressions. It also allows "range" operations,
which denotes if a value is in a certain range
- boolean operators are `and`, `or` and `not`
- comparison operators are `<`, `>`, `<=`, `>=`, `=` and `!=`
- range expression is `[ID] in range([LOW], [HIGH])`, which is equivalent to `[LOW] < [ID] < [HIGH])`, where `[ID]` is 
the name of some data in a SEG-Y file, and `[LOW]` and `[HIGH]` are numerical constants. Both ends of the range can be included
using the `INCL` keyword:
  - `[ID] in range([LOW] INCL, [HIGH])` is equivalent to `[LOW] <= [ID] < [HIGH])`
  - `[ID] in range([LOW], [HIGH] INCL)` is equivalent to `[LOW] < [ID] <= [HIGH])`
  - `[ID] in range([LOW] INCL, [HIGH] INCL)` is equivalent to `[LOW] <= [ID] <= [HIGH])`


## Ordering
The ordering expression is written as such:
```
order:
    [EXPRESSION_LIST] ;
```
Is this case `[EXPRESSION_LIST]` represents a comma-separated list of values that define the order in which the data should be sorted
 i.e. the first value represents the first ordering, the second represents the second ordering, and so forth. Data can be ordered in descending
order using the `DESC` keyword.

## Examples
```
filter: udp > 10 and coord_x = 100;
```
```
order: coord_x;
```
```
filter:
   ( elev in range(10 incl, 100) and
    coord_x = 107.5 ) or
   ( elev in range(100 , 1000 incl) and
    coord_x > 110 ) or
    (not coord_z != 11) ;
    
order a desc, b, c desc ;
```
```
filter: true;
```