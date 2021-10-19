import React from 'react';
import { t, useTheme, styled } from '@superset-ui/core';

import Button from 'src/components/Button';
import withToasts from 'src/messageToasts/enhancers/withToasts';
import Icons from 'src/components/Icons';
import CopyToClipboard from 'src/components/CopyToClipboard';
import { storeQuery } from 'src/utils/common';
import { getClientErrorObject } from 'src/utils/getClientErrorObject';
import { FeatureFlag, isFeatureEnabled } from '../../featureFlags';

interface ShareSqlLabQueryPropTypes {
  queryEditor: {
    dbId: number;
    title: string;
    schema: string;
    autorun: boolean;
    sql: string;
    remoteId: number | null;
  };
  addDangerToast: (msg: string) => void;
}

const StyledIcon = styled(Icons.Link)`
  &:first-of-type {
    margin: 0;
    display: flex;
    svg {
      margin: 0;
    }
  }
`;

function ShareSqlLabQuery({
  queryEditor,
  addDangerToast,
}: ShareSqlLabQueryPropTypes) {
  const theme = useTheme();

  const getCopyUrlForKvStore = (callback: Function) => {
    const { dbId, title, schema, autorun, sql } = queryEditor;
    const sharedQuery = { dbId, title, schema, autorun, sql };

    return storeQuery(sharedQuery)
      .then(shortUrl => {
        callback(shortUrl);
      })
      .catch(response => {
        getClientErrorObject(response).then(() => {
          addDangerToast(t('There was an error with your request'));
        });
      });
  };

  const getCopyUrlForSavedQuery = (callback: Function) => {
    let savedQueryToastContent;

    if (queryEditor.remoteId) {
      savedQueryToastContent = `${
        window.location.origin + window.location.pathname
      }?savedQueryId=${queryEditor.remoteId}`;
      callback(savedQueryToastContent);
    } else {
      savedQueryToastContent = t('Please save the query to enable sharing');
      callback(savedQueryToastContent);
    }
  };
  const getCopyUrl = (callback: Function) => {
    if (isFeatureEnabled(FeatureFlag.SHARE_QUERIES_VIA_KV_STORE)) {
      return getCopyUrlForKvStore(callback);
    }
    return getCopyUrlForSavedQuery(callback);
  };

  const buildButton = (canShare: boolean) => {
    const tooltip = canShare
      ? t('Copy query link to your clipboard')
      : t('Save the query to enable this feature');
    return (
      <Button buttonSize="small" tooltip={tooltip} disabled={!canShare}>
        <StyledIcon
          iconColor={
            canShare ? theme.colors.primary.base : theme.colors.grayscale.base
          }
          iconSize="xl"
        />
        {t('Copy link')}
      </Button>
    );
  };

  const canShare =
    !!queryEditor.remoteId ||
    isFeatureEnabled(FeatureFlag.SHARE_QUERIES_VIA_KV_STORE);

  return (
    <>
      {canShare ? (
        <CopyToClipboard
          getText={getCopyUrl}
          wrapped={false}
          copyNode={buildButton(canShare)}
        />
      ) : (
        buildButton(canShare)
      )}
    </>
  );
}

export default withToasts(ShareSqlLabQuery);
