

import React, { FunctionComponent } from 'react';
import { AutoCompleteProps } from 'antd/lib/auto-complete';
import { Radio } from 'src/components/Radio';
import { AutoComplete, Input } from 'src/common/components';
import StyledModal from 'src/components/Modal';
import Button from 'src/components/Button';
import { styled, t } from '@rabbitai-ui/core';
import { RadioChangeEvent } from 'antd/lib/radio';

interface SaveDatasetModalProps {
  visible: boolean;
  onOk: () => void;
  onHide: () => void;
  handleDatasetNameChange: (e: React.FormEvent<HTMLInputElement>) => void;
  handleSaveDatasetModalSearch: (searchText: string) => Promise<void>;
  filterAutocompleteOption: (
    inputValue: string,
    option: { value: string; datasetId: number },
  ) => boolean;
  handleSaveDatasetRadioBtnState: (e: RadioChangeEvent) => void;
  handleOverwriteCancel: () => void;
  handleOverwriteDataset: () => void;
  handleOverwriteDatasetOption: (
    data: string,
    option: Record<string, any>,
  ) => void;
  onChangeAutoComplete: () => void;
  defaultCreateDatasetValue: string;
  disableSaveAndExploreBtn: boolean;
  saveDatasetRadioBtnState: number;
  shouldOverwriteDataset: boolean;
  userDatasetOptions: AutoCompleteProps['options'];
}

const Styles = styled.div`
  .smd-body {
    margin: 0 8px;
  }
  .smd-input {
    margin-left: 45px;
    width: 401px;
  }
  .smd-autocomplete {
    margin-left: 8px;
    width: 401px;
  }
  .smd-radio {
    display: block;
    height: 30px;
    margin: 10px 0px;
    line-height: 30px;
  }
  .smd-overwrite-msg {
    margin: 7px;
  }
`;

// eslint-disable-next-line no-empty-pattern
export const SaveDatasetModal: FunctionComponent<SaveDatasetModalProps> = ({
  visible,
  onOk,
  onHide,
  handleDatasetNameChange,
  handleSaveDatasetRadioBtnState,
  saveDatasetRadioBtnState,
  shouldOverwriteDataset,
  handleOverwriteCancel,
  handleOverwriteDataset,
  handleOverwriteDatasetOption,
  defaultCreateDatasetValue,
  disableSaveAndExploreBtn,
  handleSaveDatasetModalSearch,
  filterAutocompleteOption,
  userDatasetOptions,
  onChangeAutoComplete,
}) => (
  <StyledModal
    show={visible}
    title="Save or Overwrite Dataset"
    onHide={onHide}
    footer={
      <>
        {!shouldOverwriteDataset && (
          <Button
            disabled={disableSaveAndExploreBtn}
            buttonStyle="primary"
            onClick={onOk}
          >
            {t('Save & Explore')}
          </Button>
        )}
        {shouldOverwriteDataset && (
          <>
            <Button onClick={handleOverwriteCancel}>Back</Button>
            <Button
              className="md"
              buttonStyle="primary"
              onClick={handleOverwriteDataset}
              disabled={disableSaveAndExploreBtn}
            >
              {t('Overwrite & Explore')}
            </Button>
          </>
        )}
      </>
    }
  >
    <Styles>
      {!shouldOverwriteDataset && (
        <div className="smd-body">
          <div className="smd-prompt">
            Save this query as a virtual dataset to continue exploring
          </div>
          <Radio.Group
            onChange={handleSaveDatasetRadioBtnState}
            value={saveDatasetRadioBtnState}
          >
            <Radio className="smd-radio" value={1}>
              Save as new
              <Input
                className="smd-input"
                defaultValue={defaultCreateDatasetValue}
                onChange={handleDatasetNameChange}
                disabled={saveDatasetRadioBtnState !== 1}
              />
            </Radio>
            <Radio className="smd-radio" value={2}>
              Overwrite existing
              <AutoComplete
                className="smd-autocomplete"
                options={userDatasetOptions}
                onSelect={handleOverwriteDatasetOption}
                onSearch={handleSaveDatasetModalSearch}
                onChange={onChangeAutoComplete}
                placeholder="Select or type dataset name"
                filterOption={filterAutocompleteOption}
                disabled={saveDatasetRadioBtnState !== 2}
              />
            </Radio>
          </Radio.Group>
        </div>
      )}
      {shouldOverwriteDataset && (
        <div className="smd-overwrite-msg">
          Are you sure you want to overwrite this dataset?
        </div>
      )}
    </Styles>
  </StyledModal>
);
