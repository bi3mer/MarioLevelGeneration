# Maps

Turns out that parsing png images isn't the easiest thing ever to get perfeCt. So, the [parser](../map_generator/generate_map_from_png) will read files from the [cleaned_maps](./cleaned_maps) directory and write `.map` files, which are just files where one character represents a tile. Each file generated is wildly different from the next, so I added an extra directory which takes the converted files and I hand edit them. This mainly consists of replacing all in each file for certain values. For example, on [1-1](./map/1-1.map) I'll replace `2` with `:` which is the symbol for empty space. Below, there is a table for these mappings.

| Char | Block Type              |
|------|-------------------------|
| :    | air                     |
| |    | ground                  |
| =    | square block            |
| g    | goomba                  |
| ?    | quesiton mark block     |
| #    | destructable block      |
| m    | big mushroom            | 
| p    | pipe                    |
| s    | star                    |
| k    | koopa troopa            |
| K    | red flying koopa troopa |
| h    | hammer bro              |
| L    | lakitu                  |
| f    | flag                    |
| c    | coin                    |
| f    | small castle (fort)     |
| B    | big castle              |
| P    | platform bottom         |
| T    | platform top            |
| F    | flying platform         |
| e    | plant enemy             |
| S    | spring                  |
| b    | buzzy beatle            |
| C    | Cheep Cheep             |
| w    | weird plaftform 2-3     |
| R    | red coin                |
| r    | red shell               |
| z    | single cannon           |
| Z    | double cannon           |


# Removed

I removed keys from the maps as well as buzzy beatles. But I intend to add buzzy beatles back into the cleaned map files by hand.