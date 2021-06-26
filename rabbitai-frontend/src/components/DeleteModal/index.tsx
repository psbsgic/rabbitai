
import { t, styled } from '@rabbitai-ui/core';
import React, { useState } from 'react';
import { Input } from 'src/common/components';
import Modal from 'src/components/Modal';
import { FormLabel } from 'src/components/Form';

const StyledDiv = styled.div`
  padding-top: 8px;
  width: 50%;
  label {
    color: ${({ theme }) => theme.colors.grayscale.light1};
    text-transform: uppercase;
  }
`;

const DescriptionContainer = styled.div`
  line-height: 40px;
  padding-top: 16px;
`;

interface DeleteModalProps {
  description: React.ReactNode;
  onConfirm: () => void;
  onHide: () => void;
  open: boolean;
  title: React.ReactNode;
}

export default function DeleteModal({
  description,
  onConfirm,
  onHide,
  open,
  title,
}: DeleteModalProps) {
  const [disableChange, setDisableChange] = useState(true);

  return (
    <Modal
      disablePrimaryButton={disableChange}
      onHide={onHide}
      onHandledPrimaryAction={onConfirm}
      primaryButtonName={t('delete')}
      primaryButtonType="danger"
      show={open}
      title={title}
    >
      <DescriptionContainer>{description}</DescriptionContainer>
      <StyledDiv>
        <FormLabel htmlFor="delete">
          {t('Type "%s" to confirm', t('DELETE'))}
        </FormLabel>
        <Input
          data-test="delete-modal-input"
          type="text"
          id="delete"
          autoComplete="off"
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            const targetValue = event.target.value ?? '';
            setDisableChange(targetValue.toUpperCase() !== t('DELETE'));
          }}
        />
      </StyledDiv>
    </Modal>
  );
}
