import React from 'react';
import { act } from 'react-dom/test-utils';
import thunk from 'redux-thunk';
import configureStore from 'redux-mock-store';
import { styledMount as mount } from 'spec/helpers/theming';
import { ReactWrapper } from 'enzyme';
import { Upload } from 'src/common/components';
import Button from 'src/components/Button';
import { ImportResourceName } from 'src/views/CRUD/types';
import ImportModelsModal from 'src/components/ImportModal';
import Modal from 'src/components/Modal';

const mockStore = configureStore([thunk]);
const store = mockStore({});

const requiredProps = {
  resourceName: 'database' as ImportResourceName,
  resourceLabel: 'database',
  passwordsNeededMessage: 'Passwords are needed',
  confirmOverwriteMessage: 'Database exists',
  addDangerToast: () => {},
  addSuccessToast: () => {},
  onModelImport: () => {},
  show: true,
  onHide: () => {},
};

describe('ImportModelsModal', () => {
  let wrapper: ReactWrapper;

  beforeEach(() => {
    wrapper = mount(<ImportModelsModal {...requiredProps} />, {
      context: { store },
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders', () => {
    expect(wrapper.find(ImportModelsModal)).toExist();
  });

  it('renders a Modal', () => {
    expect(wrapper.find(Modal)).toExist();
  });

  it('renders "Import database" header', () => {
    expect(wrapper.find('h4').text()).toEqual('Import database');
  });

  it('renders a file input field', () => {
    expect(wrapper.find('input[type="file"]')).toExist();
  });

  it('should render the close, file, import and cancel buttons', () => {
    expect(wrapper.find('button')).toHaveLength(4);
  });

  it('should render the import button initially disabled', () => {
    expect(wrapper.find(Button).at(2).prop('disabled')).toBe(true);
  });

  it('should render the import button enabled when a file is selected', () => {
    const file = new File([new ArrayBuffer(1)], 'model_export.zip');
    act(() => {
      const handler = wrapper.find(Upload).prop('onChange');
      if (handler) {
        handler({
          fileList: [],
          file: {
            name: 'model_export.zip',
            originFileObj: file,
            uid: '-1',
            size: 0,
            type: 'zip',
          },
        });
      }
    });
    wrapper.update();
    expect(wrapper.find(Button).at(2).prop('disabled')).toBe(false);
  });

  it('should render password fields when needed for import', () => {
    const wrapperWithPasswords = mount(
      <ImportModelsModal
        {...requiredProps}
        passwordFields={['databases/examples.yaml']}
      />,
      {
        context: { store },
      },
    );
    expect(wrapperWithPasswords.find('input[type="password"]')).toExist();
  });
});
