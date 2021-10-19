import React from 'react';
import { shallow } from 'enzyme';
import { Radio } from 'src/components/Radio';
import { AutoComplete, Input } from 'src/common/components';
import { SaveDatasetModal } from 'src/SqlLab/components/SaveDatasetModal';

describe('SaveDatasetModal', () => {
  const mockedProps = {
    visible: false,
    onOk: () => {},
    onHide: () => {},
    handleDatasetNameChange: () => {},
    handleSaveDatasetRadioBtnState: () => {},
    saveDatasetRadioBtnState: 1,
    handleOverwriteCancel: () => {},
    handleOverwriteDataset: () => {},
    handleOverwriteDatasetOption: () => {},
    defaultCreateDatasetValue: 'someDatasets',
    shouldOverwriteDataset: false,
    userDatasetOptions: [],
    disableSaveAndExploreBtn: false,
    handleSaveDatasetModalSearch: () => Promise,
    filterAutocompleteOption: () => false,
    onChangeAutoComplete: () => {},
  };
  it('renders a radio group btn', () => {
    // @ts-ignore
    const wrapper = shallow(<SaveDatasetModal {...mockedProps} />);
    expect(wrapper.find(Radio.Group)).toExist();
  });
  it('renders a autocomplete', () => {
    // @ts-ignore
    const wrapper = shallow(<SaveDatasetModal {...mockedProps} />);
    expect(wrapper.find(AutoComplete)).toExist();
  });
  it('renders an input form', () => {
    // @ts-ignore
    const wrapper = shallow(<SaveDatasetModal {...mockedProps} />);
    expect(wrapper.find(Input)).toExist();
  });
});
