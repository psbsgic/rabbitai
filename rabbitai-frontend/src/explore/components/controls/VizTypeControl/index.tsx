import React, { useCallback, useState } from 'react';
import PropTypes from 'prop-types';
import { t, getChartMetadataRegistry, styled } from '@superset-ui/core';
import { usePluginContext } from 'src/components/DynamicPlugins';
import Modal from 'src/components/Modal';
import { Tooltip } from 'src/components/Tooltip';
import Label, { Type } from 'src/components/Label';
import ControlHeader from 'src/explore/components/ControlHeader';
import VizTypeGallery, {
  MAX_ADVISABLE_VIZ_GALLERY_WIDTH,
} from './VizTypeGallery';

const propTypes = {
  description: PropTypes.string,
  label: PropTypes.string,
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func,
  value: PropTypes.string.isRequired,
  labelType: PropTypes.string,
};

interface VizTypeControlProps {
  description?: string;
  label?: string;
  name: string;
  onChange: (vizType: string | null) => void;
  value: string | null;
  labelType?: Type;
  isModalOpenInit?: boolean;
}

const defaultProps = {
  onChange: () => {},
  labelType: 'default',
};

const metadataRegistry = getChartMetadataRegistry();

export const VIZ_TYPE_CONTROL_TEST_ID = 'viz-type-control';

function VizSupportValidation({ vizType }: { vizType: string }) {
  const state = usePluginContext();
  if (state.loading || metadataRegistry.has(vizType)) {
    return null;
  }
  return (
    <div className="text-danger">
      <i className="fa fa-exclamation-circle text-danger" />{' '}
      <small>{t('This visualization type is not supported.')}</small>
    </div>
  );
}

const UnpaddedModal = styled(Modal)`
  .ant-modal-body {
    padding: 0;
  }
`;

/** Manages the viz type and the viz picker modal */
const VizTypeControl = (props: VizTypeControlProps) => {
  const { value: initialValue, onChange, isModalOpenInit, labelType } = props;
  const { mountedPluginMetadata } = usePluginContext();
  const [showModal, setShowModal] = useState(!!isModalOpenInit);
  // a trick to force re-initialization of the gallery each time the modal opens,
  // ensuring that the modal always opens to the correct category.
  const [modalKey, setModalKey] = useState(0);
  const [selectedViz, setSelectedViz] = useState<string | null>(initialValue);

  const openModal = useCallback(() => {
    setShowModal(true);
  }, []);

  const onSubmit = useCallback(() => {
    onChange(selectedViz);
    setShowModal(false);
  }, [selectedViz, onChange]);

  const onCancel = useCallback(() => {
    setShowModal(false);
    setModalKey(key => key + 1);
    // make sure the modal re-opens to the last submitted viz
    setSelectedViz(initialValue);
  }, [initialValue]);

  const labelContent = initialValue
    ? mountedPluginMetadata[initialValue]?.name || `${initialValue}`
    : t('Select Viz Type');

  return (
    <div>
      <ControlHeader {...props} />
      <Tooltip
        id="error-tooltip"
        placement="right"
        title={t('Click to change visualization type')}
      >
        <>
          <Label
            onClick={openModal}
            type={labelType}
            data-test="visualization-type"
          >
            {labelContent}
          </Label>
          {initialValue && <VizSupportValidation vizType={initialValue} />}
        </>
      </Tooltip>

      <UnpaddedModal
        show={showModal}
        onHide={onCancel}
        title={t('Select a visualization type')}
        primaryButtonName={t('Select')}
        disablePrimaryButton={!selectedViz}
        onHandledPrimaryAction={onSubmit}
        maxWidth={`${MAX_ADVISABLE_VIZ_GALLERY_WIDTH}px`}
        responsive
      >
        {/* When the key increments, it forces react to re-init the gallery component */}
        <VizTypeGallery
          key={modalKey}
          selectedViz={selectedViz}
          onChange={setSelectedViz}
        />
      </UnpaddedModal>
    </div>
  );
};

VizTypeControl.propTypes = propTypes;
VizTypeControl.defaultProps = defaultProps;

export default VizTypeControl;
