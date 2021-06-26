
import React from 'react';
import { useUrlShortener } from 'src/common/hooks/useUrlShortener';
import copyTextToClipboard from 'src/utils/copy';
import { t } from '@rabbitai-ui/core';
import { Menu } from 'src/common/components';

interface ShareMenuItemProps {
  url: string;
  copyMenuItemTitle: string;
  emailMenuItemTitle: string;
  emailSubject: string;
  emailBody: string;
  addDangerToast: Function;
  addSuccessToast: Function;
}

const ShareMenuItems = (props: ShareMenuItemProps) => {
  const {
    url,
    copyMenuItemTitle,
    emailMenuItemTitle,
    emailSubject,
    emailBody,
    addDangerToast,
    addSuccessToast,
    ...rest
  } = props;

  const getShortUrl = useUrlShortener(url);

  async function onCopyLink() {
    try {
      const shortUrl = await getShortUrl();
      await copyTextToClipboard(shortUrl);
      addSuccessToast(t('Copied to clipboard!'));
    } catch (error) {
      addDangerToast(t('Sorry, your browser does not support copying.'));
    }
  }

  async function onShareByEmail() {
    try {
      const shortUrl = await getShortUrl();
      const bodyWithLink = `${emailBody}${shortUrl}`;
      window.location.href = `mailto:?Subject=${emailSubject}%20&Body=${bodyWithLink}`;
    } catch (error) {
      addDangerToast(t('Sorry, something went wrong. Try again later.'));
    }
  }

  return (
    <>
      <Menu.Item key="copy-url" {...rest}>
        <div onClick={onCopyLink} role="button" tabIndex={0}>
          {copyMenuItemTitle}
        </div>
      </Menu.Item>
      <Menu.Item key="share-by-email" {...rest}>
        <div onClick={onShareByEmail} role="button" tabIndex={0}>
          {emailMenuItemTitle}
        </div>
      </Menu.Item>
    </>
  );
};

export default ShareMenuItems;
