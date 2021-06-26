
import React, { useState, useCallback, useRef, FunctionComponent } from 'react';
import { t, useTheme } from '@rabbitai-ui/core';

import { Input, AntdInput } from 'src/common/components';
import { Radio } from 'src/components/Radio';
import { CronPicker, CronError } from 'src/components/CronPicker';
import { StyledInputContainer } from 'src/views/CRUD/alert/AlertReportModal';

interface AlertReportCronSchedulerProps {
  value: string;
  onChange: (change: string) => any;
}

export const AlertReportCronScheduler: FunctionComponent<AlertReportCronSchedulerProps> = ({
  value,
  onChange,
}) => {
  const theme = useTheme();
  const inputRef = useRef<AntdInput>(null);
  const [scheduleFormat, setScheduleFormat] = useState<'picker' | 'input'>(
    'picker',
  );
  const customSetValue = useCallback(
    (newValue: string) => {
      onChange(newValue);
      inputRef.current?.setValue(newValue);
    },
    [inputRef, onChange],
  );
  const [error, onError] = useState<CronError>();

  return (
    <>
      <Radio.Group
        onChange={e => setScheduleFormat(e.target.value)}
        value={scheduleFormat}
      >
        <div className="inline-container add-margin">
          <Radio value="picker" />
          <CronPicker
            clearButton={false}
            value={value}
            setValue={customSetValue}
            disabled={scheduleFormat !== 'picker'}
            displayError={scheduleFormat === 'picker'}
            onError={onError}
          />
        </div>
        <div className="inline-container add-margin">
          <Radio value="input" />
          <span className="input-label">CRON Schedule</span>
          <StyledInputContainer className="styled-input">
            <div className="input-container">
              <Input
                type="text"
                name="crontab"
                ref={inputRef}
                style={error ? { borderColor: theme.colors.error.base } : {}}
                placeholder={t('CRON expression')}
                disabled={scheduleFormat !== 'input'}
                onBlur={event => {
                  onChange(event.target.value);
                }}
                onPressEnter={() => {
                  onChange(inputRef.current?.input.value || '');
                }}
              />
            </div>
          </StyledInputContainer>
        </div>
      </Radio.Group>
    </>
  );
};
