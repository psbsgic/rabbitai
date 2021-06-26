
import React from 'react';
import { Provider } from 'react-redux';
import { styledMount as mount } from 'spec/helpers/theming';
import sinon from 'sinon';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

import DeleteComponentButton from 'src/dashboard/components/DeleteComponentButton';
import EditableTitle from 'src/components/EditableTitle';
import HoverMenu from 'src/dashboard/components/menu/HoverMenu';
import WithPopoverMenu from 'src/dashboard/components/menu/WithPopoverMenu';
import DragDroppable from 'src/dashboard/components/dnd/DragDroppable';
import Header from 'src/dashboard/components/gridComponents/Header';
import newComponentFactory from 'src/dashboard/util/newComponentFactory';
import {
  HEADER_TYPE,
  DASHBOARD_GRID_TYPE,
} from 'src/dashboard/util/componentTypes';

import { mockStoreWithTabs } from 'spec/fixtures/mockStore';

describe('Header', () => {
  const props = {
    id: 'id',
    parentId: 'parentId',
    component: newComponentFactory(HEADER_TYPE),
    depth: 1,
    parentComponent: newComponentFactory(DASHBOARD_GRID_TYPE),
    index: 0,
    editMode: false,
    filters: {},
    handleComponentDrop() {},
    deleteComponent() {},
    updateComponents() {},
  };

  function setup(overrideProps) {
    // We have to wrap provide DragDropContext for the underlying DragDroppable
    // otherwise we cannot assert on DragDroppable children
    const wrapper = mount(
      <Provider store={mockStoreWithTabs}>
        <DndProvider backend={HTML5Backend}>
          <Header {...props} {...overrideProps} />
        </DndProvider>
      </Provider>,
    );
    return wrapper;
  }

  it('should render a DragDroppable', () => {
    const wrapper = setup();
    expect(wrapper.find(DragDroppable)).toExist();
  });

  it('should render a WithPopoverMenu', () => {
    const wrapper = setup();
    expect(wrapper.find(WithPopoverMenu)).toExist();
  });

  it('should render a HoverMenu in editMode', () => {
    let wrapper = setup();
    expect(wrapper.find(HoverMenu)).not.toExist();

    // we cannot set props on the Header because of the WithDragDropContext wrapper
    wrapper = setup({ editMode: true });
    expect(wrapper.find(HoverMenu)).toExist();
  });

  it('should render an EditableTitle with meta.text', () => {
    const wrapper = setup();
    expect(wrapper.find(EditableTitle)).toExist();
    expect(wrapper.find('.editable-title')).toHaveText(
      props.component.meta.text,
    );
  });

  it('should call updateComponents when EditableTitle changes', () => {
    const updateComponents = sinon.spy();
    const wrapper = setup({ editMode: true, updateComponents });
    wrapper.find(EditableTitle).prop('onSaveTitle')('New title');

    const headerId = props.component.id;
    expect(updateComponents.callCount).toBe(1);
    expect(updateComponents.getCall(0).args[0][headerId].meta.text).toBe(
      'New title',
    );
  });

  it('should render a DeleteComponentButton when focused in editMode', () => {
    const wrapper = setup({ editMode: true });
    wrapper.find(WithPopoverMenu).simulate('click'); // focus

    expect(wrapper.find(DeleteComponentButton)).toExist();
  });

  it('should call deleteComponent when deleted', () => {
    const deleteComponent = sinon.spy();
    const wrapper = setup({ editMode: true, deleteComponent });
    wrapper.find(WithPopoverMenu).simulate('click'); // focus
    wrapper.find(DeleteComponentButton).simulate('click');

    expect(deleteComponent.callCount).toBe(1);
  });
});
