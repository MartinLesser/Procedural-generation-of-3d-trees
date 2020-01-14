# Procedural generation of 3d trees
Code of my bachelor thesis with the title "procedural generation of 3d trees" from 2017. It uses
context free grammars to generate strings via L-System. A string consists of characters
that describe the skeleton of a 3d tree. The characters in a string are like instruction
for turtle graphics (instructions for drawing a skeleton tree). On that basis the 
vertices will be calculated for every tree segment (trunk and branches), then the vertices
of a circle around each segment vertex will be calculated in order to give the skeleton 
tree volume and create an actual tree. All the vertices will be given in the right order 
(to form triangles) to the opengl engine. Texture coordinates will also be transmitted.
PyGame renders the 3d tree finally.

The rules for the L-system can be found in ([grammar files](src/resources/grammars/3d)). 

Author: Martin Lesser

![picture of generated tree with different gernations and variations](https://github.com/MartinLesser/Procedural-generation-of-3d-trees/blob/master/doc/GeneratedSameTreeWithRandomVarationsAndIterations.png "Generated tree")

## Dependencies
pygame  
python3-opengl

## How to use
Unfortunately the main file was lost. I don't know how that could happen. But I might find
it again. If you are interested in executing this project, you can send me an email and I
can look for it.

You can define custom grammars ([grammar files](src/resources/grammars/3d)).  A grammar file
has the following structure:

```
axiom: mnop (start symbols. these will be replaced systematically by the rules)
angle_z: 10 - 25 (possible angle range along the z axis)
angle_y: 10 - 25 (possible angle range along the y axis)
angle_x: 10 - 25 (possible angle range along the x axis)

rules: m -> [+(><)X], n -> [+<180(><)X], o -> [+<90(><)X], o -> x, p -> [+<270(><)X], p -> x, X -> @[rFX@2.0B]rFX@2.0B
(Multiple rules separated by comma. See grammar rules section below.)

branch-shortening: 0.5 - 0.7 (The creation of branches is hierachical. On one branch 
further smaller branches can be created (depending on the rules). 
This variable states the range by how much
the new branches will be smaller.)
generations: 3 (The replacement of symbols could be done an infinite number of times
(depending on the rules). This variable states after how many replacement loops will be
made before the replacement will be stopped.)

base_length: 4 (this value is the beginning trunk length. all following branches will be
smaller)
base_radius: 0.06 (beginning radius of the trunk. all following branches will be thinner.)
bark_texture: ../resources/bark_seamless.jpg (texture path for the bark texture)
leaf_texture: ../resources/bush.png (path to the leaf texture)
```

### Grammar rules
One rule (e.g. x -> y) states how a symbol can be replaced (x can be replaced by y). The replacements
 of all symbols in a string is one generation. The replacement can be repeated. The resulting string
 contains symbols that can be interpreted as a 3d turtle graphic. Each symbol is an instruction for
 the 3d turtle.  
 
The `F` symbol moves the turtle forward. How far depends on the `base_length`. The branches can be
shortened or elongated with the `@` symbol. A float value has to follow this symbol. The values states
how much the next branch will be longer/shorter. This creates a base length for this branch and when
the next branch contains a `@` symbol the shortening or elongating depends on the parent branch length.
 
Rotations along x, y and z-axis are possible (clockwise or counter clockwise). Symbols for x-rotations: < and >. 
Symbols for y-rotations: + and -. Symbols for z-rotations: ? and !. Random rotations can be done with
`r` which generates one of the rotation-symbols (+-<>?!). The degrees of a rotation can either be 
stated in the rule e.g. `x -> +35F` (rotate 35° around the y axis clockwise) or can be generated e.g.
`x -> +F` could be replaced to `x -> +17F` (the generated degree number depends on the given 
`angle_y` range). 

To draw a branch and draw another branch afterwards. You have to make jumps (or else a branch connects the two
locations. For jumping the brackets ```[]``` are used.  

Expressions within parantheses are choices.
E.g. (+-) means rotate right or left. Which symbol will be taken is determined by chance.

`B` will be replaced as L which generate a leaf.

# Further information
If you want more information how the system works you could read my bachelor thesis (see [doc directory](doc/))
which is written in german. If you can't understand german you can write me an email and I can expand
the readme.