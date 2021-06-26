
import React from 'react';
import { Layout } from 'antd';
import { css } from '@emotion/core';
import { GithubOutlined, SlackSquareOutlined } from '@ant-design/icons';

const { Footer } = Layout;

const footerStyle = css`
  background-color: #323232;
  text-align: center;
  color: #ccc;
  padding: 10px;
  height: 100%;
  width: 100%;
`;

const copyrightStyle = css`
  font-size: 10px;
  color: rgba(255, 255, 255, 0.5);
`;
const apacheLinksStyle = css`
  text-align: center;
  font-size: 10px;
  a {
    color: rgba(255, 255, 255, 0.75);
    margin: 5px;
  }
`;
const iconContainerStyle = css`
  padding: 10px;
  background-color: #323232;
  display: flex;
  flex-direction: row;
  .icons {
    text-align: center;
    width: 100%;
    svg {
      margin-top: 15px;
      color: #ccc;
      width: 30px;
      height: 30px;
      margin: 0 15px;
    }
    .svg {
      width: 30px;
      height: 30px;
      margin-top: -15px;
      margin-left: 10px;
    }
  }
`;

const LayoutFooter = () => (
  <Footer css={footerStyle}>
    <div css={iconContainerStyle}>
      <div className="icons">
        <a
          href="https://join.slack.com/t/apache-rabbitai/shared_invite/zt-l5f5e0av-fyYu8tlfdqbMdz_sPLwUqQ"
          target="_blank"
          rel="noreferrer"
        >
          <SlackSquareOutlined className="icon" />
        </a>
        <a
          href="https://github.com/apache/rabbitai"
          target="_blank"
          rel="noreferrer"
        >
          <GithubOutlined className="icon" />
        </a>
        <a
          href="https://stackoverflow.com/questions/tagged/apache-rabbitai+rabbitai"
          target="_blank"
          rel="noreferrer"
        >
          <img
            alt="StackOverflow"
            src="/images/so-icon.svg"
            className="icon svg"
          />
        </a>
      </div>
    </div>
    <div css={copyrightStyle}>
      © Copyright
      {' '}
      {new Date().getFullYear()}
      ,
      <a href="http://www.apache.org/" target="_blank" rel="noreferrer">
        &nbsp;The Apache Software Foundation
      </a>
      , &nbsp;Licensed under the Apache
      <a
        href="https://apache.org/licenses/LICENSE-2.0"
        target="_blank"
        rel="noreferrer"
      >
        &nbsp;License.
      </a>
      {' '}
      <div>
        Apache Rabbitai, Apache, Rabbitai, the Rabbitai logo, and the Apache
        feather logo are either registered trademarks or trademarks of The
        Apache Software Foundation. All other products or name brands
        are trademarks of their respective holders, including The Apache
        Software Foundation.
      </div>
    </div>
    <div css={apacheLinksStyle} className="apacheLinks">
      <a
        href="https://www.apache.org/"
        target="_blank"
        rel="noreferrer"
      >
        Apache Software Foundation
      </a>
      resources
      <br />
      <a
        href="https://www.apache.org/security/"
        target="_blank"
        rel="noreferrer"
      >
        Security
      </a>
      {' | '}
      <a
        href="https://www.apache.org/foundation/sponsorship.html"
        target="_blank"
        rel="noreferrer"
      >
        Donate
      </a>
      {' | '}
      <a
        href="https://www.apache.org/foundation/thanks.html"
        target="_blank"
        rel="noreferrer"
      >
        Thanks
      </a>
      {' | '}
      <a
        href="https://apache.org/events/current-event"
        target="_blank"
        rel="noreferrer"
      >
        Events
      </a>
      {' | '}
      <a
        href="https://apache.org/licenses/"
        target="_blank"
        rel="noreferrer"
      >
        License
      </a>
    </div>
  </Footer>
);

export default LayoutFooter;
