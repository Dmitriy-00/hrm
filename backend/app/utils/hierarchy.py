"""Utilities for working with hierarchical structures."""

from typing import Optional, List
from sqlalchemy.orm import Session


def build_path(name: str, parent_path: Optional[str] = None) -> str:
    """
    Build materialized path for hierarchical structure.

    Args:
        name: Name of the current node
        parent_path: Path of the parent node

    Returns:
        Full path (e.g., "developer.backend.python")
    """
    if parent_path:
        return f"{parent_path}.{name.lower().replace(' ', '_')}"
    return name.lower().replace(' ', '_')


def calculate_level(path: str) -> int:
    """
    Calculate level (depth) based on path.

    Args:
        path: Materialized path

    Returns:
        Level (0 for root, 1 for first level, etc.)
    """
    return path.count('.')


def get_all_children_paths(path: str) -> List[str]:
    """
    Generate patterns to find all children of a node.

    Args:
        path: Parent path

    Returns:
        List of path patterns for children
    """
    return [f"{path}.%"]


def build_tree(items: List, id_field: str = 'id', parent_field: str = 'parent_id') -> List:
    """
    Build tree structure from flat list of items.

    Args:
        items: List of items
        id_field: Name of the ID field
        parent_field: Name of the parent ID field

    Returns:
        Tree structure with 'children' field
    """
    # Create lookup dict
    lookup = {getattr(item, id_field): item for item in items}

    # Build tree
    tree = []
    for item in items:
        parent_id = getattr(item, parent_field)
        if parent_id is None:
            tree.append(item)
        else:
            parent = lookup.get(parent_id)
            if parent:
                if not hasattr(parent, 'children'):
                    parent.children = []
                parent.children.append(item)

    return tree
