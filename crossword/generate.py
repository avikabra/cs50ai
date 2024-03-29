import sys
#from typing_extensions import TypeVar

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        for variable in self.domains:
            to_remove = set()

            for x in self.domains[variable]:
                if len(x) != variable.length:
                    to_remove.add(x)

            for element in to_remove:
                self.domains[variable].remove(element)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if x != y and self.crossword.overlaps[x, y] is not None:
            overlap = self.crossword.overlaps[x, y]
            revisionMade = False

            for first_word in self.domains[x]:
                to_remove = set()

                isWord = False
                xChar = first_word[overlap[0]]

                for second_word in self.domains[y]:
                    yChar = second_word[overlap[1]]
                    if xChar == yChar:
                        isWord = True

                if not isWord:
                    to_remove.add(first_word)
                    revisionMade = True

            for element in to_remove:
                self.domains[x].remove(element)

            return revisionMade

        else:
            return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            init_arcs = []

            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if v1 != v2:
                        if self.crossword.overlaps[v1, v2] is not None:
                            init_arcs.append((v1, v2))

        else:
            init_arcs = arcs

        while len(init_arcs) != 0:
            tup = init_arcs.pop(0)
            x = tup[0]
            y = tup[1]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                
                for z in self.crossword.neighbors(x):
                    if z != y:
                        init_arcs.append((z, x))
        
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                return False
        
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #ENTIRE FUNCTION NOT WORKING???
        
        # distinct
        for v1 in assignment:
            for v2 in assignment:
                if v1 != v2 and assignment[v1] == assignment[v2]:
                    return False
            
        for v1 in assignment:
            if v1.length != len(assignment[v1]):
                return False

        # did not check conflict with neighbors
        for v1 in assignment:
            neigh = self.crossword.neighbors(v1)
            for n in neigh:
                if n in assignment:
                    if self.crossword.overlaps[v1, n] is not None:
                        overlap = self.crossword.overlaps[v1, n]
                        if assignment[v1][overlap[0]] != assignment[n][overlap[1]]:
                            return False
                        else:
                            print(assignment[v1] + " " + assignment[v2] + " " + assignment[v1][overlap[0]])

        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #NOT DONE

        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        vars = set()
        for var in self.domains:
            vars.add(var)
        assSet = set()
        for var in assignment:
            assSet.add(var)
        vars = vars - assSet

        var_rem = {}
        for var in vars:
            var_rem[var] = len(self.domains[var])

        largestVal = sorted(var_rem.values())[len(var_rem)-1]
        for var in var_rem:
            if var_rem[var] != largestVal:
                vars.remove(var)

        if len(vars) > 1:
            var_neigh = {}
            for var in vars:
                var_neigh[var] = len(self.crossword.neighbors(var))

            largestVal = sorted(var_neigh.values())[len(var_neigh)-1]
            for var in var_neigh:
                if var_neigh[var] != largestVal:
                    vars.remove(var)

        for var in vars:
            return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != False:
                    return result
            assignment.pop(var, None)
        return False


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
