import React, { useRef, useState } from 'react';
import { styled } from '@superset-ui/core';
import { isFeatureEnabled, FeatureFlag } from 'src/featureFlags';
import Modal from 'src/components/Modal';
import { useComponentDidMount } from 'src/common/hooks/useComponentDidMount';
import { Omnibar } from './Omnibar';
import { LOG_ACTIONS_OMNIBAR_TRIGGERED } from '../../logger/LogUtils';
import { getDashboards } from './getDashboards';

const OmniModal = styled(Modal)`
  margin-top: 20%;

  .ant-modal-body {
    padding: 0;
  }
`;

interface Props {
  logEvent: (log: string, object: object) => void;
}

export default function OmniContainer({ logEvent }: Props) {
  const showOmni = useRef<boolean>();
  const [showModal, setShowModal] = useState(false);

  useComponentDidMount(() => {
    showOmni.current = false;
    function handleKeydown(event: KeyboardEvent) {
      if (!isFeatureEnabled(FeatureFlag.OMNIBAR)) return;
      const controlOrCommand = event.ctrlKey || event.metaKey;
      const isOk = ['KeyK', 'KeyS'].includes(event.code); // valid keys "s" or "k"
      if (controlOrCommand && isOk) {
        logEvent(LOG_ACTIONS_OMNIBAR_TRIGGERED, {
          show_omni: !!showOmni.current,
        });
        showOmni.current = !showOmni.current;
        setShowModal(showOmni.current);
        if (showOmni.current) {
          document.getElementById('InputOmnibar')?.focus();
        }
      }
    }

    document.addEventListener('keydown', handleKeydown);
    return () => document.removeEventListener('keydown', handleKeydown);
  });

  return (
    <OmniModal
      title=""
      show={showModal}
      hideFooter
      closable={false}
      onHide={() => {}}
    >
      <Omnibar
        id="InputOmnibar"
        placeholder="Search all dashboards"
        extensions={[getDashboards]}
      />
    </OmniModal>
  );
}
