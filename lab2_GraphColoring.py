def read_graph_from_file(file_path):
    """Reads the graph and the number of colors from the file, handling comments and empty lines."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    colors = 0
    edges = []
    for line in lines:
        line = line.strip()
        if line.startswith('#') or not line:
            # Skip comments and empty lines
            continue
        if line.lower().startswith('colors'):
            colors = int(line.split('=')[1].strip())
            continue
        parts = line.split(',')
        if len(parts) == 2:
            try:
                edge = tuple(map(int, parts))
                edges.append(edge)
            except ValueError:
                # Handle lines that do not correctly represent edges
                continue

    # Generate vertices from edges
    vertices = list(set([v for edge in edges for v in edge]))
    return colors, vertices, edges

def AC3(csp):
    """Applies AC3 algorithm for constraint propagation."""
    queue = [(vi, vj) for vi in csp.variables for vj in csp.constraints[vi]]
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.constraints[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    """Revises the domain of xi."""
    revised = False
    for x in csp.domains[xi][:]:
        if not any(x != y for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True
    return revised

class CSP:
    def __init__(self, vertices, edges, num_colors):
        self.variables = vertices
        self.domains = {v: list(range(num_colors)) for v in vertices}
        self.constraints = {v: [] for v in vertices}
        for (v1, v2) in edges:
            self.constraints[v1].append(v2)
            self.constraints[v2].append(v1)

    def is_consistent(self, var, assignment):
        """Checks if current assignment is consistent."""
        for neighbor in self.constraints[var]:
            if neighbor in assignment and assignment[neighbor] == assignment[var]:
                return False
        return True

    def select_unassigned_variable(self, assignment):
        """Selects the unassigned variable using MRV heuristic."""
        unassigned_vars = [v for v in self.variables if v not in assignment]
        _, var = min((len(self.domains[v]), v) for v in unassigned_vars)
        return var

    def order_domain_values(self, var, assignment):
        """Orders domain values using LCV heuristic (not implemented for simplicity)."""
        return self.domains[var]

    def backtrack(self, assignment={}):
        """Backtracks to find a solution."""
        if len(assignment) == len(self.variables):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.is_consistent(var, new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None

    def solve(self):
        """Solves the CSP."""
        return self.backtrack()

# Main execution
if __name__ == "__main__":
    file_path = "F:\CSCI 6511\P2\gc_1378296846561000.txt"  # Adjust the path to your file
    num_colors, vertices, edges = read_graph_from_file(file_path)
    csp = CSP(vertices, edges, num_colors)
    AC3(csp)
    solution = csp.solve()
    print("Color assignment:", solution)
