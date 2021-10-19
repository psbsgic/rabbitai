import React from 'react';
import { styled, t } from '@superset-ui/core';
import { SyntaxHighlighterProps } from 'react-syntax-highlighter';
import sqlSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/sql';
import htmlSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/htmlbars';
import markdownSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/markdown';
import jsonSyntax from 'react-syntax-highlighter/dist/cjs/languages/hljs/json';
import github from 'react-syntax-highlighter/dist/cjs/styles/hljs/github';
import SyntaxHighlighter from 'react-syntax-highlighter/dist/cjs/light';
import { ToastProps } from 'src/messageToasts/enhancers/withToasts';
import Icons from 'src/components/Icons';
import copyTextToClipboard from 'src/utils/copy';

SyntaxHighlighter.registerLanguage('sql', sqlSyntax);
SyntaxHighlighter.registerLanguage('markdown', markdownSyntax);
SyntaxHighlighter.registerLanguage('html', htmlSyntax);
SyntaxHighlighter.registerLanguage('json', jsonSyntax);

const SyntaxHighlighterWrapper = styled.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${({ theme }) => theme.colors.grayscale.base};
  }
`;

export default function SyntaxHighlighterCopy({
  addDangerToast,
  addSuccessToast,
  children,
  ...syntaxHighlighterProps
}: SyntaxHighlighterProps & {
  children: string;
  addDangerToast?: ToastProps['addDangerToast'];
  addSuccessToast?: ToastProps['addSuccessToast'];
  language: 'sql' | 'markdown' | 'html' | 'json';
}) {
  function copyToClipboard(textToCopy: string) {
    copyTextToClipboard(textToCopy)
      .then(() => {
        if (addSuccessToast) {
          addSuccessToast(t('SQL Copied!'));
        }
      })
      .catch(() => {
        if (addDangerToast) {
          addDangerToast(t('Sorry, your browser does not support copying.'));
        }
      });
  }
  return (
    <SyntaxHighlighterWrapper>
      <Icons.Copy
        tabIndex={0}
        role="button"
        onClick={e => {
          e.preventDefault();
          e.currentTarget.blur();
          copyToClipboard(children);
        }}
      />
      <SyntaxHighlighter style={github} {...syntaxHighlighterProps}>
        {children}
      </SyntaxHighlighter>
    </SyntaxHighlighterWrapper>
  );
}
