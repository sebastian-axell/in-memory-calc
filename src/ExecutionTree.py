class ExecutionTree:
    def __init__(self, value, info=False):
        self.value = value
        self.info = info
        self.children = []
        self.is_dead_end = False  # Initialize to False by default

    def delete_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
        else:
            print("Child node not found.")
    def add_child(self, child_node):
        self.children.append(child_node)
    def add_parent_info(self, child, info):
        self.children[self.children.index(child)-1].info=info
        self.info=True

    def add_info(self, info):
        self.info=True
        self.children[-1].info=info

    def mark_as_dead_end(self):
        self.is_dead_end = True

    def display(self, depth=0, is_info=False):
        prefix = "  " * depth
        connector = "──> " if depth > 0 else ""
        print(f"{prefix}{connector}{self.value} {'(Dead End)' if self.is_dead_end else ''}")

        # Print info line if available
        if self.info and depth > 0:
            print(f"{prefix}   Note: {self.info}")

        for i, child in enumerate(self.children):
            if i < len(self.children) - 1:
                child_connector = "│  "
            else:
                child_connector = "   "
            child.display(depth + 1)
            if depth < 1:
                print(f"{prefix}{child_connector}")  # Display child connector under parent node
