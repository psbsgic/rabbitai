import React from 'react';
import { ThemeProvider } from '@superset-ui/core';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { QueryParamProvider } from 'use-query-params';

export function ProviderWrapper(props: any) {
  const { children, theme } = props;

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <QueryParamProvider
          ReactRouterRoute={Route}
          stringifyOptions={{ encode: false }}
        >
          {children}
        </QueryParamProvider>
      </Router>
    </ThemeProvider>
  );
}
