
import React, { useState } from 'react';
import { css } from '@emotion/core';
import {
  Card, Row, Col, List, Modal, Button,
} from 'antd';
import SEO from '../components/seo';
import Layout from '../components/layout';

const learningLinks = [
  [
    "O'Reilly Live Training: Rapid Data Exploration and Analysis with Apache Rabbitai",
    'https://learning.oreilly.com/live-training/courses/rapid-data-exploration-and-analysis-with-apache-rabbitai/0636920457251/',
  ],
  [
    'Unlocking Advanced Data Analytics on The Data Lake Using Apache Rabbitai and Dremio from Dremio',
    'https://www.dremio.com/tutorials/dremio-apache-rabbitai/',
  ],
  [
    'Test-driving Apache Rabbitai from SmartCat',
    'https://blog.smartcat.io/2018/test-driving-apache-rabbitai/',
  ],
];

const installationLinks = [
  [
    'Official Apache releases',
    'https://dist.apache.org/repos/dist/release/rabbitai/',
  ],
  [
    'Locally with Docker',
    'https://rabbitai.apache.org/installation.html#start-with-docker',
  ],
  [
    'Rabbitai on the Python Package Index (PyPI)',
    'https://dist.apache.org/repos/dist/release/rabbitai/',
  ],
  [
    'Install on CentOS',
    'https://aichamp.wordpress.com/2019/11/20/installing-apache-rabbitai-into-centos-7-with-python-3-7/',
  ],
  [
    'Build Apache Rabbitai from source',
    'https://hackernoon.com/a-better-guide-to-build-apache-rabbitai-from-source-6f2ki32n0',
  ],
  [
    'Installing Apache Rabbitai on IBM Kubernetes Cluster',
    'https://aklin.github.io/guides/kubernetes/2020/10/05/ibm-rabbitai-guide/',
  ],
];

const youtubeVideos = [
  [
    '24XDOkGJrEY',
    'The history and anatomy of Apache Rabbitai',
  ],
  [
    'AqousXQ7YHw',
    'Apache Rabbitai for visualization and for data science',
  ],
  [
    'JGeIHrQYhIs',
    'Apache Rabbitai- Interactive Multi Tab Multiple Dashboards Samples',
  ],
  [
    'z350Gbi463I',
    'Apache Rabbitai - Interactive Sales Dashboard (Demo 1)',
  ],
];

const resourcesContainer = css`
  .link-section {
    margin-bottom: 24px;
    a {
      display: block;
    }
  }
  .links {
    .videos {
      margin-top: 50px;
      text-align: left;
      iframe {
        margin: 15px;
      }
    }
  }
`;

interface featureProps {
  title: string,
  links: string[][],
}
const LinkSection = ({ title, links }: featureProps) => (
  <div className="link-section">
    <h3>{title}</h3>
    <List
      size="small"
      bordered
      dataSource={links}
      renderItem={([link, href]) => (
        <List.Item>
          <a href={href} target="_blank" rel="noreferrer">
            {link}
          </a>
        </List.Item>
      )}
    />
  </div>
);

const Resources = () => {
  const [showModal, setModal] = useState(false);
  const [videoId, setVideoId] = useState(null);
  const [cardTitle, setCardTitle] = useState(null);
  const handleClose = () => {
    setModal(false);
    setVideoId(null);
    setCardTitle(null);
  };
  return (
    <Layout>
      <div className="contentPage">
        <SEO title="Resources" />
        <div css={resourcesContainer}>
          <section>
            <h1 className="title">Resources</h1>
            <span>
              Here’s a collection of resources and blogs about Apache Rabbitai
              from around the Internet. For a more more extensive and dynamic
              list of resources, check out the
              {' '}
              <a href="https://github.com/apache-rabbitai/awesome-apache-rabbitai">
                Awesome Apache Rabbitai
              </a>
              {' '}
              repository
            </span>
          </section>
          <section className="links">
            <Row gutter={24}>
              <Col md={12} sm={24} xs={24}>
                <LinkSection title="Learning Content" links={learningLinks} />
              </Col>
              <Col md={12} sm={24} xs={24}>
                <LinkSection title="Installation" links={installationLinks} />
              </Col>
            </Row>
          </section>
          <section className="videos">
            <Modal
              title={cardTitle}
              visible={showModal}
              onOk={handleClose}
              onCancel={handleClose}
              width={610}
              footer={[
                <Button key="back" onClick={handleClose}>
                  Close
                </Button>,
              ]}
            >
              <iframe
                width="560"
                height="315"
                src={`https://www.youtube.com/embed/${(youtubeVideos[videoId] && youtubeVideos[videoId][0])}`}
                frameBorder="0"
                allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            </Modal>
            <h2>Videos</h2>
            <Card>
              {youtubeVideos.map(([id, title], idx) => (
                <Card.Grid>
                  <div
                    role="button"
                    onClick={() => {
                      setModal(true);
                      setVideoId(idx);
                      setCardTitle(title);
                    }}
                  >
                    <h4>{title}</h4>
                    <img
                      width="100%"
                      alt="youtube vid"
                      src={`http://img.youtube.com/vi/${id}/maxresdefault.jpg`}
                    />
                  </div>
                </Card.Grid>
              ))}
            </Card>
          </section>
        </div>
      </div>
    </Layout>
  );
};

export default Resources;
