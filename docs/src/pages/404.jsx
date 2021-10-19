import React from 'react';

import Layout from '../components/layout.tsx';
import SEO from '../components/seo';

const NotFoundPage = () => (
  <Layout>
    <SEO title="404: Not found" />
    <h1>NOT FOUND</h1>
    <p>Sorry, you&apos;ve requested a page that does not exist.</p>
  </Layout>
);

export default NotFoundPage;
