This is the program to evaluate the physicochemical properties from the AAindex database for any
non-canonical amino acid from its OpenEye's SMILES encoding.
(C) Yuri V. Milchevskiy, Yuri V. Kravatsky under the terms of the Creative Commons CC BY-NC-SA 4.0 license
email: milch@eimb.ru

1. Compile the program by running make.sh

2. SMILES code should be surrounded by brackets, e.g.

./predictNC "O[C@H]1CN[C@@H](C1)C(O)=O"

Output:

Property        Value
.........................
VINM940104      0.809604
WARP780101      6.84314
.........................

Quality of prediction of the each quality, RMSE, number of predictors and threshold F-value can be
found in the complete database.

If SMILES contains components that cannot be predicted (e.g., (Au)), the appropriate error message
is generated:

./predictNC "O[C@H]1CN[C@@H](C1)C(O)=O[Au]"
Can't calculate properties. incorrect SMILES component: [Au]

Right now due to the lack of the source data for the learning models, this method cannot predict
physicochemical properties of amino acids if they include elements such as As, B, Br, Cl, F, I, P, Se
