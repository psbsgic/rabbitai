import React, { useEffect, useState, FunctionComponent } from 'react';
import moment, { Moment, MomentInput } from 'moment';
import { t, styled } from '@superset-ui/core';
import Icons from 'src/components/Icons';

const REFRESH_INTERVAL = 60000; // every minute

interface LastUpdatedProps {
  updatedAt: MomentInput;
  update?: React.MouseEventHandler<HTMLSpanElement>;
}
moment.updateLocale('en', {
  calendar: {
    lastDay: '[Yesterday at] LTS',
    sameDay: '[Today at] LTS',
    nextDay: '[Tomorrow at] LTS',
    lastWeek: '[last] dddd [at] LTS',
    nextWeek: 'dddd [at] LTS',
    sameElse: 'L',
  },
});

const TextStyles = styled.span`
  color: ${({ theme }) => theme.colors.grayscale.base};
`;

const Refresh = styled(Icons.Refresh)`
  color: ${({ theme }) => theme.colors.primary.base};
  width: auto;
  height: ${({ theme }) => theme.gridUnit * 5}px;
  position: relative;
  top: ${({ theme }) => theme.gridUnit}px;
  left: ${({ theme }) => theme.gridUnit}px;
  cursor: pointer;
`;

export const LastUpdated: FunctionComponent<LastUpdatedProps> = ({
  updatedAt,
  update,
}) => {
  const [timeSince, setTimeSince] = useState<Moment>(moment(updatedAt));

  useEffect(() => {
    setTimeSince(() => moment(updatedAt));

    // update UI every minute in case day changes
    const interval = setInterval(() => {
      setTimeSince(() => moment(updatedAt));
    }, REFRESH_INTERVAL);

    return () => clearInterval(interval);
  }, [updatedAt]);

  return (
    <TextStyles>
      {t('Last Updated %s', timeSince.isValid() ? timeSince.calendar() : '--')}
      {update && <Refresh onClick={update} />}
    </TextStyles>
  );
};

export default LastUpdated;
