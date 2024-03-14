class ExecutionTree:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.is_dead_end = False  # Initialize to False by default

    def add_child(self, child_node):
        self.children.append(child_node)

    def mark_as_dead_end(self):
        self.is_dead_end = True

    def display(self, depth=0, is_info=False):
        prefix = "  " * depth
        connector = "──> " if depth > 0 else ""
        print(f"{prefix}{connector}{self.value} {'(Dead End)' if self.is_dead_end else ''}")

        for i, child in enumerate(self.children):
            if i < len(self.children) - 1:
                child_connector = "│  "
            else:
                child_connector = "   "
            child.display(depth + 1)
            if depth < 1:
                print(f"{prefix}{child_connector}")  # Display child connector under parent node
