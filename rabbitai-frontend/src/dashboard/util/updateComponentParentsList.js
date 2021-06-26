
export default function updateComponentParentsList({
  currentComponent,
  layout = {},
}) {
  if (currentComponent && layout[currentComponent.id]) {
    const parentsList = (currentComponent.parents || []).slice();
    parentsList.push(currentComponent.id);

    currentComponent.children.forEach(childId => {
      layout[childId].parents = parentsList; // eslint-disable-line no-param-reassign
      updateComponentParentsList({
        currentComponent: layout[childId],
        layout,
      });
    });
  }
}
