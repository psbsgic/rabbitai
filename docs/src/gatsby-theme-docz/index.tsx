
import React from 'react';
import { theme, useConfig } from 'docz';
import { ThemeProvider } from 'theme-ui';
import { css } from '@emotion/core';
import SEO from '../components/seo';
import Layout from '../components/layout';
import AnchorNavigator from '../components/AnchorNavigator';
import NextLinks from '../components/next';

import 'antd/dist/antd.css';

interface Props {
  children: React.ReactNode;
}

const docLayout = css`
  display: flex;
  flex-direction: row;
  .docSearch-content {
    word-wrap: break-all;
    width: 100%;
  }

  // Hacks to disable Swagger UI's "try it out" interactive mode
  .try-out, .auth-wrapper, .information-container {
    display: none;
  }
`;

const Theme = ({ children }: Props) => {
  const config = useConfig();
  return (
    <ThemeProvider theme={config}>
      <Layout>
        <SEO title="Documentation" />
        <div css={docLayout}>
          <div className="docSearch-content">
            {children}
          </div>
          <AnchorNavigator />
        </div>
        <div>
          <NextLinks />
        </div>
      </Layout>
    </ThemeProvider>
  );
};

// @ts-ignore
export default theme()(Theme);
