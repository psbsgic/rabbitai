import { NEW_COMPONENTS_SOURCE_ID } from './constants';
import findParentId from './findParentId';
import getDetailedComponentWidth from './getDetailedComponentWidth';
import newComponentFactory from './newComponentFactory';

export default function getComponentWidthFromDrop({
  dropResult,
  layout: components,
}) {
  const { source, destination, dragging } = dropResult;

  const isNewComponent = source.id === NEW_COMPONENTS_SOURCE_ID;
  const component = isNewComponent
    ? newComponentFactory(dragging.type)
    : components[dragging.id] || {};

  // moving a component within the same container shouldn't change its width
  if (source.id === destination.id) {
    return component.meta.width;
  }

  const {
    width: draggingWidth,
    minimumWidth: minDraggingWidth,
  } = getDetailedComponentWidth({
    component,
    components,
  });

  const {
    width: destinationWidth,
    occupiedWidth: draggingOccupiedWidth,
  } = getDetailedComponentWidth({
    id: destination.id,
    components,
  });

  let destinationCapacity = Number(destinationWidth - draggingOccupiedWidth);

  if (Number.isNaN(destinationCapacity)) {
    const {
      width: grandparentWidth,
      occupiedWidth: grandparentOccupiedWidth,
    } = getDetailedComponentWidth({
      id: findParentId({
        childId: destination.id,
        layout: components,
      }),
      components,
    });

    destinationCapacity = Number(grandparentWidth - grandparentOccupiedWidth);
  }

  if (
    Number.isNaN(destinationCapacity) ||
    Number.isNaN(Number(draggingWidth))
  ) {
    return draggingWidth;
  }
  if (destinationCapacity >= draggingWidth) {
    return draggingWidth;
  }
  if (destinationCapacity >= minDraggingWidth) {
    return destinationCapacity;
  }

  return -1;
}
