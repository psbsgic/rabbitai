import React from 'react';
import thunk from 'redux-thunk';
import configureStore from 'redux-mock-store';
import { Provider } from 'react-redux';
import fetchMock from 'fetch-mock';
import AnnotationModal from 'src/views/CRUD/annotation/AnnotationModal';
import Modal from 'src/components/Modal';
import waitForComponentToPaint from 'spec/helpers/waitForComponentToPaint';
import { JsonEditor } from 'src/components/AsyncAceEditor';
import { styledMount as mount } from 'spec/helpers/theming';

const mockData = {
  id: 1,
  short_descr: 'annotation 1',
  start_dttm: '2019-07-01T10:25:00',
  end_dttm: '2019-06-11T10:25:00',
};

const FETCH_ANNOTATION_ENDPOINT =
  'glob:*/api/v1/annotation_layer/*/annotation/*';
const ANNOTATION_PAYLOAD = { result: mockData };

fetchMock.get(FETCH_ANNOTATION_ENDPOINT, ANNOTATION_PAYLOAD);

const mockStore = configureStore([thunk]);
const store = mockStore({});

const mockedProps = {
  addDangerToast: () => {},
  addSuccessToast: () => {},
  annotation: mockData,
  onAnnotationAdd: jest.fn(() => []),
  onHide: () => {},
  show: true,
};

async function mountAndWait(props = mockedProps) {
  const mounted = mount(
    <Provider store={store}>
      <AnnotationModal show {...props} />
    </Provider>,
  );
  await waitForComponentToPaint(mounted);
  return mounted;
}

describe('AnnotationModal', () => {
  let wrapper;

  beforeAll(async () => {
    wrapper = await mountAndWait();
  });

  it('renders', () => {
    expect(wrapper.find(AnnotationModal)).toExist();
  });

  it('renders a Modal', () => {
    expect(wrapper.find(Modal)).toExist();
  });

  it('renders add header when no annotation prop is included', async () => {
    const addWrapper = await mountAndWait({});
    expect(
      addWrapper.find('[data-test="annotaion-modal-title"]').text(),
    ).toEqual('Add annotation');
  });

  it('renders edit header when annotation prop is included', () => {
    expect(wrapper.find('[data-test="annotaion-modal-title"]').text()).toEqual(
      'Edit annotation',
    );
  });

  it('renders input elements for annotation name', () => {
    expect(wrapper.find('input[name="short_descr"]')).toExist();
  });

  it('renders json editor for json metadata', () => {
    expect(wrapper.find(JsonEditor)).toExist();
  });
});
