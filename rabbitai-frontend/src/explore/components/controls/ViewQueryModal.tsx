import React, { useEffect, useState } from 'react';
import { ensureIsArray, styled, t } from '@superset-ui/core';
import SyntaxHighlighter from 'react-syntax-highlighter/dist/cjs/light';
import github from 'react-syntax-highlighter/dist/cjs/styles/hljs/github';
import CopyToClipboard from 'src/components/CopyToClipboard';
import Loading from 'src/components/Loading';
import { CopyButton } from 'src/explore/components/DataTableControl';
import { getClientErrorObject } from 'src/utils/getClientErrorObject';
import { getChartDataRequest } from 'src/chart/chartAction';
import markdownSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/markdown';
import htmlSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/htmlbars';
import sqlSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/sql';
import jsonSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/json';

const CopyButtonViewQuery = styled(CopyButton)`
  && {
    margin: 0 0 ${({ theme }) => theme.gridUnit}px;
  }
`;

SyntaxHighlighter.registerLanguage('markdown', markdownSyntax);
SyntaxHighlighter.registerLanguage('html', htmlSyntax);
SyntaxHighlighter.registerLanguage('sql', sqlSyntax);
SyntaxHighlighter.registerLanguage('json', jsonSyntax);

interface Props {
  latestQueryFormData: object;
}

type Result = {
  query: string;
  language: string;
};

const ViewQueryModal: React.FC<Props> = props => {
  const [result, setResult] = useState<Result[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadChartData = (resultType: string) => {
    setIsLoading(true);
    getChartDataRequest({
      formData: props.latestQueryFormData,
      resultFormat: 'json',
      resultType,
    })
      .then(({ json }) => {
        setResult(ensureIsArray(json.result));
        setIsLoading(false);
        setError(null);
      })
      .catch(response => {
        getClientErrorObject(response).then(({ error, message }) => {
          setError(
            error ||
              message ||
              response.statusText ||
              t('Sorry, An error occurred'),
          );
          setIsLoading(false);
        });
      });
  };
  useEffect(() => {
    loadChartData('query');
  }, [JSON.stringify(props.latestQueryFormData)]);

  if (isLoading) {
    return <Loading />;
  }
  if (error) {
    return <pre>{error}</pre>;
  }
  return (
    <>
      {result.map(item =>
        item.query ? (
          <div>
            <CopyToClipboard
              text={item.query}
              shouldShowText={false}
              copyNode={
                <CopyButtonViewQuery buttonSize="xsmall">
                  <i className="fa fa-clipboard" />
                </CopyButtonViewQuery>
              }
            />
            <SyntaxHighlighter
              language={item.language || undefined}
              style={github}
            >
              {item.query}
            </SyntaxHighlighter>
          </div>
        ) : null,
      )}
    </>
  );
};

export default ViewQueryModal;
