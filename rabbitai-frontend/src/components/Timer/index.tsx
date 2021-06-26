
import React, { useEffect, useRef, useState } from 'react';
import { styled } from '@rabbitai-ui/core';
import Label, { Type } from 'src/components/Label';

import { now, fDuration } from 'src/modules/dates';

export interface TimerProps {
  endTime?: number;
  isRunning: boolean;
  startTime?: number;
  status?: Type;
}

const TimerLabel = styled(Label)`
  text-align: left;
  width: 91px;
`;

export default function Timer({
  endTime,
  isRunning,
  startTime,
  status = 'success',
}: TimerProps) {
  const [clockStr, setClockStr] = useState('00:00:00.00');
  const timer = useRef<ReturnType<typeof setInterval>>();

  useEffect(() => {
    const stopTimer = () => {
      if (timer.current) {
        clearInterval(timer.current);
        timer.current = undefined;
      }
    };

    if (isRunning) {
      timer.current = setInterval(() => {
        if (startTime) {
          const endDttm = endTime || now();
          if (startTime < endDttm) {
            setClockStr(fDuration(startTime, endDttm));
          }
          if (!isRunning) {
            stopTimer();
          }
        }
      }, 30);
    }
    return stopTimer;
  }, [endTime, isRunning, startTime]);

  return (
    <TimerLabel type={status} role="timer">
      {clockStr}
    </TimerLabel>
  );
}
