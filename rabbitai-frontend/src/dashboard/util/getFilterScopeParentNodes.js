
export default function getFilterScopeParentNodes(nodes = [], depthLimit = -1) {
  const parentNodes = [];
  const traverse = (currentNode, depth) => {
    if (!currentNode) {
      return;
    }

    if (currentNode.children && (depthLimit === -1 || depth < depthLimit)) {
      parentNodes.push(currentNode.value);
      currentNode.children.forEach(child => traverse(child, depth + 1));
    }
  };

  if (nodes.length > 0) {
    nodes.forEach(node => {
      traverse(node, 0);
    });
  }

  return parentNodes;
}
