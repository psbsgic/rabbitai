
import React, { useState } from 'react';
import { Row, Col, Input, TextArea } from 'src/common/components';
import { t, rabbitaiTheme, styled } from '@rabbitai-ui/core';
import Button from 'src/components/Button';
import { Form, FormItem } from 'src/components/Form';
import Modal from 'src/components/Modal';
import Icon from 'src/components/Icon';

const Styles = styled.span`
  svg {
    vertical-align: -${rabbitaiTheme.gridUnit * 1.25}px;
  }
`;

interface SaveQueryProps {
  query: any;
  defaultLabel: string;
  onSave: (arg0: QueryPayload) => void;
  onUpdate: (arg0: QueryPayload) => void;
  saveQueryWarning: string | null;
}

type QueryPayload = {
  autorun: boolean;
  dbId: number;
  description?: string;
  id?: string;
  latestQueryId: string;
  queryLimit: number;
  remoteId: number;
  schema: string;
  schemaOptions: Array<{
    label: string;
    title: string;
    value: string;
  }>;
  selectedText: string | null;
  sql: string;
  tableOptions: Array<{
    label: string;
    schema: string;
    title: string;
    type: string;
    value: string;
  }>;
  title: string;
};

export default function SaveQuery({
  query,
  defaultLabel = t('Undefined'),
  onSave = () => {},
  onUpdate,
  saveQueryWarning = null,
}: SaveQueryProps) {
  const [description, setDescription] = useState<string>(
    query.description || '',
  );
  const [label, setLabel] = useState<string>(defaultLabel);
  const [showSave, setShowSave] = useState<boolean>(false);
  const isSaved = !!query.remoteId;

  const queryPayload = () => ({
    ...query,
    title: label,
    description,
  });

  const close = () => {
    setShowSave(false);
  };

  const onSaveWrapper = () => {
    onSave(queryPayload());
    close();
  };

  const onUpdateWrapper = () => {
    onUpdate(queryPayload());
    close();
  };

  const onLabelChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLabel(e.target.value);
  };

  const onDescriptionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDescription(e.target.value);
  };

  const toggleSave = () => {
    setShowSave(!showSave);
  };

  const renderModalBody = () => (
    <Form layout="vertical">
      <Row>
        <Col xs={24}>
          <FormItem label={t('Name')}>
            <Input type="text" value={label} onChange={onLabelChange} />
          </FormItem>
        </Col>
      </Row>
      <br />
      <Row>
        <Col xs={24}>
          <FormItem label={t('Description')}>
            <TextArea
              rows={4}
              value={description}
              onChange={onDescriptionChange}
            />
          </FormItem>
        </Col>
      </Row>
      {saveQueryWarning && (
        <>
          <br />
          <div>
            <Row>
              <Col xs={24}>
                <small>{saveQueryWarning}</small>
              </Col>
            </Row>
            <br />
          </div>
        </>
      )}
    </Form>
  );

  return (
    <Styles className="SaveQuery">
      <Button buttonSize="small" onClick={toggleSave}>
        <Icon
          name="save"
          color={rabbitaiTheme.colors.primary.base}
          width={20}
          height={20}
        />{' '}
        {isSaved ? t('Save') : t('Save as')}
      </Button>
      <Modal
        className="save-query-modal"
        onHandledPrimaryAction={onSaveWrapper}
        onHide={close}
        primaryButtonName={isSaved ? t('Save') : t('Save as')}
        width="620px"
        show={showSave}
        title={<h4>{t('Save query')}</h4>}
        footer={[
          <>
            <Button onClick={close} data-test="cancel-query" cta>
              {t('Cancel')}
            </Button>
            <Button
              buttonStyle={isSaved ? undefined : 'primary'}
              onClick={onSaveWrapper}
              className="m-r-3"
              cta
            >
              {isSaved ? t('Save as new') : t('Save')}
            </Button>
            {isSaved && (
              <Button
                buttonStyle="primary"
                onClick={onUpdateWrapper}
                className="m-r-3"
                cta
              >
                {t('Update')}
              </Button>
            )}
          </>,
        ]}
      >
        {renderModalBody()}
      </Modal>
    </Styles>
  );
}
