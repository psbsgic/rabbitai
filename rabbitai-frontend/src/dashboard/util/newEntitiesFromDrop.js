import componentIsResizable from './componentIsResizable';
import shouldWrapChildInRow from './shouldWrapChildInRow';
import newComponentFactory from './newComponentFactory';
import getComponentWidthFromDrop from './getComponentWidthFromDrop';

import { ROW_TYPE, TABS_TYPE, TAB_TYPE } from './componentTypes';

export default function newEntitiesFromDrop({ dropResult, layout }) {
  const { dragging, destination } = dropResult;

  const dragType = dragging.type;
  const dropEntity = layout[destination.id];
  const dropType = dropEntity.type;
  let newDropChild = newComponentFactory(dragType, dragging.meta);
  newDropChild.parents = (dropEntity.parents || []).concat(dropEntity.id);

  if (componentIsResizable(dragging)) {
    newDropChild.meta.width = // don't set a 0 width
      getComponentWidthFromDrop({ dropResult, layout }) || undefined;
  }

  const wrapChildInRow = shouldWrapChildInRow({
    parentType: dropType,
    childType: dragType,
  });

  const newEntities = {
    [newDropChild.id]: newDropChild,
  };

  if (wrapChildInRow) {
    const rowWrapper = newComponentFactory(ROW_TYPE);
    rowWrapper.children = [newDropChild.id];
    rowWrapper.parents = (dropEntity.parents || []).concat(dropEntity.id);
    newEntities[rowWrapper.id] = rowWrapper;
    newDropChild = rowWrapper;
    newDropChild.parents = rowWrapper.parents.concat(rowWrapper.id);
  } else if (dragType === TABS_TYPE) {
    // create a new tab component
    const tabChild = newComponentFactory(TAB_TYPE);
    tabChild.parents = (dropEntity.parents || []).concat(dropEntity.id);
    newDropChild.children = [tabChild.id];
    newEntities[tabChild.id] = tabChild;
  }

  const nextDropChildren = [...dropEntity.children];
  nextDropChildren.splice(destination.index, 0, newDropChild.id);

  newEntities[destination.id] = {
    ...dropEntity,
    children: nextDropChildren,
  };

  return newEntities;
}
