import handleHover from './handleHover';
import handleDrop from './handleDrop';

// note: the 'type' hook is not useful for us as dropping is contigent on other properties
const TYPE = 'DRAG_DROPPABLE';

export const dragConfig = [
  TYPE,
  {
    canDrag(props) {
      return !props.disableDragDrop;
    },

    // this defines the dragging item object returned by monitor.getItem()
    beginDrag(props /* , monitor, component */) {
      const { component, index, parentComponent = {} } = props;
      return {
        type: component.type,
        id: component.id,
        meta: component.meta,
        index,
        parentId: parentComponent.id,
        parentType: parentComponent.type,
      };
    },
  },
  function dragStateToProps(connect, monitor) {
    return {
      dragSourceRef: connect.dragSource(),
      dragPreviewRef: connect.dragPreview(),
      isDragging: monitor.isDragging(),
    };
  },
];

export const dropConfig = [
  TYPE,
  {
    canDrop(props) {
      return !props.disableDragDrop;
    },
    hover(props, monitor, component) {
      if (component && component.mounted) {
        handleHover(props, monitor, component);
      }
    },
    // note:
    //  the react-dnd api requires that the drop() method return a result or undefined
    //  monitor.didDrop() cannot be used because it returns true only for the most-nested target
    drop(props, monitor, component) {
      const dropResult = monitor.getDropResult();
      if ((!dropResult || !dropResult.destination) && component.mounted) {
        return handleDrop(props, monitor, component);
      }
      return undefined;
    },
  },
  function dropStateToProps(connect, monitor) {
    return {
      droppableRef: connect.dropTarget(),
      isDraggingOver: monitor.isOver(),
      isDraggingOverShallow: monitor.isOver({ shallow: true }),
    };
  },
];
