import React from 'react';
import { css } from '@emotion/core';
import { Card, List } from 'antd';
import { GithubOutlined } from '@ant-design/icons';
import SEO from '../components/seo';
import Layout from '../components/layout';
import { pmc } from '../resources/data';

const links = [
  [
    'https://join.slack.com/t/apache-rabbitai/shared_invite/zt-l5f5e0av-fyYu8tlfdqbMdz_sPLwUqQ',
    'Slack',
    'interact with other Rabbitai users and community members',
  ],
  [
    'https://github.com/apache/rabbitai',
    'GitHub',
    'create tickets to report issues, report bugs, and suggest new features',
  ],
  [
    'https://lists.apache.org/list.html?dev@rabbitai.apache.org',
    'dev@ Mailing List',
    'participate in conversations with committers and contributors',
  ],
  [
    'https://stackoverflow.com/questions/tagged/rabbitai+apache-rabbitai',
    'Stack Overflow',
    'our growing knowledge base',
  ],
  [
    'https://www.meetup.com/Global-Apache-Rabbitai-Community-Meetup/',
    'Rabbitai Meetup Group',
    'join our monthly virtual meetups and register for any upcoming events',
  ],
  [
    'https://github.com/apache/rabbitai/blob/master/RESOURCES/INTHEWILD.md',
    'Organizations',
    'a list of some of the organizations using Rabbitai in production',
  ],
  [
    'https://github.com/apache-rabbitai/awesome-apache-rabbitai',
    'Contributors Guide',
    'Interested in contributing? Learn how to contribute and best practices',
  ],
];

const communityContainer = css`
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin: 0 auto;
  overflow: auto;
  .communityCard {
    font-size: 12px;
    overflow: hidden;
    margin: 10px 10px;
    .ant-card-meta-title {
      text-overflow: clip;
      white-space: normal;
    }
    .ant-card-body {
      padding: 8px;
      display:inline-block;
      white-space: nowrap;
    }
  }
`;

const getInvolvedContainer = css`
  margin-bottom: 25px;
`;

const Community = () => {
  const pmcList = pmc.map((e) => {
    const name = e.name.indexOf(' ');
    return (
      <a href={e.github} target="_blank" rel="noreferrer" key={name}>
        <Card
          className="communityCard"
          hoverable
          style={{ width: '150px' }}
          size="small"
          cover={<img alt="example" src={e.image} />}
        >
          <GithubOutlined style={{ paddingRight: 3, paddingTop: 3 }} />
          {e.name}
        </Card>
      </a>
    );
  });
  return (
    <Layout>
      <div className="contentPage">
        <SEO title="Community" />
        <section>
          <h1 className="title">Community</h1>
          Get involved in our welcoming, fast growing community!
        </section>
        <section className="joinCommunity">
          <div css={getInvolvedContainer}>
            <h2>Get involved!</h2>
            <List
              size="small"
              bordered
              dataSource={links}
              renderItem={([href, link, post]) => (
                <List.Item>
                  <a href={href}>{link}</a>
                  {' '}
                  -
                  {' '}
                  {post}
                </List.Item>
              )}
            />
          </div>
        </section>
        <section className="ppmc">
          <h2>Apache Committers</h2>
          <div css={communityContainer}>{pmcList}</div>
        </section>
      </div>
    </Layout>
  );
};

export default Community;
