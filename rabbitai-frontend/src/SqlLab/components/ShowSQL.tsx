
import React from 'react';
import SyntaxHighlighter from 'react-syntax-highlighter/dist/cjs/light';
import sql from 'react-syntax-highlighter/dist/cjs/languages/hljs/sql';
import github from 'react-syntax-highlighter/dist/cjs/styles/hljs/github';

import { IconTooltip } from '../../components/IconTooltip';
import ModalTrigger from '../../components/ModalTrigger';

SyntaxHighlighter.registerLanguage('sql', sql);

interface ShowSQLProps {
  sql: string;
  title: string;
  tooltipText: string;
}

export default function ShowSQL({
  tooltipText,
  title,
  sql: sqlString,
}: ShowSQLProps) {
  return (
    <ModalTrigger
      modalTitle={title}
      triggerNode={
        <IconTooltip
          className="fa fa-eye pull-left m-l-2"
          tooltip={tooltipText}
        />
      }
      modalBody={
        <div>
          <SyntaxHighlighter language="sql" style={github}>
            {sqlString}
          </SyntaxHighlighter>
        </div>
      }
    />
  );
}
