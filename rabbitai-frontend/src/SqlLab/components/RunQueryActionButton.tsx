
import React from 'react';
import { t, styled, rabbitaiTheme } from '@rabbitai-ui/core';

import { Menu } from 'src/common/components';
import Button, { ButtonProps } from 'src/components/Button';
import Icon from 'src/components/Icon';
import {
  DropdownButton,
  DropdownButtonProps,
} from 'src/components/DropdownButton';

interface Props {
  allowAsync: boolean;
  queryState?: string;
  runQuery: (c?: boolean) => void;
  selectedText?: string;
  stopQuery: () => void;
  sql: string;
  overlayCreateAsMenu: typeof Menu | null;
}

type QueryButtonProps = DropdownButtonProps | ButtonProps;

const buildText = (
  shouldShowStopButton: boolean,
  selectedText: string | undefined,
): string | JSX.Element => {
  if (shouldShowStopButton) {
    return (
      <>
        <i className="fa fa-stop" /> {t('Stop')}
      </>
    );
  }
  if (selectedText) {
    return t('Run selection');
  }
  return t('Run');
};

const onClick = (
  shouldShowStopButton: boolean,
  allowAsync: boolean,
  runQuery: (c?: boolean) => void = () => undefined,
  stopQuery = () => {},
): void => {
  if (shouldShowStopButton) return stopQuery();
  if (allowAsync) {
    return runQuery(true);
  }
  return runQuery(false);
};

const StyledButton = styled.span`
  button {
    line-height: 13px;
    // this is to over ride a previous transition built into the component
    transition: background-color 0ms;
    &:last-of-type {
      margin-right: ${({ theme }) => theme.gridUnit * 2}px;
    }
  }
`;

const RunQueryActionButton = ({
  allowAsync = false,
  queryState,
  selectedText,
  sql = '',
  overlayCreateAsMenu,
  runQuery,
  stopQuery,
}: Props) => {
  const shouldShowStopBtn =
    !!queryState && ['running', 'pending'].indexOf(queryState) > -1;

  const ButtonComponent: React.FC<QueryButtonProps> = overlayCreateAsMenu
    ? (DropdownButton as React.FC)
    : Button;

  const isDisabled = !sql.trim();

  return (
    <StyledButton>
      <ButtonComponent
        onClick={() =>
          onClick(shouldShowStopBtn, allowAsync, runQuery, stopQuery)
        }
        disabled={isDisabled}
        tooltip={
          (!isDisabled &&
            (shouldShowStopBtn
              ? t('Stop running (Ctrl + x)')
              : t('Run query (Ctrl + Return)'))) as string
        }
        cta
        {...(overlayCreateAsMenu
          ? {
              overlay: overlayCreateAsMenu,
              icon: (
                <Icon
                  color={
                    isDisabled
                      ? rabbitaiTheme.colors.grayscale.base
                      : rabbitaiTheme.colors.grayscale.light5
                  }
                  name="caret-down"
                />
              ),
              trigger: 'click',
            }
          : { buttonStyle: 'primary' })}
      >
        {buildText(shouldShowStopBtn, selectedText)}
      </ButtonComponent>
    </StyledButton>
  );
};

export default RunQueryActionButton;
