Fetch
    1) WAN -> threads (html)
    2) threads (html) -> OP (html)
Parse
    1) OP (html) -> OP (text)
    2) OP (text) -> DATA
        nodeOrd
            types   | ords
            --------------
            root    | 1
            thread  | 2
            header  | 3
            edition | 4
            author  | 5
            title   | 6
            url     | 7

        nodes.json
            "{UID}" : {
                data_line:
                UID:
                value:
                span:
                span2:
                type:
                childuids:
            }

        nodetypes.json

Resolve
Analyze


Glossary
    OP             Original Poster; the first post at the begining of a thread that contains the list of recent stories along 
                   with edition numbers and other relevant links