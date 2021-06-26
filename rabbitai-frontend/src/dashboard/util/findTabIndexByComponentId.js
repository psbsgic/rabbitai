
export default function findTabIndexByComponentId({
  currentComponent,
  directPathToChild = [],
}) {
  if (
    !currentComponent ||
    directPathToChild.length === 0 ||
    directPathToChild.indexOf(currentComponent.id) === -1
  ) {
    return -1;
  }

  const currentComponentIdx = directPathToChild.findIndex(
    id => id === currentComponent.id,
  );
  const nextParentId = directPathToChild[currentComponentIdx + 1];
  if (currentComponent.children.indexOf(nextParentId) >= 0) {
    return currentComponent.children.findIndex(
      childId => childId === nextParentId,
    );
  }
  return -1;
}
