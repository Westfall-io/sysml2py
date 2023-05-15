start: package 
    | type name dict2
    | definition name dict2


package: "package" name dict2

// Allow optional punctuation after each word
type: WORD
definition: type "def"
name: WORD
pointer: WORD

dict2: "{" [pair+ | doc | "@" word dict2] "}"

word: WORD ["," | "!" | "." | ":"]
variable: (word ["_"])*

iname3: "::" word
iname2: "::" word [iname3]
iname: word ("::" word)*

LCASE_LETTER: "a".."z" | "*"
UCASE_LETTER: "A".."Z"

LETTER: UCASE_LETTER | LCASE_LETTER
WORD: LETTER+

import: "import" iname ";"
str2: ESCAPED_STRING
keyv: word "=" str2 ";"
    | input
    | output
    
input: "in" variable ":" word dict2
output: "out" variable ":" word dict2

pair: type name ":" pointer ";"
    | type dict2
    | import
    | type name dict2
    | definition name dict2
    | keyv
    
doc: "doc" "/*" [word* ("*" word*)*] "*/"

// imports WORD from library
%import common.ESCAPED_STRING
//%import common.WORD
//%import common.LETTER
%import common.WS
%import lark.STRING
%ignore WS

// Disregard spaces in text
%ignore " "  