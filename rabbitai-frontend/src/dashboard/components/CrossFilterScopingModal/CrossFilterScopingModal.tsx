import { t } from '@superset-ui/core';
import React, { FC } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { StyledModal } from 'src/components/Modal';
import Button from 'src/components/Button';
import { Form } from 'src/common/components';
import { setChartConfiguration } from 'src/dashboard/actions/dashboardInfo';
import { ChartConfiguration } from 'src/dashboard/reducers/types';
import CrossFilterScopingForm from './CrossFilterScopingForm';
import { CrossFilterScopingFormType } from './types';
import { StyledForm } from '../nativeFilters/FiltersConfigModal/FiltersConfigModal';

type CrossFilterScopingModalProps = {
  chartId: number;
  isOpen: boolean;
  onClose: () => void;
};

const CrossFilterScopingModal: FC<CrossFilterScopingModalProps> = ({
  isOpen,
  chartId,
  onClose,
}) => {
  const dispatch = useDispatch();
  const [form] = Form.useForm<CrossFilterScopingFormType>();
  const chartConfig = useSelector<any, ChartConfiguration>(
    ({ dashboardInfo }) => dashboardInfo?.metadata?.chart_configuration,
  );
  const scope = chartConfig?.[chartId]?.crossFilters?.scope;
  const handleSave = () => {
    dispatch(
      setChartConfiguration({
        ...chartConfig,
        [chartId]: {
          id: chartId,
          crossFilters: { scope: form.getFieldValue('scope') },
        },
      }),
    );
    onClose();
  };

  return (
    <StyledModal
      visible={isOpen}
      maskClosable={false}
      title={t('Cross Filter Scoping')}
      width="55%"
      destroyOnClose
      onCancel={onClose}
      onOk={handleSave}
      centered
      data-test="cross-filter-scoping-modal"
      footer={
        <>
          <Button
            key="cancel"
            buttonStyle="secondary"
            data-test="cross-filter-scoping-modal-cancel-button"
            onClick={onClose}
          >
            {t('Cancel')}
          </Button>
          <Button
            key="submit"
            buttonStyle="primary"
            onClick={handleSave}
            data-test="cross-filter-scoping-modal-save-button"
          >
            {t('Save')}
          </Button>
        </>
      }
    >
      <StyledForm preserve={false} form={form} layout="vertical">
        <CrossFilterScopingForm form={form} scope={scope} chartId={chartId} />
      </StyledForm>
    </StyledModal>
  );
};

export default CrossFilterScopingModal;
