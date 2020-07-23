from typing import Dict, TypeVar
from hypothesis import given, infer

from kvs.rbtree import RBTree, inorder_traversal

A = TypeVar("A")

def from_dict(kv_dict: Dict[str, A]) -> RBTree[A]:
    rb_tree: RBTree[A] = RBTree()
    for key, value in kv_dict.items():
        rb_tree.insert(key, value)
    return rb_tree

def to_dict(rb_tree: RBTree[A]) -> Dict[str, A]:
    return dict((key, value) for (key, value) in inorder_traversal(rb_tree))


@given(kv_pairs=infer)
def test_from_dict_always_returns_sorted_tree(kv_pairs: Dict[str, int]):
    tree = from_dict(kv_pairs)
    assert list(key for (key, _) in inorder_traversal(tree)) == sorted(kv_pairs.keys())

@given(kv_pairs=infer)
def test_isomorphism_exists_with_dict(kv_pairs: Dict[str, int]):
    assert to_dict(from_dict(kv_pairs)) == kv_pairs
